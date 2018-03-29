# from rawpycdump import read_pyc
from pycdump import read_pyc
from opcode import *
import inspect
# https://docs.python.org/3/library/inspect.html


class Module:
    """
    __doc__	documentation string
 	__file__	filename (missing for built-in modules)
    """

class Class:
    """
    __doc__	documentation string
 	__name__	name with which this class was defined
 	__qualname__	qualified name
 	__module__	name of module in which this class was defined
    """

class Method:
    """
    __doc__	documentation string
 	__name__	name with which this method was defined
 	__qualname__	qualified name
 	__func__	function object containing implementation of method
 	__self__	instance to which this method is bound, or None
    """

class Traceback:
    """
    tb_frame	frame object at this level
 	tb_lasti	index of last attempted instruction in bytecode
 	tb_lineno	current line number in Python source code
 	tb_next	next inner traceback object (called by this level)
    """

class Frame:
    """
    f_back	next outer frame object (this frame’s caller)
 	f_builtins	builtins namespace seen by this frame
 	f_code	code object being executed in this frame
 	f_globals	global namespace seen by this frame
 	f_lasti	index of last attempted instruction in bytecode
 	f_lineno	current line number in Python source code
 	f_locals	local namespace seen by this frame
 	f_restricted	0 or 1 if frame is in restricted execution mode
 	f_trace	tracing function for this frame, or None
    """

class Generator:
    """
    __name__	name
 	__qualname__	qualified name
 	gi_frame	frame
 	gi_running	is the generator running?
 	gi_code	code
 	gi_yieldfrom	object being iterated by yield from, or None
    """

class Coroutine:
    """
    __name__	name
 	__qualname__	qualified name
 	cr_await	object being awaited on, or None
 	cr_frame	frame
 	cr_running	is the coroutine running?
 	cr_code
    """

class Builtin:
    """
    __doc__	documentation string
 	__name__	original name of this function or method
 	__qualname__	qualified name
 	__self__	instance to which a method is bound, or None
    """


def run_code(code):
    frame = Frame
    print(code)


if __name__ == '__main__':
    filename = '__pycache__/test.cpython-38.pyc'
    with open(filename, "rb") as file:
        magic, modtime, filesz, code = read_pyc(file)
        run_code(code)


