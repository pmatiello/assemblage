class assemblage(object):
    
    def __init__(self):
        self.types = {}
    
    def register(self, type, requires=None, factory=None):
        dependencies = requires or []
        factory = factory or (lambda *deps : self.__build(type, deps))
        self.types[type] = type_information(factory, dependencies)
    

    def new(self, type, cache=None):
        if (type not in self.types):
            raise ValueError("Can't build instance for unregistered type %s" % type)
        if (cache is not None and type in cache.keys()):
            return cache[type]
        instance = self._build_new(type)
        self._add_to_cache(cache, type, instance)
        return instance

    def _build_new(self, type):
        dependencies = self._build_dependencies(type)
        return self.types[type].factory(*dependencies)

    def _build_dependencies(self, type):
        dependencies = []
        for each in self.types[type].dependencies:
            dependencies.append(self.new(each))
        return dependencies
  
    def _add_to_cache(self, cache, type, instance):
        if (cache is not None):
            cache[type] = instance
    
    def __build(self, type, dependencies):
        return type(*dependencies)


class type_information(object):
    
    def __init__(self, factory, dependencies):
        self.factory = factory
        self.dependencies = dependencies