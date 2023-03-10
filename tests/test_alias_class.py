
class Vector:
  pass

Vector3f = Vector
        
if __name__ == "__main__":
    import test_alias_class
    import sys
    sys.path.insert(0, "..")
    from pybind11_stubgen import ModuleStubsGenerator


    generator = ModuleStubsGenerator(test_alias_class)
    generator.parse()
    print('\n'.join(generator.to_lines()))


