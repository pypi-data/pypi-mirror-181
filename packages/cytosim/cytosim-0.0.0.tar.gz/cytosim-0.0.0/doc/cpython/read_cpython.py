from os import listdir
from os.path import isfile, join


__NOTE__ = "@PYD;"
__CLASS__ = "C:"
__TEXT__ = "T:"
__DEF__ = "D:"
__NAME__ = "N:"
__STYLE__ = "S:"

class Member:
    """ A class storing class members """
    def __init__(self, name = None, parent=None, comment=None, text=None, link=None, *args, **kwargs):
        self.name = name
        self.comment = comment
        if parent is not None:
            self.get_adopted(parent)
        self.link = link
        self.text = text
        self.parent = None
        self.lost = False
        self.style = None
        self.depth = 0

    def get_adopted(self, parent):
        self.parent = parent
        if parent is not None:
            self.depth = parent.depth + 1
        else:
            self.depth = 1

    def get_parent_by_name(self, module, name):
        if self.parent is not None:
            if not self.parent.name == name:
                self.parent.rm_member(self)
                classe = module.find_or_create(name)
                classe.add_member(self)
        else:
            classe = module.find_or_create(name)
            classe.add_member(self)

    def __repr__(self):
        return "    "*self.depth+"Member " + self.name + "\n"


class Classe:
    """ A class storing C++ classes and inheritance"""
    def __init__(self, *args, name=None, parent=None, parents=None, **kwargs):
        self.children = []
        self.members = []
        self.comment = None
        self.parents = []
        self.depth = 0
        if parents is not None:
            self.parents.extend(parents)
        if parent is not None:
            if parent not in self.parents:
                self.parents.append(parent)
        self.name = name
        self.update()

        if self.parents:
            self.module = self.parents[0].module
        self.complete(*args, **kwargs)

    def complete(self, *args, comment=None, **kwargs):
        self.comment = comment

    def print(self, *args):
        text = " "
        for arg in args:
            text += arg+" "
        if self.name is not None:
            text += "class %s from " %self.name
            if self.parents:
                for parent in self.parents:
                    text+="%s (" %parent.name
                    for child in parent.children:
                        text += child.name+", "
                    text += "), "
            print(text)
        else:
            raise ValueError("name is None")

    def find_member(self, name):
        member = None
        for m in self.members:
            if m.name==name:
                member = m
        if member is not None:
            return member
        else:
            for child in self.children:
                member = child.find_member(name)
                if member is not None:
                    return member
        return member

    def add_member(self, member):
        if member not in self.members:
            self.members.append(member)
            member.get_adopted(self)

    def rm_member(self, member):
        if member in self.members:
            self.members.remove(member)
            member.get_adopted(self)

    def update(self):
        #self.print("updated")
        self.depth = 0
        for p in self.parents:
            if p.depth >= self.depth:
                self.depth = p.depth+1

    def __repr__(self):
        sentence = ""
        if self.members:
            sentence += "    " * self.depth + self.name + " has members : \n"
            for meth in self.members:
                sentence += meth.__repr__()
        if self.children:
            sentence += "    "*self.depth+self.name+" has children : \n"
            for child in self.children:
                sentence += child.__repr__()
            return sentence
        sentence += "    "*self.depth+self.name+" \n"
        return sentence


    def find_child(self, name):
        if name == self.name:
            return self
        else:
            for child in self.children:
                ans = child.find_child(name)
                if ans is not None:
                    return ans
            return None

    def find_or_create(self, name, *args, **kwargs):
        ans = self.find_child(name)
        if ans is None:
            ans = self.spawn(name, *args, **kwargs)
        return ans

    def spawn(self, name, *args, **kwargs):
        child = Classe(*args, name =name, parent=self, **kwargs)
        self.acknowledge(child)
        child.update()
        return child

    def acknowledge(self, child):
        if child not in self.children:
            self.children.append(child)
        if self not in child.parents:
            child.parents.append(self)
        child.update()
        return


class Module(Classe):
    """ A class storing a module and its derived classes """
    def __init__(self, *args, name=None, **kwargs):
        if name is None:
            self.name = "Module"
        else:
            self.name = name
        super().__init__(*args, name=name, parent=None, **kwargs)
        self.module = self

    def disdain(self, child):
        if child in self.children:
            self.children.remove(child)
        if self in child.parents:
            child.parents.remove(self)
        child.update()
        return

    def define_duo(self, child_name, parent_name, *args,  **kwargs):
        parent = self.find_child(parent_name)
        child = self.find_child(child_name)

        if child is not None:
            # Child exists
            if parent is not None:
                # fParent exists
                if parent not in child.parents:
                    # But fParent is not in child's parents
                    if self in child.parents:
                        self.disdain(child)

                    parent.acknowledge(child)
            else:
                parent = self.spawn(parent_name)
                parent.acknowledge(child)
        else:
            if parent is not None:
                child = parent.spawn(child_name, *args, **kwargs)
            else:
                parent = self.spawn(parent_name)
                child = parent.spawn(child_name, *args, **kwargs)
        child.complete(*args, **kwargs)
        return child

    def define_single(self, name, *args, **kwargs):
        child = self.find_or_create(name, *args, **kwargs)
        child.complete(*args, **kwargs)
        return child


def parse_classe(module, line ):
    words = line.split("<")[1]
    checks = words.split(">")
    comment = None
    words = checks[0].split(",")
    blips = checks[1].split(",")
    if len(blips)>2:
        for blip in blips[2:]:
            s = blip.split('"')
            if len(s)>1:
                comment=s[1]

    if len(words)==1:
        return module.define_single(words[0], comment=comment)
    else:
        for p in words[1:]:
            child = module.define_duo(words[0], p, comment=comment)
        return child

def parse_def(module, classe, line):
    checks = line.split('"')
    member = None
    if len(checks)>2:
        name = checks[1]
        member = Member(name=name)
        if classe is not None:
            classe.add_member(member)
        else:
            module.add_member(member)
            member.lost = True
        parse_comment(module, member, line)
    return member

def parse_comment(module, member, line):
    words = line.split(__NOTE__)
    if len(words) > 1:
        note = words[1].split('"')[0]
        notes = note.split(";")
        for note in notes:
            if note.startswith(__NAME__):
                name = note[2:]
                if member is None:
                    member = module.find_member(name)
                if member is not None:
                    if member.name != name:
                        member = module.find_member(name)
        if member is not None:
            for note in notes:
                if note.startswith(__CLASS__):
                    name = note[2:]
                    member.get_parent_by_name(module, name)
                if note.startswith(__DEF__):
                    member.comment = note[2:]
                if note.startswith(__TEXT__):
                    member.text = note[2:]
                if note.startswith(__STYLE__):
                    member.style = note[2:]
    return None


if __name__=="__main__":
    folders = ["src/cpython", "src/tools"]
    header_files = []
    for folder in folders:
        header_files.extend([join(folder, f) for f in listdir(folder) if isfile(join(folder, f)) and f.endswith(".h") or f.endswith(".cc") ])
    #fname = point_modules.h"
    module = Module(name="Module")
    for fname in header_files:
        with open(fname) as file:
            current_class = None
            current_def = None
            for line in file.readlines():
                line = line.strip()
                if line.find("py::class")>=0:
                    current_class = parse_classe(module, line)
                    current_def = None
                elif line.find(".def")>=0:
                    current_def = parse_def(module, current_class, line)
                elif line.find("@PYD;"):
                    current_def = parse_comment(module, current_def, line)


    module.print("last : ")
    #print(module)
