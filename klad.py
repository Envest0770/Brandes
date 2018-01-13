import brandes

edges1 = [[0, 1], [1, 2], [1]]
edges2 = [[0], [0, 1, 2], [1]]
G = brandes.connectTree(edges1, edges2)
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
T = ["gfgfgf"]
T[0].lower()


def alternativeBrandes(self, start=0):
    self.constructBlocks()
    count = self.componentCount
    n = self.n
    AP_in_block = [[] for x in range(count)]
    for u in self.articulationPoints:
        for B in self.blockOfU[u]:
            AP_in_block[B].append(u)
    discovered = [False] * count
    discovered[start] = True
    discovered_vertex = [False] * n
    vertex_to_index = [-1] * n
    index_to_vertex = [-1] * n
    edges = [[] for x in range(n)]
    processed_block = [False] * count
    depth = 0
    vertices_processed = 0
    S = [(start, None)]
    while len(S) > 0:
        pair = S.pop()
        B = pair[0]
        u = pair[1]
        vertices_discovered = vertices_processed
        for u in self.blockContains[B]:
            vertex_to_index[u] = vertices_discovered
            index_to_vertex[vertices_discovered] = u
            discovered_vertex[u] = True
            vertices_discovered += 1
        for i in range(vertices_processed, vertices_discovered):
            u = index_to_vertex[i]
            if self.isArticulationPoint(u):
                for v in self.edges[u]:
                    if self.isInBlock(v, B):
                        j = vertex_to_index[v]
                        edges[i].append(j)
            else:
                for v in self.edges[u]:
                    j = vertex_to_index[v]
                    edges[i].append(j)
        self.brandes_for_dfs(B, u, edges, vertices_processed)
        if u is not None:
            S = []
            P = [[] for x in range(n)]
            sigma = [0] * n
            sigma[s] = 1
            d = [-1] * n
            d[s] = 0
            Q = deque([s])
            while len(Q) > 0:
                i = Q.popleft()
                v = self.blockContains[B][i]
                S.append(i)
                for w in self.edges[v]:
                    if self.isInBlock(w, B):
                        j = self.findIndex(w, B)
                        if d[j] < 0:
                            Q.append(j)
                            d[j] = d[i] + 1
                        if d[j] == d[i] + 1:  # v is a predecessor of w on a shortest path from s to w
                            sigma[j] += sigma[i]
                            P[j].append(i)
            delta = [0] * n
            if ap == None:
                while len(S) > 0:
                    j = S.pop()
                    for i in P[j]:
                        delta[i] += (sigma[i] / sigma[j]) * (1 + delta[j])
                    if j != s:
                        w = self.blockContains[B][j]
                        self.bc[w] += delta[j]
            elif u == ap:
                while len(S) > 0:
                    j = S.pop()
                    for i in P[j]:
                        delta[i] += (sigma[i] / sigma[j]) * (1 + delta[j])
                    if j != s:
                        w = self.blockContains[B][j]
                        self.bc[w] += vertices_processed * delta[j]
            else:
                while len(S) > 0:
                    j = S.pop()
                    w = self.blockContains[B][j]
                    if w == ap:
                        for i in P[j]:
                            delta[i] += (sigma[i] / sigma[j]) * (vertices_processed + delta[j])
                        if j != s:
                            self.bc[w] += delta[j]
                    else:
                        for i in P[j]:
                            delta[i] += (sigma[i] / sigma[j]) * (1 + delta[j])
                        if j != s:
                            self.bc[w] += delta[j]

    """
    def computeTrafficMatrix(self, B):
        length = len(self.blockContains[B])
        h = [[1] * length for x in range(length)]
        for i in range(length):
            for j in range(i):
                u = self.blockContains[B][i]
                v = self.blockContains[B][j]
                if self.isArticulationPoint(u):
                    if self.isArticulationPoint(v):
                        h[i][j] = (self.n - self.D_B[(B, u)]) * (self.n - self.D_B[(B, v)])
                    else:
                        h[i][j] = self.n - self.D_B[(B, u)]
                else:
                    if self.isArticulationPoint(v):
                        h[i][j] = self.n - self.D_B[(B, v)]
                h[j][i] = h[i][j]
            h[i][i] = 0
        return h
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
