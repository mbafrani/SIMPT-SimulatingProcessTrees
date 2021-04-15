from network import Network
g=Network()
g.add_nodes(range(4))
g.add_edges([(0, 1), (2, 3)])
print(g)