import graphs

n = 11
m = 13
edges = {0: [1, 4], 1: [0, 2], 2: [1, 3, 5], 3: [2, 6], 4: [0, 5], 5: [2, 4, 6, 9], 6: [3, 5, 7], 7: [6], 8: [9],
         9: [5, 8, 10], 10: [9]}
G = graphs.Graphs(edges)
G.constructBlocks()

print("Articulation points:")
for i in G.articulationPoints:
    print(i)
print()
print("Components:")
for i in G.blockContains:
    print(i)
print()
for i in range(n):
    print("Vertex: " + str(i) + ", in component(s): " + str(G.blockOfU[i]))
print()
G.brandes()
for i in range(n):
    print(G.bc[i])