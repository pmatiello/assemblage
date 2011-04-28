class assemblage(object):
    
    def __init__(self):
        self.types = {}
    
    def register(self, type, requires=None, factory=None):
        dependencies = requires or []
        factory = factory or (lambda *deps : self.__build__(type, deps))
        self.types[type] = type_information(factory, dependencies)
    
    def new(self, type):
        if (type in self.types):
            dependencies = self.build_dependencies(type)
            return self.types[type].factory(*dependencies)
        raise ValueError("Can't build instance for unregistered type %s" % type)

    def build_dependencies(self, type):
        dependencies = []
        for each in self.types[type].dependencies:
            dependencies.append(self.new(each))
        return dependencies
    
    def __build__(self, type, dependencies):
        return type(*dependencies)


class type_information(object):
    
    def __init__(self, factory, dependencies):
        self.factory = factory
        self.dependencies = dependencies