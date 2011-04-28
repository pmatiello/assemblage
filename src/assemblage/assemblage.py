class assemblage(object):
    
    def __init__(self):
        self.types = {}
    
    def register(self, type, requires=None):
        dependencies = requires or []
        self.types[type] = type_information(dependencies)
    
    def new(self, type):
        if (type in self.types):
            dependencies = self.build_dependencies(type)
            return type(*dependencies)
        raise ValueError("Can't build instance for unregistered type %s" % type)

    def build_dependencies(self, type):
        dependencies = []
        for each in self.types[type].dependencies:
            dependencies.append(self.new(each))
        return dependencies


class type_information(object):
    
    def __init__(self, dependencies):
        self.dependencies = dependencies