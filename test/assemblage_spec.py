from assemblage import assemblage
from fixtures import *
from mocker import Mocker, expect, MATCH

class assemblage_spec:
    
    def setUp(self):
        self.mockery = Mocker()
        self.assembler = assemblage()
        self.assembler.register(no_deps)
        self.assembler.register(one_dep, requires=[no_deps])
        self.assembler.register(two_deps, requires=[no_deps, one_dep], cacheable=False)
    
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
    
    def should_build_objects_without_dependencies_from_factories(self):
        factory = self.mockery.mock()
        expect(factory()).result(12345)
        with self.mockery:
            self.assembler.register(int, requires=[], factory=factory)
            instance = self.assembler.new(int)
        assert instance == 12345
    
    def should_build_objects_with_dependencies_from_factories(self):
        factory = self.mockery.mock()
        expect(
            factory(MATCH(lambda arg : type(arg) == no_deps))
        ).result(12345)
        with self.mockery:
            self.assembler.register(int, requires=[no_deps], factory=factory)
            instance = self.assembler.new(int)
        assert instance == 12345
    
    def should_add_the_new_instance_to_the_cache(self):
        instance = self.assembler.new(no_deps)
        assert self.assembler.cache[no_deps] is instance
    
    def should_not_cache_instances_of_classes_registered_as_uncacheable(self):
        self.assembler.new(two_deps)
        assert two_deps not in self.assembler.cache
        
    def should_reuse_cached_instances(self):
        first_instance = self.assembler.new(no_deps)
        second_instance = self.assembler.new(no_deps)
        assert second_instance is first_instance
    