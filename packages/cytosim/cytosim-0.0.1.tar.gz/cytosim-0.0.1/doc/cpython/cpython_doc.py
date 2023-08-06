import read_cpython as rcp
from os import listdir
from os.path import isfile, join

def read_to_modules(header_files, name=None):
    if name is None:
        name="PyCytosim"
    module = rcp.Module(name=name)
    for fname in header_files:
        with open(fname) as file:
            current_class = None
            current_def = None
            for line in file.readlines():
                line = line.strip()
                if line.find("py::class") >= 0:
                    current_class = rcp.parse_classe(module, line)
                    current_def = None
                elif line.find(".def") >= 0:
                    current_def = rcp.parse_def(module, current_class, line)
                elif line.find("@PYD;"):
                    current_def = rcp.parse_comment(module, current_def, line)
    return module

def print_member(member, classe, classe_link=None, link_pref=None):
    text = ""
    member_link = None
    if member is not None:
        member_text = member.name
        text += "<div class='contents'>"
        if classe_link is not None:
            with open(classe_link,"r") as cl:
                lines = cl.readlines()
                member_text = get_classe_text(lines, member_text, link_pref=link_pref)
        text += "<div class='textblock'>%s" % member_text
        if member.comment is not None:
            text += "<span class='membercomment'> Comment :  </span> \n" %member.comment
        if member.text is not None:
            text += "<span class='membertext'>  %s  </span> \n" % member.text
        text += "</div>"
        text += "</div>"

    return text

def get_link(text):
    try:
        link = text.split('"')[3]
    except:
        link = None
    return link


def print_classe(classe, lines, link_pref=None):
    text = ""
    classe_link=None
    if classe is not None:
        classe_text = classe.name
        text += "<div class='contents' data-class data-depth-%s data-state='0'>" %classe.depth

        if lines is not None:
            classe_text = get_classe_text(lines, classe_text, link_pref=link_pref)
            classe_link = get_link(classe_text)
        text += "<div class='title'> <span data-arr onclick='activate(this)'><a>&#9660;</a></span>"
        text += "<span data-arr onclick='deactivate(this)'><a>&#9650;</a></span>"
        text += "%s</div> " %(classe_text)

        #text += "<div class='textblock'> Members </div> \n"
        if classe.members or classe.comment:
            text += "<div class='directory' data-member>"
            #print(classe.comment)
            if classe.comment is not None:
                if classe.comment.strip():
                    text += "<div class='classcomment'> %s </div>" % classe.comment
            for member in classe.members:
                text += print_member(member, classe, classe_link=classe_link, link_pref=link_pref)
            text += "</div>"
        #text += "<div class='textblock'> Derived classes \n</div>"

        if classe.children:
            text += "<div class='directory'>"
            for child in classe.children:
                text += print_classe(child, lines, link_pref=link_pref)
            text += "</div>"

        text += "</div> \n"
    return   text


def get_classe_text(lines, classe_text, link_pref=None):
    for line in lines:
        l = line.find(">"+classe_text+"<")
        if l>0:
            b = line.find('<a class="el"')
            d = line.find('</a>')
            if b>0 and d>b:
                link = line[b:d+4]
                k = link.find("href=")
                link = link[:(k+6)] + link_pref + link[(k+6):]
                return link
    return classe_text

def make_page(module, html_list, output, link_pref=None):
    with open(output, "w") as out:
        lines = None
        out.write("<!DOCTYPE html> \
        <html xmlns='http://www.w3.org/1999/xhtml' > \
        <link href='cpython.css' rel='stylesheet' type='text/css'/> \
        <head > <title>%s: Bound classes and members</title> \
        <script type='text/javascript'> \
        function activate(element) {element.parentElement.parentElement.setAttribute('data-state','1');} \
        function deactivate(element) {element.parentElement.parentElement.setAttribute('data-state','0');} \
        </script> \
        </head > \
        \n" %module.name)
        out.write("<body>")
        out.write("<div class ='header' ><h1> Bound classes and members.</h1></div >")
        out.write("<div class ='header' > To use the links, please compile the cytosim documentation.  \
        For this run the command : <p/> <span class='membertext'>make doc </span> </div >")
        try:
            page = open(html_list,"r")
            lines = [line.split("</td>")[0] for line in page.readlines() if line.find("entry")>0]
        except:
            out.write("<div class ='textblock' > Could not open the code documentation. Try typing 'make doc' in your terminal.</div >")

        text = print_classe(module, lines, link_pref=link_pref)
        out.write(text)
        out.write("</body>")
        out.write("</html>")

if __name__=="__main__":
    folder = "../../src/cpython/"
    modules_tools = {"PyCytosim" : "../../src/tools/pycytosim.cc", "PyCytoplay" : "../../src/tools/pycytoplay.cc"}
    html_list = "../code/doxygen/annotated.html"
    #output = "cpython_bindings.html"
    link_pref = "../code/doxygen/"
    header_files = []
    header_files.extend([join(folder, f) for f in listdir(folder) if isfile(join(folder, f)) and f.endswith(".h") or f.endswith(".cc") ])

    for name, file in modules_tools.items():
        files = [file]
        files.extend(header_files)
        module = read_to_modules(files,name=name)
        output = "doc_%s.html" %name
        make_page(module, html_list, output, link_pref=link_pref)


