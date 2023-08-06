"""
Helper functions for analyzing and generating AST produced by ast.parse().

**The contents of this module are intended only for internal Deephaven use and may change at any time.**
"""

from _ast import Load, Store, Name, Call, keyword, Subscript, FunctionDef, arguments, Slice, Attribute, \
    Assign, AST, If, Compare, Is, List
from numpy import int32, int64, float32, float64, asarray, empty, dtype
from numba.types import Type, int_, float_, complex128
from re import compile
from sys import version_info
is_py2 = version_info.major < 3

if is_py2:
    raise Exception('Python 2 is no longer supported. Please update to python 3.6, 3.7 or 3.8')

is_py38_or_higher = (version_info.major > 3) or (version_info.major == 3 and version_info.minor >= 8)

_regex_int_or_float = compile(r"^(int|float)([0-9]+)$")

if is_py38_or_higher:
    from _ast import Constant
    Num=Constant
    Str=Constant
    # Python 3.8 updated some internal ast classes and no longer uses NameConstant
    # For simplicity, we will just assign the "new correct form" (Constant) to NameConstant
    NameConstant=Constant
else:
    from _ast import Num, Str, NameConstant

from _ast import arg

def array_access(var_name, index):
    """AST array access."""
    var_name = read(var_name)
    # var_name if isinstance(var_name, AST) else read(var_name) if is_py2 else arg(arg=var_name, annotation=None)
    index = index if isinstance(index, AST) else Num(index)
    return Subscript(value=var_name, ctx=Load(), slice=Slice(lower=index))


def write_array(var_name, index):
    """AST writing to an array element."""
    var_name = read(var_name)
    index = index if isinstance(index, AST) else Num(index)
    return Subscript(value=var_name, ctx=Store(), slice=Slice(lower=index))


def read(name):
    """AST read."""
    return Name(id=name.id, ctx=Load()) if isinstance(name, Name) else \
        name_constant(name) if isinstance(name, str) else \
        Name(id=name.arg, ctx=Load()) if isinstance(name, arg) else name


def name_constant(name):
    """AST constant for True, False, and None."""
    # Python >= 3.0 <=3.7 uses NameConstant for True, False and None,
    # Python >= 3.8 uses plain Constant, but we assigned NameConstant=Constant, above, to simplify the code below
    return NameConstant(value=True) if 'True' == name else \
        NameConstant(value=False) if 'False' == name else \
        NameConstant(value=None) if 'None' == name else \
        Name(id=name, ctx=Load())


def read_none():
    """AST read a None."""
    return Name(id='None', ctx=Load()) if is_py2 else NameConstant(value=None)


def read_true():
    """AST read a True."""
    return Name(id='True', ctx=Load()) if is_py2 else NameConstant(value=True)


def read_false():
    """AST read a False."""
    return Name(id='False', ctx=Load()) if is_py2 else NameConstant(value=False)


def write(name):
    "AST write."
    return Name(id=name, ctx=Store())


def keyword_arg(name, value):
    "AST keyword value."
    value = value if isinstance(value, AST) else Str(value)
    return keyword(arg=name, value=value)


def field_read(scope, field):
    """AST field read."""
    scope = scope if isinstance(scope, AST) or isinstance(scope, arg) else read(scope)
    return Attribute(value=scope, attr=field, ctx=Load())


def decorate(fun, args):
    """Create a decorator call.  To get jit(nopython=True), call decorate('jit', {"nopython": "True"}"""
    return Call(func=Name(id=fun, ctx=Load()), args=[],
                keywords=list(map(lambda kv:
                                  keyword(arg=kv[0],
                                          value=read(kv[1])),
                                  itr(args))),
                starargs=None, kwargs=None)


def method_call(scope, args, keywords=None):
    "AST method call."
    scope = scope if isinstance(scope, AST) else read(scope)
    args = list(map(lambda x: x if isinstance(x, AST) or isinstance(x, arg) else read(x), args))
    return Call(func=scope,
                args=args,
                keywords=[] if keywords is None else keywords,
                starargs=None, kwargs=None)


def assign(target, value):
    """AST assignment."""
    # Convert strings to Name(id=target, ctx=Store())
    target = target if isinstance(target, AST) else write(target)
    return Assign(targets=[target], ctx=Load(), value=value)


def param(name):
    """AST name."""
    return name


def arg_or_name(name):
    """AST argument or name."""
    return arg(arg=name, annotation=None)


def to_ast(item):
    """Returns an AST"""
    if isinstance(item, list):
        return list(map(lambda i: to_ast(i), item))
    return item if isinstance(item, AST) \
        else Str(s=item) if isinstance(item, str) \
        else Num(n=item)


def new_list(items):
    """AST list."""
    return List(ctx=Load(),
                elts=to_ast(items) if isinstance(items, list) else [to_ast(items)])


def new_func(func_name, args, body, decorators=None, defaults=None):
    """AST function."""
    return FunctionDef(name=func_name,
                       returns=None,
                       args=arguments(args=args, vararg=None, kwarg=None,
                                      kw_defaults=[],
                                      kwonlyargs=[],
                                      defaults=[] if defaults is None else defaults),
                       body=body,
                       decorator_list=[] if decorators is None else decorators)


def check_if_none(val, body, orelse=[]):
    """AST check if None."""
    val = val if isinstance(val, AST) else read(val)
    cmp = Compare(left=val, ops=[Is()], comparators=[read_none()])
    return If(test=cmp, body=body, orelse=orelse)


def merge_two_dicts(x, y):
    """Merges the contents of two dictionaries."""
    z = x.copy()  # start with x's keys and values
    z.update(y)  # modifies z with y's keys and values & returns None
    return z


def int32_(a):
    """
    Converts the input to a numpy int32 array.

    :param a: input
    :return: numpy array
    """
    return asarray(a, dtype=int32, order='C') if isinstance(a, list) \
        else empty(a, dtype=int32, order='C')


def int64_(a):
    """
    Converts the input to a numpy int64 array.

    :param a: input
    :return: numpy array
    """
    return asarray(a, dtype=int64, order='C') if isinstance(a, list) \
        else empty(a, dtype=int64, order='C')


def float32_(a):
    """
    Converts the input to a numpy float32 array.

    :param a: input
    :return: numpy array
    """
    return asarray(a, dtype=float32, order='C') if isinstance(a, list) \
        else empty(a, dtype=float32, order='C')


def float64_(a):
    """
    Converts the input to a numpy float64 array.

    :param a: input
    :return: numpy array
    """
    return asarray(a, dtype=float64, order='C') if isinstance(a, list) \
        else empty(a, dtype=float64, order='C')


def to_numba_type(item_type):
    """Returns the numba type for a given item type."""
    if isinstance(item_type, int):
        item_type = int_
    elif isinstance(item_type, float):
        item_type = float_
    elif isinstance(item_type, complex):
        item_type = complex128
    return item_type if isinstance(item_type, Type) else \
        int_ if isinstance(item_type, int) else \
        float_ if isinstance(item_type, float) else \
        complex128 if isinstance(item_type, complex) else \
        dtype(item_type)


def num_size(s):
    """Returns the size in bits of a type represented as a string."""
    try:
        return int(_regex_int_or_float.sub(r'\2', s))
    except ValueError:
        return None


def int_or_float(s):
    """Returns if a string representation of an input type is an int or float."""
    return _regex_int_or_float.sub(r'\1', s)


def itr(arr):
    """Iterate over a collection."""
    return arr.iteritems() if is_py2 else arr.items()


def values(dct):
    """Returns a list of all values in a dictionary."""
    return list(dct.itervalues()) if is_py2 else list(dct.values())
