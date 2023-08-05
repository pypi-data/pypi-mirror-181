from cymem.cymem cimport Pool
from ._bp cimport BP


cdef struct node:
    node* parent
    node* children
    size_t n_children
    double length
    char* name
    int edge_num


cdef void append(node* parent, node* child):
    if parent.n_children == 0:
        parent.children = <node*>mem.alloc(1, sizeof(node))
    else:
        parent.children = <node*>mem.realloc(parent.children, parent.n_children + 1)
    
    parent.children[parent.n_children] = child
    parent.n_children += 1


cdef node* allocate(Py_ssize_t n):
    cdef:
        Pool mem = Pool()
        node* nodes = <node*>mem.alloc(n, sizeof(node))
    return nodes


def to_simple(BP bp):
    cdef: 
        int i
        node* nodes = allocate(sum(bp.B))
    
#    for i in range(sum(bp.B)):
#        node_idx = bp.preorderselect(i)
#        nodes[i].name = bp.name(node_idx)
#        nodes[i].length = bp.length(node_idx)
#        nodes[i].edge_num = bp.edge(node_idx)
#
#        if node_idx != bp.root():
#            # preorder starts at 1 annoyingly
#            parent = bp.preorder(bp.parent(node_idx)) - 1
#            nodes[parent].append(nodes[i])
#
    #root.length = None

    root = nodes[0]
    return <object>root
    #return root
