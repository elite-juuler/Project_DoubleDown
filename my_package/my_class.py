# class to create properties
class MyClass:
    def __init__(self, values):
        self._values = values

    def _create_property(index):
        def getter(self):
            return self._values[index]
        
        def setter(self, value):
            self._values[index] = value

        return property(getter, setter)
    
# create properties dynamically
properties = ['CardValue']
for i, name in enumerate(properties):
    setattr(MyClass, name, MyClass._create_property(i))