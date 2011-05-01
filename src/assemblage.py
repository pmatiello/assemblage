class assembler(object):
    
    def __init__(self, parent=None):
        self.types = {}
        self.cache = {}
        self.parent = parent
    
    def register(self, type, requires=None, factory=None, cacheable=True):
        dependencies = requires or []
        factory = factory or (lambda *deps : self.__build(type, deps))
        self.types[type] = type_information(factory, dependencies, cacheable)

    def __build(self, type, dependencies):
        return type(*dependencies)
    
    def spawn_child(self):
        return assembler(parent=self)

    def new(self, type):
        if (not self._can_build_type(type)):
            raise ValueError("Can't build instance for unregistered type %s" % type)
        
        cached_instance = self._retrieve_from_cache(type)
        if (cached_instance is not None):
            return cached_instance
        
        new_instance = self._build_new(type)
        self._add_to_cache(type, new_instance)
        return new_instance

    def _can_build_type(self, type):
        if (type in self.types):
            return True
        if (self.parent and self.parent._can_build_type(type)):
            return True
        return False
    
    def _retrieve_from_cache(self, type):
        if (type in self.cache.keys()):
            return self.cache[type]
        if (self.parent):
            return self.parent._retrieve_from_cache(type)
        return None
    
    def _build_new(self, type):
        dependencies = self._build_dependencies(type)
        return self._type_information(type).factory(*dependencies)

    def _build_dependencies(self, type):
        dependencies = []
        for each in self._type_information(type).dependencies:
            dependencies.append(self.new(each))
        return dependencies
  
    def _add_to_cache(self, type, instance):
        if (self._type_information(type).cacheable):
            self.cache[type] = instance

    def _type_information(self, type):
        if (type in self.types):
            return self.types[type]
        if (self.parent):
            return self.parent._type_information(type)
        return None
    

class type_information(object):
    
    def __init__(self, factory, dependencies, cacheable):
        self.factory = factory
        self.dependencies = dependencies
        self.cacheable = cacheable