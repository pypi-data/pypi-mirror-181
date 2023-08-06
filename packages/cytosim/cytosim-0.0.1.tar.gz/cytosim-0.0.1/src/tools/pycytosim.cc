// Cytosim was created by Francois Nedelec. Copyright 2007-2017 EMBL.
/**
 This is a program to analyse simulation results:
 it reads a trajectory-file, and provides a python interface to it.
   
   * @TODO :    - manage to return ObjectSet from simul, in order to not necessitate frame()
                - bead and sphere
                - live player + python ? o_O
                - specialized classes, including dynamic spaces
                - and so on and so forth
*/


/**

  To use in python : move the cytosim...._.so file to a folder with *.cmo files
    We recommend using cym/aster.cym for a demo.
   
    Then run : 
        
    import cytosim
    sim = cytosim.open()
    sim.prop.timestep 
    frame = cytosim.load(0)
    fibers = frame["microtubule"]
    fibers.prop.segmentation = 1.337    # <- Yes, yes, yes.
    fibers[0].points()
    fibers[0].id()
    fibers[0].join(fibers[1]) # <- yes, indeed
    core = frame["core"][0]
    core.points()
    while frame.loaded:
        print(frame.time)
        frame = frame.next()
         

    OR, IN LIVE MODE !

    sim = cytosim.start('cym/aster.cym')
    fibers = sim.fibers
    fibers[0].join(fibers[1])    # <- Yes, yes, yes. 
    sim.run(10)
     
    # etc...
*/

/*
@TODO : an interface for FiberSet (problem : cannot iterate because of FiberSet interface)
@TODO : support input arguments
 */
#include "pycytosim.h"

namespace py = pybind11;

/// Using global vars, sorry not sorry.
FrameReader reader;
int __is_loaded__ = 0;
SimThread * thread;
bool __saved__ = 0;
Parser * parser;

extern FrameReader reader;
extern int __is_loaded__;
extern SimThread * thread;
extern bool __saved__;
extern Parser * parser;

void gonna_callback(void) {};

/**
 * @brief Open the simulation from the .cmo files
 * @return 
 */
Simul * open()
{   
    
    int verbose = 1;
    int prefix = 0;
    
    Glossary arg;

    std::string input = TRAJECTORY;
    std::string str;

    Simul * sim = new Simul;
    
    unsigned period = 1;

    arg.set(input, ".cmo") || arg.set(input, "input");    
    if ( arg.use_key("-") ) verbose = 0;

    try
    {
        RNG.seed();
        sim->loadProperties();
        reader.openFile(input);
        Cytosim::all_silent();
        __is_loaded__ = 1;
    }
    catch( Exception & e )
    {
        std::clog << "Aborted: " << e.what() << '\n';
        return nullptr;
    }

    return sim;
}

/**
 * @brief Starts a simulation from a config file fname
 * @param fname
 * @return 
 */
Simul * start(std::string fname) {
    int n = fname.length();
    char inp[n] ;
    std::strcpy(inp, fname.c_str());
    Glossary arg;
    arg.read_string(inp,2);
    
    if ( ! arg.use_key("+") )
    {
        Cytosim::out.open("messages.cmo");
        Cytosim::log.redirect(Cytosim::out);
        Cytosim::warn.redirect(Cytosim::out);
    }
    
    Simul * simul = new Simul;
    try {
        simul->initialize(arg);
    }
    catch( Exception & e ) {
        print_magenta(std::cerr, e.brief());
        std::cerr << '\n' << e.info() << '\n';
    }
    catch(...) {
        print_red(std::cerr, "Error: an unknown exception occurred during initialization\n");
    }
    
    time_t sec = TicToc::seconds_since_1970();
    
    std::string file = simul->prop->config_file;
    std::string setup = file;
    
    parser = new Parser(*simul, 0, 1, 0, 0, 0);
    parser->readConfig();
    thread = new SimThread(*simul, &gonna_callback);
    thread->start();
    __is_loaded__ = 2;
    return simul;
}

/**
 * @brief Prepares a given frame by sorting objects into object groups
 * @param sim
 * @param reader
 * @param fr
 * @return 
 */
int loader( Simul * sim, FrameReader * reader, int fr) 
{   
	int load = 1;
    if (__is_loaded__ == 1) {
        try 
        {
            load = reader->loadFrame(*sim, fr);
            if (load!=0) {
                std::clog << "Unable to load frame " << fr << ". Maybe frame does not exist." << std::endl;
            } 
                
        }
        catch( Exception & e )
        {
            std::clog << "Aborted: " << e.what() << '\n';
        }
    }
    else{
        std::clog << "Simulation not loaded : use cytosim.open() first" << std::endl;
    }
    
    return load;
}

/**
 * @brief Loads the next frame
 * @param sim
 * @param reader
 * @return 
 */
int loadNext( Simul * sim, FrameReader * reader) 
{   
	int load = 1;
    if (__is_loaded__ == 1) {
        try 
        {
            load = reader->loadNextFrame(*sim);
            if (load!=0) {
                std::clog << "Unable to load next frame. Maybe frame does not exist." << std::endl;
            } 
                
        }
        catch( Exception & e )
        {
            std::clog << "Aborted: " << e.what() << '\n';
        }
    }
    else{
        std::clog << "Simulation not loaded : use cytosim.open() first" << std::endl;
    }
    
    return load;
}

/**
 * @brief A python module to run or play cytosim
 * @return 
 */
PYBIND11_MODULE(cytosim, m) {
    m.doc() = 
				"import cytosim"
				"sim = cytosim.open() \n"
                "sim.prop.timestep \n"
                "frame = cytosim.load(0) \n"
                "fibers = frame['microtubule'] \n"
                "print(len(fibers)) \n"
                "while frame.loaded: \n"
                "    print(frame.time) \n"
                "    frame = frame.next()"
                "# --- OR --- \n"
                "sim = cytosim.start('cym/aster.cym') \n"
                "frame = sim.frame() \n"
                "sim.fibers \n"
                "fibers[0].join(fibers[1])    # <- Yes, yes, yes. \n"
                "sim.run(10) \n"; // optional module docstring
    
    /// Loading properties into the module
    load_object_classes(m);
    load_meca_classes(m);
    load_point_classes(m);
    auto pysim = load_simul_classes(m);
    load_glossary_classes(m);
    load_solid_classes(m);
    load_fiber_classes(m);
    load_hand_classes(m);
    load_space_classes(m);
    load_single_classes(m);
    load_couple_classes(m);
    load_organizer_classes(m);
    
    /// We declare object groups
    // We can later add additional def to any of these groups
    auto fibs = declare_group(m, ObjGroup<Fiber,FiberProp>(), "FiberGroup");
    auto sols = declare_group(m, ObjGroup<Solid,SolidProp>(), "SolidGroup");
    auto spas = declare_group(m, ObjGroup<Space,SpaceProp>(), "SpaceGroup");
    auto beds = declare_group(m, ObjGroup<Bead,BeadProp>(), "BeadGroup");
    auto sfrs = declare_group(m, ObjGroup<Sphere,SphereProp>(), "SphereGroup");
    auto orgs = declare_group(m, ObjGroup<Organizer,Property>(), "OrganizerGroup");
    auto sins = declare_group(m, ObjGroup<Single,SingleProp>(), "SingleGroup");
    auto cous = declare_group(m, ObjGroup<Couple,CoupleProp>(), "CoupleGroup");
    
    ///  Python interface to timeframe : behaves roughly as a Python dict of ObjectGroup
    py::class_<Frame>(m, "Timeframe","Python interface to timeframe : behaves as a Python dictionary of Objectsets")
        .def_readwrite("fibers", &Frame::fibers, py::return_value_policy::reference)
        .def_readwrite("time", &Frame::time)
        .def_readwrite("simul", &Frame::simul)
        .def_readwrite("index", &Frame::index)
        .def_readwrite("loaded", &Frame::loaded)
        .def("update", [](Frame &f) {  return make_frame(f.simul) ; })
        .def("next", [](Frame &f)
			  {	if (loader(f.simul, &reader, f.index+1)==0) 
					{return make_frame_index(f.simul,f.index+1 );}
				return new Frame;}) //py::return_value_policy::reference
        .def("__iter__", [](Frame &f) {
            return py::make_iterator(f.objects.begin(), f.objects.end());
        }, py::keep_alive<0, 1>())
        .def("keys", [](Frame &f) {  return f.objects.attr("keys")() ; })
        .def("items", [](Frame &f) { return f.objects.attr("items")() ; })
        .def("__getitem__",[](const Frame &f, std::string s) {
                 return f.objects[py::cast(s)];
             }, py::return_value_policy::reference);

    
    /// Opens the simulation from *.cmo files
    m.def("open", &open, "@PYD;C:PyCytosim;T:loads simulation from object files", py::return_value_policy::reference);
    m.def("start", &start, "@PYD;C:PyCytosim;T:loads simulation from config files", py::return_value_policy::reference);
    m.def("str_to_glos", &str_to_glos, "@PYD;C:PyCytosim;T:converts string to Glossary");

    /// Expading Python interface to simul
    pysim.def("load", [](Simul * sim, size_t i) // @PYD;C:Simul;T:loads a frame by index, e.g. frame = sim.load(2);
            {return !loader(sim, &reader, i);  }); 
    pysim.def("next", [](Simul * sim) // @PYD;C:Simul;T:loads next frame, e.g. frame = sim.next();
            {return !loadNext(sim, &reader);  }); 
	pysim.def("loadframe", [](Simul * sim, size_t i) // @PYD;C:Simul
            {	if (loader(sim, &reader, i)==0) 
					{return make_frame_index(sim,i);}
				return new Frame;});
    pysim.def("frame", [](Simul * sim)  // @PYD;C:Simul;T:returns current frame, e.g. frame = sim.frame();
            {return make_frame(sim);} );
    pysim.def("writeObjects",  [](Simul * sim) { // @PYD;C:Simul;T: writes Objects to default trajectory file
        sim->writeObjects(sim->prop->trajectory_file,__saved__,1);
        if (!__saved__) {__saved__ = 1;}  ;} );
    pysim.def("writeObjects",  [](Simul * sim, std::string & str) { // @PYD;C:Simul;T: writes Objects to a trajectory file, e.g. writeOjects('file.cmo')
        sim->writeObjects(str,__saved__,1);
        if (!__saved__) {__saved__ = 1;}  ;} );
    pysim.def("save", [](Simul * sim) { // @PYD;C:Simul;T: saves current state to trajectory file
            sim->writeObjects(sim->prop->trajectory_file,__saved__,1);
            if (!__saved__) {__saved__ = 1;};
            sim->writeProperties(&sim->prop->property_file[0],1);
        });
    pysim.def("add",  [](Simul * sim, py::args args) { // @PYD;C:Simul;T: adds objects to simulation, see provided examples 
        std::string name = "";
        std::string how = "";
        int many = 1;
        int nargs = args.size();
        if (nargs>0) {
            name = py::cast<std::string>(args[0]);
        }
        if (nargs>1) {
            how = py::cast<std::string>(args[1]);
        }
        if (nargs>2) {
            many = py::cast<int>(args[2]);
        }
        Glossary glos = Glossary(how);
        ObjectList objects;
        for (int i=0;i<many;++i) {
            auto objs = parser->execute_new(name, glos);
            objects.push_back(objs[0]);
        }
        return objects;
        }, py::return_value_policy::reference); 
    pysim.def("cut",  [](Simul * sim, std::string & name, std::string & where) { // @PYD;C:Simul;T: performes a cut : sim.cut(filament_name, where), see Parser.execute_cut  (C++)
            Glossary glos = Glossary(where);
            parser->execute_cut(name, glos);
            });
    pysim.def("delete",  [](Simul * sim, std::string & name, std::string & how, int number) { // @PYD;C:Simul;T: deletes objects from simulation, see provided examples
            Glossary glos = Glossary(how);
            parser->execute_delete(name, glos, number);
            });
    pysim.def("import",  [](Simul * sim, std::string & file, std::string & what, std::string & how) { // @PYD;C:Simul;T: imports objects from text file, see provided examples
            Glossary glos = Glossary(how);
            parser->execute_import(file, what, glos);
            });
    pysim.def("export",  [](Simul * sim, std::string & file, std::string & what, std::string & how) { // @PYD;C:Simul;T: export objects to text file, see provided examples
            Glossary glos = Glossary(how);
            parser->execute_export(file, what, glos);
            });
    pysim.def("run",  [](Simul * sim, py::args args) { // @PYD;C:Simul;T: runs the simulation ; eg. sim.run(1) ; sim.run(1,arguments)
            std::string how = "";
            int many = 1;
            int nargs = args.size();
            if (nargs>0) {
                many = py::cast<int>(args[0]);
            }
            if (nargs>1) {
                how = py::cast<std::string>(args[1]);
            }
            Glossary glos = Glossary(how);
            parser->execute_run(many, glos,0);
            });
    pysim.def("set",  [](Simul * sim, std::string & cat, std::string & name, std::string & how) { // @PYD;C:Simul; defines a new object, see provided example
            Glossary glos = Glossary(how);
            parser->execute_set(cat, name, glos);
            return glos;
            });        

            
}

