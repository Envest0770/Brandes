import graphs

edges1 = [[0, 1], [1, 2], [1]]
edges2 = [[0], [0, 1, 2], [1]]
G = graphs.connectTree(edges1, edges2)
print(G.edges)

"""
def connectTree(edges1, edges2):
    length = len(edges1)
    for u in range(length):
        for i in range(len(edges1[u])):
            edges1[u][i] += length
    edges1 += edges2
    return Graphs(edges1)

"""


"""
n = self.n
counter = n
self.dfs(start, True)
highest = self.d.copy()
dToVertex = [0] * n  # Avoids O(n) searches later
for u in range(n):
    dToVertex[self.d[u]] = u
while counter > 0:
    counter -= 1
    u = dToVertex[counter]
    for v in self.edges[u]:
        if v == self.pi[u]:  # v is parent in dfs tree
            pass
        elif self.d[v] < self.d[u]:  # backedge
            if self.d[v] < highest[u]:
                highest[u] = self.d[v]
        else:  # child
            if highest[v] < highest[u]:
                highest[u] = highest[v]
u = dToVertex[0]
children = 0
for v in self.edges[u]:
    if u == self.pi[v]:
        children += 1
if children > 1:
    self.articulationPoints.append(u)
    self.blockOfU[u] = []
else:
    self.addComponent(u)
for i in range(1, n):
    u = dToVertex[i]
    for v in self.edges[u]:
        if u == self.pi[v]:  # v is a child of u
            if highest[v] >= i:  # This means u is an articulation point
                if not self.isArticulationPoint(u):
                    # This means it's the first time it's determined that u is an articulation point
                    self.blockOfU[u] = []
                    self.articulationPoints.append(u)
"""
