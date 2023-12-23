import gdb


def printBlock(block: gdb.Block):
    for sym in block:
        if sym.is_argument:
            print("argument: ", sym.name)
        print("symbol: ", sym.name)
        print("type: ", sym.type.name)
    print("superblock")
    if block.superblock is not None:
        printBlock(block.superblock)

def analyseFrame(frame: gdb.Frame):
    print("analyse frame: ", frame.name())
    print("src file: ", frame.function().symtab.filename)
    print(frame.function().symtab.filename, frame.function().line)
    block = frame.block()
    printBlock(block)


# This loops through all the Thread objects in the process
for thread in gdb.selected_inferior().threads():

    # This is equivalent to 'thread X'
    thread.switch()       

    print("Thread ", thread.num)

    # Just execute a raw gdb command
    gdb.execute('bt')

    f = gdb.newest_frame()
    while f is not None:
        analyseFrame(f)
        f = gdb.Frame.older(f)


