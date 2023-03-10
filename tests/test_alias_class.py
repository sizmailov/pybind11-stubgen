import sys
sys.path.insert(0, "..")
from pybind11_stubgen import ModuleStubsGenerator

class Vector:
    def __init__(self, x : float, y : float, z : float):
        self.x = x
        self.y = y
        self.z = z
        
    def __add__(self, v):
        return Vector(self.x + v.x, self.y + v.y, self.z + v.z)
    
    def __sub__(self, v):
        return Vector(self.x - v.x, self.y - v.y, self.z - v.z)
    
    @property
    def length(self):
        return (self.x * self.x + self.y * self.y + self.z * self.z) ** 0.5
    
    def normalize(self):
        len = self.length
        self.x /= len 
        self.y /= len 
        self.z /= len

Vector3f = Vector
        
if __name__ == "__main__":
    import test_alias_class

    generator = ModuleStubsGenerator(test_alias_class)
    generator.parse()
    print('\n'.join(generator.to_lines()))


