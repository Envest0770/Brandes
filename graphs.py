from collections import deque


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
                    if d[w] == d[v] + 1:
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
        treeEdges = {}
        D_B = {}
        for u in self.articulationPoints:
            treeEdges[u] = []
            for i in self.blockOfU[u]:
                treeEdges[u].append(-i)  # Avoids overlap between articulation points and blocks
                if -i in treeEdges:
                    treeEdges[-i].append(u)
                else:
                    treeEdges[-i] = [u]
                D_B[[-i, u]] = -1
        Q = deque()
        for i in range(self.componentCount):
            if self.blockAPCount[i] == 1:
               Q.append([-i, treeEdges[-i][0]])
        while len(Q) > 0:
            pair = Q.pop()
            if pair[0] < 0:  # Pair is of the form (B, v)
                B = -pair[0]
                u = pair[1]
                size = len(self.blockContains[B]) - 1
                for v in treeEdges[-B]:
                    if D_B[[-B, v]] != -1:
                        size += self.n - D_B[[-B, v]]
                D_B[[-B, u]] = size
                for j in treeEdges[u]:
                    if D_B[[j, u]] == -1:
                        Q.append([u, j])
                        break  # TODO: check if really needed
            else:
                B = -pair[1]
                u = pair[0]
                size = 1
                for j in treeEdges[u]:
                    if D_B[[j, u]] != -1:
                        size += D_B[[j, u]]
                D_B[[-B, u]] = self.n - 1 - size
                for v in treeEdges[-B]:
                    if D_B[[-B, v]] == -1:
                        Q.append([-B, v])
                        break
        return Graphs(treeEdges)
