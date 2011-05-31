class assembler(object):
    
    def __init__(self, parent=None):
        """
        Assembler constructor.
        
        parent: an optional parent assembler.
        """
        self.types = {}
        self.cache = {}
        self.parent = parent
    
    def register(self, type, requires=None, factory=None, cacheable=True):
        """
        Register a new type for construction.
        
        type: the type to be registered.
        requires: an optional list of the types of the dependencies required by instances of the given type.
        factory: an optional factory method capable of building instances of the given type.
        cacheable: whether produced instances of the given type should be cached for reuse. 
        """
        dependencies = requires or []
        factory = factory or (lambda *deps : self.__build(type, deps))
        self.types[type] = type_information(factory, dependencies, cacheable)

    def __build(self, type, dependencies):
        return type(*dependencies)
    
    def spawn_child(self):
        """
        Produce an child assembler.
        
        Child assemblers have access to all registered types and cached instances present in
        any of its ancestors.
        """
        return assembler(parent=self)

    def provide(self, type):
        """
        Provide a instance of the desired type.
        
        If the type is cacheable, it will reuse a previously build instance instead of building a new one.
        
        type: the desired type.
        """
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
            dependencies.append(self.provide(each))
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