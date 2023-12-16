import gdb

def analyseFrame(frame: gdb.Frame):
    gdb.write("analyse frame: %s\n" % frame.name())
    block = frame.block()
    for sym in block:
        gdb.write("symbol: %s\n" % sym.name)
    


# This loops through all the Thread objects in the process
for thread in gdb.selected_inferior().threads():

    # This is equivalent to 'thread X'
    thread.switch()       

    gdb.write("Thread %s \n" % thread.num)

    # Just execute a raw gdb command
    gdb.execute('bt')

    f = gdb.newest_frame()
    while f is not None:
        analyseFrame(f)
        f = gdb.Frame.older(f)


