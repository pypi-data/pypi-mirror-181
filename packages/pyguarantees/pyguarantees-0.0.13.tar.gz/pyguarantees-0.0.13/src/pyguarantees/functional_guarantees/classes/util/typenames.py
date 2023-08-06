from typing import Any


type_to_str_dict = {
    int: "int",
    float: "float",
    complex: "complex",
    bool: "bool",
    str: "str",
    list: "list",
    tuple: "tuple",
    dict: "dict",
    set: "set",
    frozenset: "frozenset",
    bytes: "bytes",
    bytearray: "bytearray",
    memoryview: "memoryview",
    range: "range",
    None: "None"
}


def get_arg_type_name(arg: Any) -> str:
    try:
        global type_to_str_dict
        return type_to_str_dict[type(arg)]
    except KeyError:
        return str(type(arg))


def get_type_name(t) -> str:
    try:
        global type_to_str_dict
        return type_to_str_dict[t]
    except KeyError:
        return str(t)
