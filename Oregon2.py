import brandes
import time

file = open("oregon2_010526.txt")
vertex_to_ID = []
ID_to_vertex = {}
edges = []
m = 0
for line in file:
    if line[0] != "#":
        splitLine = line.split()
        if splitLine[0] not in ID_to_vertex:
            ID_to_vertex[splitLine[0]] = len(vertex_to_ID)
            vertex_to_ID.append(int(splitLine[0]))
            edges.append([])
        if splitLine[1] not in ID_to_vertex:
            ID_to_vertex[splitLine[1]] = len(vertex_to_ID)
            vertex_to_ID.append(int(splitLine[1]))
            edges.append([])
        u = ID_to_vertex[splitLine[0]]
        v = ID_to_vertex[splitLine[1]]
        if u not in edges[v]: # This turns the directed graph into an undirected graph
            edges[v].append(u)
            edges[u].append(v)
            m += 1
G = brandes.Graphs(edges)
n = G.n
print("Number of vertices: " + str(n))
print("Number of edges: " + str(m))
print("Graph is connected? " + str(G.is_connected()))
print("Graph is undirected? " + str(G.is_undirected()))
t = time.process_time()
G.dfs(0, True)
print("Dfs takes " + str(time.process_time() - t) + " seconds to complete")
t = time.process_time()
G.findArticulationPoints()
print("find_articulation_points takes " + str(time.process_time() - t) + " seconds to complete")
t = time.process_time()
G.constructBlocks()
print("construct_blocks takes " + str(time.process_time() - t) + " seconds to complete")
t = time.process_time()
G.constructWeightedBlockTree()
print("construct_weighted_block_tree takes " + str(time.process_time() - t) + " seconds to complete")
t = time.process_time()
G.BCBCC()
print("BCBCC takes " + str(time.process_time() - t) + " seconds to complete")
results_of_BCBCC = list(G.bc)
t = time.process_time()
G = brandes.Graphs(edges)
G.brandes()
print("standard Brandes takes " + str(time.process_time() - t) + " seconds to complete")
results_of_brandes = list(G.bc)
for i in range(n):
    if results_of_BCBCC[i] != results_of_brandes[i]:
        print(":(")
        print("Vertex: " + str(i))
        print("Result of BCBCC: " + str(results_of_BCBCC[i]))
        print("Result of Brandes: " + str(results_of_brandes[i]))
        print("Articulation point? " + str(G.isArticulationPoint(i)))
print("Number of articulation points: " + str(len(G.articulation_points)))

