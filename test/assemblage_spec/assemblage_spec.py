from assemblage.assemblage import assemblage
from fixtures import *

class assemblage_spec:
    
    def setUp(self):
        self.assembler = assemblage()
        self.assembler.register(no_deps)
        self.assembler.register(one_dep, requires=[no_deps])
        self.assembler.register(two_deps, requires=[no_deps, one_dep])
        self.assembler.register(from_factory, requires=[no_deps], factory=factory)
    
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
    
    def should_build_objects_from_factories(self):
        instance = self.assembler.new(from_factory)
        assert type(instance) == from_factory
        assert type(instance.dependency) == no_deps