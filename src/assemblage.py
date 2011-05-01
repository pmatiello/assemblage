class assembler(object):
    
    def __init__(self):
        self.types = {}
        self.cache = {}
    
    def register(self, type, requires=None, factory=None, cacheable=True):
        dependencies = requires or []
        factory = factory or (lambda *deps : self.__build(type, deps))
        self.types[type] = type_information(factory, dependencies, cacheable)
    

    def new(self, type):
        if (type not in self.types):
            raise ValueError("Can't build instance for unregistered type %s" % type)
        if (type in self.cache.keys()):
            return self.cache[type]
        instance = self._build_new(type)
        self._add_to_cache(type, instance)
        return instance

    def _build_new(self, type):
        dependencies = self._build_dependencies(type)
        return self.types[type].factory(*dependencies)

    def _build_dependencies(self, type):
        dependencies = []
        for each in self.types[type].dependencies:
            dependencies.append(self.new(each))
        return dependencies
  
    def _add_to_cache(self, type, instance):
        if (self.types[type].cacheable):
            self.cache[type] = instance
    
    def __build(self, type, dependencies):
        return type(*dependencies)


class type_information(object):
    
    def __init__(self, factory, dependencies, cacheable):
        self.factory = factory
        self.dependencies = dependencies
        self.cacheable = cacheable