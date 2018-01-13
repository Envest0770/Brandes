import brandes
import time
import sys

sys.setrecursionlimit(20000)
string = "as-caida/as-caida20040105.txt"
file = open(string)
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
        if u not in edges[v]:  # This turns the directed graph into an undirected graph
            edges[v].append(u)
            edges[u].append(v)
            m += 1
G = brandes.Graphs(edges)
n = G.n
print("Name of graph: " + string[0: len(string) - 4])
print("Number of vertices: " + str(n))
print("Number of edges: " + str(m))
print("Graph is connected? " + str(G.is_connected()))
print("Graph is undirected? " + str(G.is_undirected()))
t = time.process_time()
G.BCBCC()
print("Number of articulation points: " + str(len(G.articulation_points)))
print("Number of biconnected components: " + str(G.component_count))
print("BCBCC takes " + str(time.process_time() - t) + " seconds to complete")
results_of_BCBCC = list(G.bc)
n_max = 0
m_max = 0
largest_component = -1
for B in range(G.component_count):
    if len(G.component_contains[B]) > n_max:
        n_max = len(G.component_contains[B])
        largest_component = B
B = largest_component
for i in range(n_max):
    u = G.component_contains[B][i]
    if G.isArticulationPoint(u):
        for v in G.edges[u]:
            if G.isInBlock(v, B):
                m_max += 1
    else:
        for v in G.edges[u]:
            m_max += 1
m_max /= 2
print("The component with the largest number of vertices contains " + str(n_max) + " vertices and " +
      str(m_max) + " edges")
G = brandes.Graphs(edges)
t = time.process_time()
G.brandes()
print("standard Brandes takes " + str(time.process_time() - t) + " seconds to complete")
results_of_brandes = list(G.bc)
for i in range(n):
    if results_of_BCBCC[i] - results_of_brandes[i] > 0.000001:
        print("The values for the two betweennness centrality methods do not overlap")
        print("Vertex: " + str(i))
        print("Result of BCBCC: " + str(results_of_BCBCC[i]))
        print("Result of Brandes: " + str(results_of_brandes[i]))
        print("Articulation point? " + str(G.isArticulationPoint(i)))
