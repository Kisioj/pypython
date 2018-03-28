import dis, marshal, struct, time, types, binascii

# https://gist.github.com/Kisioj/3f42851d272f25127054a211364a44dd

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

        # code = load_object(FileWrapper(file))
        code = marshal.load(file)
        show_code(code)

def show_code(code, indent=''):
    # pprint.pprint({x: getattr(code, x) for x in dir(code) if not x.startswith('__')})
    # return
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
        if type(const) == types.CodeType:
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
