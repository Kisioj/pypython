MAX_MARSHAL_STACK_DEPTH = 2000
SIZE32_MAX = 0x7FFFFFFF

TYPE_NULL = 0x00 # '0'
TYPE_NONE = 0x4E # 'N'
TYPE_FALSE = 0x46 # 'F'
TYPE_TRUE = 0x54 # 'T'
TYPE_STOPITER = 0x53 # 'S'
TYPE_ELLIPSIS = 0x2E # '.'
TYPE_INT = 0x69 # 'i'

TYPE_INT64 = 0x49 # 'I'  # not used
TYPE_FLOAT = 0x66 # 'f'
TYPE_BINARY_FLOAT = 0x67 # 'g'
TYPE_COMPLEX = 0x78 # 'x'
TYPE_BINARY_COMPLEX = 0x79 # 'y'
TYPE_LONG = 0x6C # 'l'
TYPE_STRING = 0x73 # 's'
TYPE_INTERNED = 0x74 # 't'
TYPE_REF = 0x72 # 'r'
TYPE_TUPLE = 0x28 # '('
TYPE_LIST = 0x5B # '['
TYPE_DICT = 0x7B # '{'
TYPE_CODE = 0x63 # 'c'
TYPE_UNICODE = 0x75 # 'u'
TYPE_UNKNOWN = 0x3F # '?'
TYPE_SET = 0x3C # '<'
TYPE_FROZENSET = 0x3E # '>'
FLAG_REF = 0x80 # '\x80' # with a type, add obj to index */

TYPE_ASCII = 0x61 # 'a'
TYPE_ASCII_INTERNED = 0x41 # 'A'
TYPE_SMALL_TUPLE = 0x29 #  ')'
TYPE_SHORT_ASCII = 0x7A # 'z'
TYPE_SHORT_ASCII_INTERNED =  0x5A # 'Z'

WFERR_OK = 0
WFERR_UNMARSHALLABLE = 1
WFERR_NESTEDTOODEEP = 2
WFERR_NOMEMORY = 3

import dis, struct, sys, time, binascii


class FileWrapper:
    def __init__(self, file, offset=12):
        self.file = file
        self.depth = 0
        self.refs = []
        self.offset = offset

    def __repr__(self):
        return '<file %02x - %d>' % (self.offset, self.offset)

    def unpack(self, bytes, as_string=False):
        result = self.file.read(bytes)
        if as_string:
            result = struct.unpack('<{}s'.format(bytes), result)[0]
        elif bytes == 1:
            result = ord(struct.unpack('<c', result)[0])
        elif bytes == 4:
            # result = struct.unpack('<L', result)[0]
            result = struct.unpack('<l', result)[0]
        elif bytes == 8:
            # result = struct.unpack('<Q', result)[0]
            result = struct.unpack('<q', result)[0]

        self.offset += bytes
        return result

    def increment_depth(self):
        self.depth += 1
        if self.depth >= MAX_MARSHAL_STACK_DEPTH:
            raise MemoryError('too deep!!!')

    def decrement_depth(self):
        self.depth -= 1


def ref_reserve(flag, file):
    if flag:
        idx = len(file.refs)
        file.refs.append('UNREFERENCED')
    else:
        # raise ValueError('flag should be set')
        # idx = -1
        idx = 0

    return idx

def ref_insert(obj, idx, flag, file):
    if flag:  # and idx != -1:
        file.refs[idx] = obj

def ref(obj, flag, file):
    if flag:
        file.refs.append(obj)

def read_object(file):
    type_code = file.unpack(1)

    file.increment_depth()

    flag = type_code & FLAG_REF
    obj_type = type_code & ~FLAG_REF

    if obj_type == TYPE_NULL:
        obj = None  # CHECK

    elif obj_type == TYPE_NONE:
        obj = None

    elif obj_type == TYPE_STOPITER:
        obj = StopIteration # CHECK

    elif obj_type == TYPE_ELLIPSIS:
        obj = ...  # CHECK

    elif obj_type == TYPE_FALSE:
        obj = False

    elif obj_type == TYPE_TRUE:
        obj = True

    elif obj_type == TYPE_INT:
        obj = file.unpack(4)
        ref(obj, flag, file)

    elif obj_type == TYPE_INT64:
        obj = file.unpack(8)
        ref(obj, flag, file)  # CHECK

    elif obj_type == TYPE_LONG:
        raise NotImplementedError  # CHECK

    elif obj_type == TYPE_FLOAT:
        raise NotImplementedError  # CHECK

    elif obj_type == TYPE_BINARY_FLOAT:
        raise NotImplementedError  # CHECK

    elif obj_type == TYPE_COMPLEX:
        raise NotImplementedError  # CHECK

    elif obj_type == TYPE_BINARY_COMPLEX:
        raise NotImplementedError  # CHECK

    elif obj_type == TYPE_STRING:
        length = file.unpack(4)
        obj = file.unpack(length, as_string=True)
        ref(obj, flag, file)

    # elif obj_type == TYPE_ASCII_INTERNED:
    #     is_interned = True
    #     # TYPE_SHORT_ASCII
    #     length = file.unpack(4)
    #     obj = file.unpack(length, as_string=True).decode('utf8')
    #     ref(obj, flag, file)
    #
    # elif obj_type == TYPE_ASCII:
    #     length = file.unpack(4)
    #     obj = file.unpack(length, as_string=True).decode('utf8')
    #     ref(obj, flag, file)

    elif obj_type == TYPE_SHORT_ASCII_INTERNED:
        is_interned = True
        # TYPE_SHORT_ASCII
        length = file.unpack(1)
        obj = file.unpack(length, as_string=True).decode('utf8')
        ref(obj, flag, file)

    elif obj_type == TYPE_SHORT_ASCII:
        length = file.unpack(1)
        obj = file.unpack(length, as_string=True).decode('utf8')
        ref(obj, flag, file)

    # elif obj_type == TYPE_INTERNED:
    #     raise NotImplementedError  # CHECK

    elif obj_type == TYPE_UNICODE:
        length = file.unpack(4)
        if length != 0:
            obj = file.unpack(length, as_string=True).decode('utf8')
            # decode utf8
        else:
            obj = ''

        ref(obj, flag, file)

    elif obj_type == TYPE_SMALL_TUPLE:
        idx = len(file.refs)
        obj = []
        ref(obj, flag, file)

        length = file.unpack(1)  # unsigned
        for _ in range(length):
            obj.append(read_object(file))

        obj = tuple(obj)
        if flag:
            file.refs[idx] = obj

    # elif obj_type == TYPE_TUPLE:
    #     idx = len(file.refs)
    #     obj = []
    #     ref(obj, flag, file)
    #
    #     length = file.unpack(4)
    #     for _ in range(length):
    #         obj.append(read_object(file))
    #
    #     obj = tuple(obj)
    #     file.refs[idx] = obj

    # elif obj_type == TYPE_LIST:
    #     obj = []
    #     ref(obj, flag, file)
    #
    #     length = file.unpack(4)
    #     for _ in range(length):
    #         obj.append(read_object(file))

    elif obj_type == TYPE_DICT:
        obj = {}
        while True:
            key = read_object(file)
            if not key:
                break
            value = read_object(file)
            obj[key] = value

    # elif obj_type == TYPE_SET:
    #     obj = set()
    #     ref(obj, flag, file)
    #
    #     length = file.unpack(4)
    #     for _ in range(length):
    #         obj.add(read_object(file))
    #
    # elif obj_type == TYPE_FROZENSET:
    #     obj = set()
    #     idx = len(file.refs)
    #     ref(obj, flag, file)
    #
    #     length = file.unpack(4)
    #     for _ in range(length):
    #         obj.add(read_object(file))
    #
    #     obj = frozenset(obj)
    #     file.refs[idx] = obj



    elif obj_type == TYPE_CODE:
        idx = ref_reserve(flag, file)
        obj = Code(file)
        ref_insert(obj, idx, flag, file)

    elif obj_type == TYPE_REF:
        ref_id = file.unpack(4)  #, as_string=True)
        # print ((PyVarObject*)p->refs)->ob_size
        # import binascii
        # print('offset:', hex(file.offset))
        # print('ref_id:', binascii.hexlify(ref_id))
        return file.refs[ref_id]

    else:
        raise Exception

    file.decrement_depth()

    # if flag and idx is not None:
    #     file.refs.append(obj)

    return obj


class Code:
    def __init__(self, file):
        # self.idx = 'unique ref counter???' r_ref_reserve, r_ref_insert

        self.co_argcount = file.unpack(4)
        self.co_kwonlyargcount = file.unpack(4)
        self.co_nlocals = file.unpack(4)
        self.co_stacksize = file.unpack(4)
        self.co_flags = file.unpack(4)

        self.co_code = read_object(file)
        self.co_consts = read_object(file)
        self.co_names = read_object(file)
        self.co_varnames = read_object(file)
        self.co_freevars = read_object(file)
        self.co_cellvars = read_object(file)
        self.co_filename = read_object(file)
        self.co_name = read_object(file)

        self.co_firstlineno = file.unpack(4)

        self.co_lnotab = read_object(file)


    def __repr__(self):
        # return f"""<code object {self.co_name} at {hex(id(self))}, file "{self.co_filename}", line {self.co_firstlineno}>"""
        return """<code object {} at {}, file "{}", line {}>""".format(self.co_name, hex(id(self)), self.co_filename, self.co_firstlineno)

def show_file(fname):
    with open(fname, "rb") as file:
        magic = file.read(4)
        file.read(4)
        moddate = file.read(4)
        filesz = file.read(4)  # size of the source file
        modtime = time.asctime(time.localtime(struct.unpack('<L', moddate)[0]))  # < is little-endian and size standard (4), without this on 64 bit machine, L's size is 8
        filesz = struct.unpack('<L', filesz)
        print ("magic %s" % (binascii.hexlify(magic)))
        print ("moddate %s (%s)" % (binascii.hexlify(moddate), modtime))
        print ("files sz %d" % filesz)

        code = read_object(FileWrapper(file))
        # code = marshal.load(file)
        show_code(code)

def show_code(code, indent=''):
    print ("%scode" % indent)
    indent += '   '
    print ("%sargcount %d" % (indent, code.co_argcount))
    print ("%snlocals %d" % (indent, code.co_nlocals))
    print ("%sstacksize %d" % (indent, code.co_stacksize))
    print ("%sflags %04x" % (indent, code.co_flags))
    show_hex("code", code.co_code, indent=indent)
    dis.disassemble(code)
    print ("%sconsts" % indent)
    for const in code.co_consts:
        # if type(const) == types.CodeType:
        if isinstance(const, Code):
            show_code(const, indent+'   ')
        else:
            print ("   %s%r" % (indent, const))
    print ("%snames %r" % (indent, code.co_names))
    print ("%svarnames %r" % (indent, code.co_varnames))
    print ("%sfreevars %r" % (indent, code.co_freevars))
    print ("%scellvars %r" % (indent, code.co_cellvars))
    print ("%sfilename %r" % (indent, code.co_filename))
    print ("%skwonlyargcount %r" % (indent, code.co_kwonlyargcount))
    print ("%sname %r" % (indent, code.co_name))
    print ("%sfirstlineno %d" % (indent, code.co_firstlineno))
    show_hex("lnotab", code.co_lnotab, indent=indent)

def show_hex(label, h, indent):
    h = binascii.hexlify(h)
    if len(h) < 60:
        print ("%s%s %s" % (indent, label, h))
    else:
        print ("%s%s" % (indent, label))
        for i in range(0, len(h), 60):
            print ("%s   %s" % (indent, h[i:i+60]))


if __name__ == '__main__':
    # show_file(sys.argv[1])
    import test
    show_file('__pycache__/test.cpython-38.pyc')
