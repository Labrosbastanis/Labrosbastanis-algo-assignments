import sys

input_filename = sys.argv[1]

g = {}

with open(input_filename) as graph_input:
    for line in graph_input:
        # Split line and convert line parts to integers.
        nodes = [int(x) for x in line.split()]
        if len(nodes) != 2:
            continue
        # If a node is not already in the graph
        # we must create a new empty list.
        if nodes[0] not in g:
            g[nodes[0]] = []
        if nodes[1] not in g:
            g[nodes[1]] = []
        # We need to append the "to" node
        # to the existing list for the "from" node.
        g[nodes[0]].append(nodes[1])
        # And also the other way round.
        g[nodes[1]].append(nodes[0])

def create_pg():
    return []

def add_last(pq, c):
    pq.append(c)

def root(pq):
    return 0

def set_root(pq, c):
    if len(pq) != 0:
        pq[0] = c

def get_data(pq, p):
    return pq[p]

def children(pq, p):
    if 2*p + 2 < len(pq):
        return [2*p + 1, 2*p + 2]
    else:
        return [2*p + 1]

def has_children(pq, p):
    return 2*p + 1 < len(pq)

def extract_last_from_pq(pq):
    return pq.pop()

def parent(p):
    return (p - 1) // 2

def exchange(pq, p1, p2):
    pq[p1], pq[p2] = pq[p2], pq[p1]

def insert_in_pq(pq, g):
    add_last(pq, g)
    i = len(pq) - 1
    while i != root(pq) and get_data(pq, i) < get_data(pq, parent(i)):
        p = parent(i)
        exchange(pq, i, p)
        i = p

def extract_min_from_pq(pq):
    c=pq[root(pq)]
    set_root(pq,extract_last_from_pq(pq))
    i=root(pq)
    while has_children(pq,i):
        j = min(children(pq, i), key=lambda x: get_data(pq, x))
        if get_data(pq, i) < get_data(pq, j):
            return c
        exchange(pq, i, j)
        i = j
    return c

def updatepq(pq,oldpq,new):

    for u,i in enumerate(pq):
        if i ==oldpq:
            pq[u]=new
            while u != root(pq) and get_data(pq, u) < get_data(pq, parent(u)):
                p = parent(u)
                exchange(pq, u, p)
                u = p
    return pq

prq = create_pg() #grammi 1
d={}
p = {} #grammi 3
core = {} #grammi 4

for u in g:
    d[u] = len(g[u])
    p[u]=d[u]
    core[u]=0
    pn= [p[u],u]
    insert_in_pq(prq,pn)

while len(prq)>0:
    minV=extract_min_from_pq(prq)
    core[minV[1]] = minV[0]
    if len(prq) != 0:
        for u in g[minV[1]]:
            d[u]=d[u]-1
            opn=[p[u],u]
            p[u]=max(minV[0],d[u])
            newpn=[p[u],u]
            prq = updatepq(prq,opn,newpn)

a=[]
for key in core.keys():
  a.append(key)

N=len(a)
for i in range(N-1):
    for j in range(N-i-1):
        if a[j]>a[j+1]:
            a[j],a[j+1]=a[j+1],a[j]

for u in a:
    print(a[u],core[u])
