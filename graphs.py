from collections import deque


class Graphs:
    def __init__(self, edges):
        n = len(edges)
        self.n = n
        self.edges = edges
        # Calculated with Brandes/BCBCC:
        self.bc = [0] * n

        # Calculated in dfs:
        self.time = 0  # counter for dfs
        self.d = [-1] * n  # d[vertex] = time discovered
        self.pi = [-1] * n  # parent in dfs tree
        self.dfs_completed = False

        # Calculated in findArticulationPoints:
        self.dToVertex = [-1] * n  # d[time discovered] = vertex
        self.highest = [-1] * n  # Used for finding articulation points
        self.articulationPoints = []
        self.find_articulationpoints_completed = False

        # Calculated in constructBlocks:
        self.blockOfU = [0] * n  # Keeps track of which biconnected component a vertex belongs to. Articulation points
        # belong too multiple components and use lists. For example, if edges == [[1], [0, 2], [1]],
        # then Graphs(edges).block == [0, [0, 1], 1]
        self.componentCount = 0
        self.blockContains = []
        self.blockAPCount = []
        self.indexInBlock = [0] * n
        self.indexAPInBlock = {}
        self.construct_blocks_completed = False

        # Calculated in constructWeightedBlockTree
        self.D_B = {}
        self.construct_weighted_block_tree_completed = False

    # Main functions

    def brandes(self):
        n = self.n
        V = [x for x in range(n)]
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

    def BCBCC(self):
        self.constructWeightedBlockTree()
        for u in self.articulationPoints:
            # self.bc[u] = len(self.blockOfU[u]) - 1
            for B in self.blockOfU[u]:
                self.bc[u] += self.D_B[(B, u)] * (self.n - self.D_B[(B, u)] - 1)
        for B in range(self.componentCount):
            h = self.computeTrafficMatrix(B)
            self.brandesForBCBCC(B, h)
        return

    def alternativeBrandes(self, start=0):
        count = self.componentCount
        AP_in_block = [[] for x in range(count)]
        for u in self.articulationPoints:
            for B in self.blockOfU[u]:
                AP_in_block[B].append(u)
        discovered = [False] * count
        discovered[start] = True
        processed = [False] * count
        vertices_processed = len(self.blockContains[start])
        S = [(start, None)]
        while len(S) > 0:
            pair = S.pop()
            B = S[0]
            u = S[1]
            self.brandes(B, u)
            if u is not None:
                self.one_start_brandes(B, u, processed)



    # Functions needed to perform BCBCC

    def dfs(self, u, resetTime=False):  # see Introduction to Algorithms page 621
        if self.dfs_completed:
            return
        if resetTime:
            self.time = 0
        self.d[u] = self.time
        for v in self.edges[u]:
            if self.d[v] == -1:
                self.time += 1
                self.dfs(v)
                self.pi[v] = u
        if resetTime:
            self.dfs_completed = True
        return

    def findArticulationPoints(self, start=0):
        if self.find_articulationpoints_completed:
            return
        n = self.n
        counter = n
        self.dfs(start, True)
        self.highest = list(self.d)
        for u in range(n):
            self.dToVertex[self.d[u]] = u
        while counter > 0:
            counter -= 1
            u = self.dToVertex[counter]
            for v in self.edges[u]:
                if v == self.pi[u]:  # v is parent in dfs tree
                    pass
                elif self.d[v] < self.d[u]:  # backedge
                    if self.d[v] < self.highest[u]:
                        self.highest[u] = self.d[v]
                else:  # child
                    if self.highest[v] < self.highest[u]:
                        self.highest[u] = self.highest[v]
        u = start
        children = 0
        for v in self.edges[u]:
            if u == self.pi[v]:
                children += 1
        if children > 1:
            self.articulationPoints.append(u)
            self.blockOfU[u] = []
        for i in range(1, n):
            u = self.dToVertex[i]
            for v in self.edges[u]:
                if u == self.pi[v]:  # v is a child of u
                    if self.highest[v] >= i:  # This means u is an articulation point
                        if not self.isArticulationPoint(u):
                            # This means it's the first time it's determined that u is an articulation point
                            self.articulationPoints.append(u)
                            self.blockOfU[u] = []
        self.find_articulationpoints_completed = True
        return

    def constructBlocks(self, start=0):
        if self.construct_blocks_completed:
            return
        self.findArticulationPoints(start)
        n = self.n
        if not self.isArticulationPoint(start):
            self.addNewComponent(start)
        for i in range(1, n):
            u = self.dToVertex[i]
            parent = self.pi[u]
            j = self.d[parent]
            if self.isArticulationPoint(parent):
                if self.highest[u] >= j or j == 0:
                    self.blockOfU[parent].append(self.componentCount)
                    self.addNewComponent(u)
                else:
                    self.assignComponent(u, self.blockOfU[parent][0])
            else:
                self.assignComponent(u, self.blockOfU[parent])
        for u in range(n):
            if isinstance(self.blockOfU[u], int):
                self.blockContains[self.blockOfU[u]].append(u)
            else:
                for i in self.blockOfU[u]:
                    self.blockContains[i].append(u)
                    self.blockAPCount[i] += 1
        for B in range(self.componentCount):
            for i in range(len(self.blockContains[B])):
                u = self.blockContains[B][i]
                if self.isArticulationPoint(u):
                    self.indexAPInBlock[(B, u)] = i
                else:
                    self.indexInBlock[u] = i
        self.construct_blocks_completed = True
        return

    def constructWeightedBlockTree(self):
        # See Algorithm 1 in Heuristics for Speeding up Betweenness Centrality Computation
        if self.construct_weighted_block_tree_completed:
            return
        self.constructBlocks()
        treeEdgesBlockToAP = [[] for x in range(self.componentCount)]
        unknownNeighboursOfAP = {}
        unknownNeighboursOfBlock = [0] * self.componentCount
        for u in self.articulationPoints:
            unknownNeighboursOfAP[u] = len(self.blockOfU[u])
            for B in self.blockOfU[u]:
                treeEdgesBlockToAP[B].append(u)
                self.D_B[(B, u)] = -1
        Q = deque()
        for B in range(self.componentCount):
            unknownNeighboursOfBlock[B] = self.blockAPCount[B]
            if unknownNeighboursOfBlock[B] == 1:
                Q.append((B, treeEdgesBlockToAP[B][0], True))
        while len(Q) > 0:
            triple = Q.popleft()
            if triple[2]:  # Pair is of the form (B, v)
                B = triple[0]
                u = triple[1]
                if self.D_B[(B, u)] == -1:
                    size = len(self.blockContains[B]) - 1
                    for v in treeEdgesBlockToAP[B]:
                        if self.D_B[(B, v)] != -1:
                            size += self.n - self.D_B[(B, v)] - 1
                    self.D_B[(B, u)] = size
                    unknownNeighboursOfAP[u] -= 1
                    if unknownNeighboursOfAP[u] == 1:
                        for C in self.blockOfU[u]:
                            if self.D_B[(C, u)] == -1:
                                Q.append((u, C, False))
                                break
            else:
                B = triple[1]
                u = triple[0]
                if self.D_B[(B, u)] == -1:
                    size = 1
                    for C in self.blockOfU[u]:
                        if self.D_B[(C, u)] != -1:
                            size += self.D_B[(C, u)]
                    self.D_B[(B, u)] = self.n - size
                    unknownNeighboursOfBlock[B] -= 1
                    if unknownNeighboursOfBlock[B] == 1:
                        for v in treeEdgesBlockToAP[B]:
                            if self.D_B[(B, v)] == -1:
                                Q.append((B, v, True))
                                break
        self.construct_weighted_block_tree_completed = True
        return

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

    def brandesForBCBCC(self, B, h):
        n = len(self.blockContains[B])
        V = [x for x in range(n)]
        # previously calculated bc values are NOT overwritten.
        for s in V:
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
            while len(S) > 0:
                j = S.pop()
                for i in P[j]:
                    delta[i] += (sigma[i] / sigma[j]) * (h[s][j] + delta[j])
                if j != s:
                    w = self.blockContains[B][j]
                    self.bc[w] += delta[j]
        return

    # Utility functions

    def isArticulationPoint(self, u):
        return isinstance(self.blockOfU[u], list)

    def isInBlock(self, u, B):
        if self.isArticulationPoint(u):
            return B in self.blockOfU[u]
        else:
            return B == self.blockOfU[u]

    def findIndex(self, u, B):
        if self.isArticulationPoint(u):
            return self.indexAPInBlock[(B, u)]
        else:
            return self.indexInBlock[u]

    def addNewComponent(self, u):
        if self.isArticulationPoint(u):
            self.blockOfU[u].append(self.componentCount)
        else:
            self.blockOfU[u] = self.componentCount
        self.blockContains.append([])
        self.blockAPCount.append(0)
        self.componentCount += 1
        return

    def assignComponent(self, u, component):
        if self.isArticulationPoint(u):
            self.blockOfU[u].append(component)
        else:
            self.blockOfU[u] = component
        return

    def is_connected(self):
        self.dfs(0)
        if self.n - self.time == 1:
            return True
        return False

    def is_undirected(self):
        for u in range(self.n):
            for v in self.edges[u]:
                if u not in self.edges[v]:
                    return False
        return True