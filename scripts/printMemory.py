import gdb

# stolen from libstdc++-v6 printers
# Starting with the type ORIG, search for the member type NAME.  This
# handles searching upward through superclasses.  This is needed to
# work around http://sourceware.org/bugzilla/show_bug.cgi?id=13615.
def find_type(orig, name):
    typ = orig.strip_typedefs()
    while True:
        # Use Type.tag to ignore cv-qualifiers.  PR 67440.
        search = '%s::%s' % (typ.tag, name)
        try:
            return gdb.lookup_type(search)
        except RuntimeError:
            pass
        # The type was not found, so try the superclass.  We only need
        # to check the first superclass, so we don't bother with
        # anything fancier here.
        fields = typ.fields()
        if len(fields) and fields[0].is_base_class:
            typ = fields[0].type
        else:
            raise ValueError("Cannot find type %s::%s" % (str(orig), name))

def lookup_templ_spec(templ, *args):
    """
    Lookup template specialization templ<args...>
    """
    t = '{}<{}>'.format(templ, ', '.join([str(a) for a in args]))
    try:
        return gdb.lookup_type(t)
    except gdb.error as e:
        # Type not found, try again in versioned namespace.
        global _versioned_namespace
        if _versioned_namespace and _versioned_namespace not in templ:
            t = t.replace('::', '::' + _versioned_namespace, 1)
            try:
                return gdb.lookup_type(t)
            except gdb.error:
                # If that also fails, rethrow the original exception
                pass
        raise e

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

def print_unordered_map(unordered_map_name):
    try:
        unordered_map = gdb.parse_and_eval(unordered_map_name)
        hashtable = unordered_map["_M_h"]
        
        valtype = hashtable.type.template_argument(1)
        cached = hashtable.type.template_argument(9).template_argument(0)
        node_type = lookup_templ_spec('std::__detail::_Hash_node', str(valtype),
                                      'true' if cached else 'false')
        
        node_type = node_type.pointer()
        print(f"Determined node type: {node_type}")

        node = unordered_map["_M_h"]["_M_before_begin"]["_M_nxt"]
        print(f"node: {node.address}")

        # Dynamically cast the node to its derived type
        while node:
            derived_node = node.cast(node_type).dereference()
            node = derived_node['_M_nxt']  # Move to the next node

            #print(f"node: {derived_node}")

            valptr = derived_node['_M_storage'].address
            valptr = valptr.cast(derived_node.type.template_argument(0).pointer())
            print(f"value: {valptr.dereference()}")
            
    except gdb.error as e:
        print(f"Error accessing {unordered_map_name}: {e}")
    except RuntimeError as e:
        print(f"Runtime error while processing {unordered_map}: {e}")

# Example usage
#get_unordered_map_node_type("s_map")
print_var1()
# Example for retrieving key-value pairs from a bucket
print_unordered_map("s_map")