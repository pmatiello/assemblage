class no_deps(object):
    pass

class one_dep(object):
    def __init__(self, dependency):
        self.dependency = dependency

class two_deps(object):
    def __init__(self, first_dep, second_dep):
        self.first_dep = first_dep
        self.second_dep = second_dep
