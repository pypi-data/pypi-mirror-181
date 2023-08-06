from enum import Enum


class SHA1CalcType(Enum):  # list with supported packages
    # hackage = ("y","Cabal","cabal") #cabal
    # gradle = ("y","JAVA","jar") #jar
    # maven_1 = ("y","JAVA","war") #war
    # gradle_1 = ("y","JAVA","war") #war
    # cargo = ("n","Crate","crate") #crate
    # opam = ("n","Opam","opam") #opam
    maven = ("y", "JAVA", "jar", "maven")  # jar
    pypi = ("n", "PYTHON", "whl", "pypi")  # whl
    npm = ("y", "NPM", "js", "npm", "npm")  # js
    cdnjs = ("y", "CDNJS", "js", "cdnjs")  # js
    dotnet = ("y", "NUGET", "exe", ".net")  # exe
    bower = ("y", "BOWER", "jar", "bower")  # jar
    ocaml = ("n", "Opam", "ml", "ocaml")  # ml
    go = ("n", "GO", "go", "go")  # go
    nuget = ("y", "NUGET", "ng", "nuget")  # ng
    rpm = ("n", "RPM", "rpm", "rpm")  # rpm
    composer = ("n", "PHP", "php", "php")  # php
    cocoapods = ("n", "CocoaPods", "pod", "cocoapods")
    cran = ("n", "R", "r", "r")  # r
    gem = ("y", "RUBY", "gem", "ruby")  # gem
    rust = ("y", "RUST", "rs", "rust")  # rs
    rlib = ("y", "RUST", "rlib", "rust")  # rlib
    hex = ("y", "HEX", "hex", "hex", "hex")  # hex, h86
    alpine = ("n", "Alpine", "apk", "alpine")

    @property
    def lower_case(self):
        return self.value[0]

    @property
    def language(self):
        return self.value[1]

    @property
    def ext(self):
        return self.value[2]

    @property
    def libtype(self):
        return self.value[3]

    @classmethod
    def get_package_data(cls, lng: str):
        res = ""
        for el_ in cls:
            if el_.language == lng:
                res = el_.lower_case
                break
        return res

    @classmethod
    def get_package_type(cls, f_t: str):
        try:
            return cls.__dict__[f_t]
        except:
            return []

    @classmethod
    def get_package_type_list_by_ext(cls, ext: str):
        res = []
        for el_ in cls:
            if el_.ext == ext:
                res.append(el_)
        return res
