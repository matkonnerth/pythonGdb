import gdb

def print_var1():
    try:
        var1 = gdb.parse_and_eval("var1")
        print("var1 value: ", var1)
        print("var1: ", var1.dereference())
        
        # Downcast var1 to its real type
        real_type = var1.dynamic_type
        var1_downcasted = var1.cast(real_type)
        print("var1 downcasted to real type: ", var1_downcasted.dereference())
    except gdb.error as e:
        print("Error retrieving var1:", e)


print_var1()