import graphs

edges1 = [[0, 1], [1, 2], [1]]
edges2 = [[0], [0, 1, 2], [1]]
G = graphs.connectTree(edges1, edges2)
print(G.edges)

