from collections import deque


def connectTree(edges1, edges2):
    length = len(edges1)
    for u in range(length):
        for i in range(len(edges1[u])):
            edges1[u][i] += length
    edges1 += edges2
    return Graphs(edges1)


class Graphs:
    def __init__(self, edges):
        n = len(edges)
        self.n = n
        # self.m
        self.edges = edges
        self.bc = [0] * n
        self.time = 0  # counter for dfs
        self.d = [-1] * n  # time vertex discovered
        self.pi = [-1] * n  # parent in dfs tree
        self.articulationPoints = []
        self.blockOfU = [0] * n  # Keeps track of which biconnected component a vertex belongs to. Articulation points
        # belong too multiple components and use lists. For example, if edges == {0: [1], 1: [0, 2], 2: [1]},
        # Graphs(3,2,edges).block == [0, [0, 2], 2]
        self.componentCount = 0
        self.blockContains = [[]]
        self.blockAPCount = [0]
        self.D_B = {}

    def brandes(self):
        n = self.n
        V = [x for x in range(n)]
        self.bc = [0] * n  # previously calculated bc values are overwritten.
        for s in V:
            S = []
            P = [[] for i in range(n)]
            sigma = [0] * n
            sigma[s] = 1
            d = [-1] * n
            d[s] = 0
            Q = deque([s])
            while len(Q) > 0:
                v = Q.popleft()
                S.append(v)
                for w in self.edges[v]:
                    if d[w] < 0:
                        Q.append(w)
                        d[w] = d[v] + 1
                    if d[w] == d[v] + 1:  # v is a predecessor of w on a shortest path from s to w
                        sigma[w] += sigma[v]
                        P[w].append(v)
            delta = [0] * n
            while len(S) > 0:
                w = S.pop()
                for v in P[w]:
                    delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w])
                if w != s:
                    self.bc[w] += delta[w]
        return

    def dfs(self, u, resetTime=False):  # see Introduction to Algorithms page 621
        if resetTime:
            self.time = 0
        self.d[u] = self.time
        for v in self.edges[u]:
            if self.d[v] == -1:
                self.time += 1
                self.dfs(v)
                self.pi[v] = u
        return

    def findArticulationPoints(self, start=0):
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
        for i in range(1, n):
            u = dToVertex[i]
            for v in self.edges[u]:
                if u == self.pi[v]:
                    if highest[v] >= i:
                        self.articulationPoints.append(u)
        return

    def addComponent(self, u):
        self.componentCount += 1
        if isinstance(self.blockOfU[u], int):
            self.blockOfU[u] = self.componentCount
        else:
            self.blockOfU[u].append(self.componentCount)
        self.blockContains.append([])
        self.blockAPCount.append(0)

    def constructBlocks(self, start=0):
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
                        if isinstance(self.blockOfU[u], int):
                            # This means it's the first time it's determined that u is an articulation point
                            self.blockOfU[u] = []
                            self.articulationPoints.append(u)
            parent = self.pi[u]
            if isinstance(self.blockOfU[u], int):
                if isinstance(self.blockOfU[parent], int):
                    self.blockOfU[u] = self.blockOfU[parent]
                elif highest[u] == highest[parent] and highest[u] != parent and parent != dToVertex[0]:
                    self.blockOfU[u] = self.blockOfU[parent][0]
                else:
                    self.addComponent(u)
                    self.blockOfU[parent].append(self.componentCount)
            else:
                if isinstance(self.blockOfU[parent], int):
                    self.blockOfU[u].append(self.blockOfU[parent])
                elif highest[u] == highest[parent] and highest[u] != parent and parent != dToVertex[0]:
                    self.blockOfU[u].append(self.blockOfU[parent][0])
                else:
                    self.addComponent(u)
                    self.blockOfU[parent].append(self.componentCount)
        for u in range(n):
            if isinstance(self.blockOfU[u], int):
                self.blockContains[self.blockOfU[u]].append(u)
            else:
                for i in self.blockOfU[u]:
                    self.blockContains[i].append(u)
                    self.blockAPCount[i] += 1
        return

    def constructWeightedBlockTree(self):
        # See Algorithm 1 in Heuristics for Speeding up Betweenness Centrality Computation
        self.constructBlocks()
        treeEdgesBlockToAP = [[] for i in range(self.componentCount)]
        treeEdgesAPToBlock = [[] for i in range(len(self.articulationPoints))]
        self.D_B = {}
        for u in range(len(self.articulationPoints)):
            for i in self.blockOfU[self.articulationPoints[u]]:
                treeEdgesAPToBlock[u].append(i)
                if i in treeEdgesBlockToAP:
                    treeEdgesBlockToAP[i].append(u)
                self.D_B[(i, u)] = -1
        Q = deque()
        for i in range(self.componentCount):
            if self.blockAPCount[i] == 1:
                Q.append((i, treeEdgesBlockToAP[i][0], True))
        while len(Q) > 0:
            pair = Q.pop()
            if pair[2]:  # Pair is of the form (B, v)
                B = pair[0]
                u = pair[1]
                size = len(self.blockContains[B]) - 1
                for v in treeEdgesBlockToAP[B]:
                    if self.D_B[(B, v)] != -1:
                        size += self.n - self.D_B[(B, v)]
                self.D_B[(B, u)] = size
                for i in treeEdgesAPToBlock[u]:
                    if self.D_B[(i, u)] == -1:
                        Q.append((u, i, False))
                        break  # TODO: check if really needed
            else:
                B = pair[1]
                u = pair[0]
                size = 1
                for i in treeEdgesAPToBlock[u]:
                    if self.D_B[(i, u)] != -1:
                        size += self.D_B[(i, u)]
                self.D_B[(B, u)] = self.n - 1 - size
                for v in treeEdgesBlockToAP[B]:
                    if self.D_B[[B, v]] == -1:
                        Q.append((B, v))
                        break
        return connectTree(treeEdgesAPToBlock, treeEdgesBlockToAP)

    def computeTrafficMatrix(self, B):
        length = len(self.blockContains[B])
        h = []
        for i in range(1, length):
            h += [1] * i
        for i in range(length):
            for j in range(len(h[i])):
                u = self.blockContains[B][i]
                v = self.blockContains[B][j]
                if isinstance(self.blockOfU[u], int):
                    if isinstance(self.blockOfU[v], int):
                        pass
                    else:
                        h[i][j] = self.n - self.D_B[(B, v)]
                else:
                    if isinstance(self.blockOfU[v], int):
                        h[i][j] = self.n - self.D_B[(B, u)]
                    else:
                        h[i][j] = (self.n - self.D_B[(B, u)]) * (self.n - self.D_B[(B, v)])
        return h

    def BCBCC(self):
        self.bc = self.bc = [0] * self.n
        T = self.constructWeightedBlockTree()
        for u in self.articulationPoints:
            self.bc[u] = len(self.blockOfU[u]) - 1
            for B in self.blockOfU[u]:
                self.bc[u] += self.D_B[(B, u)] * (self.n - self.D_B[(B, u)] - 1)
        for B in range(self.componentCount):
            h = self.computeTrafficMatrix(B)
            E_B = [[] for i in range(len(self.blockContains[B]))]
            for i in range(len(self.blockContains[B])):
                u = self.blockContains[B][i]
                for v in self.edges:
                    0
        return
