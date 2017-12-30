import graphs



edges = [[1, 4], [0, 2], [1, 3, 5], [2, 6], [0, 5], [2, 4, 6, 9], [3, 5, 7], [6], [9], [5, 8, 10], [9]]
# edges = [[1, 3, 4], [0, 2, 3], [1, 4], [0, 1], [0, 2]]
# edges = [[1], [0, 2], [1, 3], [2]]
# edges = [[1, 3], [0, 2], [1, 3], [0, 2]]
# edges = [[1, 4], [0, 2, 3], [1, 4], [1], [0, 2]]
# edges = [[1, 3], [0, 2, 4], [1, 3, 5], [0, 2], [1], [2, 6], [5]]
n = len(edges)

G = graphs.Graphs(edges)
G.findArticulationPoints()

print("Articulation points:")
for i in G.articulationPoints:
    print(i)
print()
G.constructBlocks()
print("Components:")
for i in G.blockContains:
    print(i)
print()
for i in range(n):
    print("Vertex: " + str(i) + ", in component(s): " + str(G.blockOfU[i]))
print()
G.brandes()
for i in range(n):
    print("BC(" + str(i) + ") = " + str(G.bc[i]))
print()
G.BCBCC()
for i in range(n):
    print("BC(" + str(i) + ") = " + str(G.bc[i]))