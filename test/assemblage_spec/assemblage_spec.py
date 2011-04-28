from assemblage.assemblage import assemblage

class no_deps(object):
    pass

class one_dep(object):
    def __init__(self, dependency):
        self.dependency = dependency

class two_deps(object):
    def __init__(self, first_dep, second_dep):
        self.first_dep = first_dep
        self.second_dep = second_dep

class assemblage_spec:
    
    def setUp(self):
        self.assembler = assemblage()
        self.assembler.register(no_deps)
        self.assembler.register(one_dep, requires=[no_deps])
        self.assembler.register(two_deps, requires=[no_deps, one_dep])
    
    def should_not_build_objects_for_unregistered_types(self):
        try:
            self.assembler.new(str)
            assert False
        except ValueError:
            pass
    
    def should_build_objects_without_dependencies(self):
        instance = self.assembler.new(no_deps)
        assert type(instance) == no_deps
    
    def should_build_objects_with_one_dependency(self):
        instance = self.assembler.new(one_dep)
        assert type(instance) == one_dep
        assert type(instance.dependency) == no_deps
    
    def should_build_objects_with_a_few_dependencies(self):
        instance = self.assembler.new(two_deps)
        assert type(instance) == two_deps
        assert type(instance.first_dep) == no_deps
        assert type(instance.second_dep) == one_dep
    
    def should_build_dependencies_correctly(self):
        instance = self.assembler.new(two_deps)
        assert type(instance.second_dep) == one_dep
        assert type(instance.second_dep.dependency) == no_deps