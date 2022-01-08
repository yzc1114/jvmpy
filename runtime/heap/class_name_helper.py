def get_array_class_name(class_name: str) -> str:
    return "[" + to_descriptor(class_name)

def get_component_class_name(class_name: str) -> str:
    if class_name[0] == '[':
        component_type_descriptor = class_name[1:]
        return to_class_name(component_type_descriptor)
    raise Exception("Not array: " + class_name)

def to_class_name(descriptor: str) -> str:
    if descriptor[0] == '[': # array
        return descriptor
    if descriptor[0] == 'L': # object
        return descriptor[1: len(descriptor) - 1]
    for class_name, d in PRIMTIVE_TYPES_DICT.items():
        if d == descriptor:  # primitive type
            return class_name
    raise Exception("Invalid descriptor: " + descriptor)

def to_descriptor(class_name):
    if class_name[0] == '[':
        return class_name
    if class_name in PRIMTIVE_TYPES_DICT.keys():
        return PRIMTIVE_TYPES_DICT[class_name]
    else:
        return "L" + class_name + ";"

PRIMTIVE_TYPES_DICT = {
    "void": "V",
    "boolean": "Z",
    "byte": "B",
    "short": "S",
    "int": "I",
    "long": "J",
    "char": "C",
    "float": "F",
    "double": "D",
}