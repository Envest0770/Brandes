from collections import deque
import time


class Graphs:
    def __init__(self, edges):
        n = len(edges)
        self.n = n
        self.edges = edges
        # Calculated in Brandes/BCBCC/:
        self.bc = [0] * n

        # Calculated in dfs:
        self.time = 0  # counter for dfs
        self.g = [-1] * n  # g[vertex] = time discovered
        self.parent = [-1] * n  # parent in dfs tree
        self.dfs_completed = False

        # Calculated in findArticulationPoints:
        self.g_inverse = [-1] * n  # d[time discovered] = vertex
        self.h = [-1] * n  # Used for finding articulation points
        self.articulation_points = []
        self.find_articulationpoints_completed = False

        # Calculated in constructBlocks:
        self.component_of_u = [
                                  0] * n  # Keeps track of which biconnected component a vertex belongs to. Articulation points
        # belong too multiple components and use lists. For example, if edges == [[1], [0, 2], [1]],
        # then Graphs(edges).component_of_u == [0, [0, 1], 1]
        self.component_count = 0
        self.component_contains = []
        self.component_AP_count = []
        self.index_in_component = [0] * n  # Can't be used for articulation points
        self.index_AP_in_component = {}
        self.construct_blocks_completed = False

        # Calculated in constructWeightedBlockTree
        self.c = {}
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
        for u in self.articulation_points:
            for B in self.component_of_u[u]:
                self.bc[u] += self.c[(B, u)] * (self.n - self.c[(B, u)] - 1)
        for B in range(self.component_count):
            # h = self.computeTrafficMatrix(B)
            h = self.compute_tau(B)
            self.brandesForBCBCC(B, h)
        return

    # Functions needed to perform BCBCC

    def dfs(self, u, resetTime=False):  # see Introduction to Algorithms page 621
        if self.dfs_completed:
            return
        if resetTime:
            self.time = 0
        self.g[u] = self.time
        for v in self.edges[u]:
            if self.g[v] == -1:
                self.time += 1
                self.dfs(v)
                self.parent[v] = u
        if resetTime:
            self.dfs_completed = True
        return

    def findArticulationPoints(self, start=0):
        if self.find_articulationpoints_completed:
            return
        n = self.n
        counter = n
        self.dfs(start, True)
        self.h = list(self.g)
        for u in range(n):
            self.g_inverse[self.g[u]] = u
        while counter > 0:
            counter -= 1
            u = self.g_inverse[counter]
            for v in self.edges[u]:
                if v == self.parent[u]:  # v is parent in dfs tree
                    pass
                elif self.g[v] < self.g[u]:  # backedge
                    if self.g[v] < self.h[u]:
                        self.h[u] = self.g[v]
                else:  # child
                    if self.h[v] < self.h[u]:
                        self.h[u] = self.h[v]
        u = start
        children = 0
        for v in self.edges[u]:
            if u == self.parent[v]:
                children += 1
        if children > 1:
            self.articulation_points.append(u)
            self.component_of_u[u] = []
        for i in range(1, n):
            u = self.g_inverse[i]
            for v in self.edges[u]:
                if u == self.parent[v]:  # v is a child of u
                    if self.h[v] >= i:  # This means u is an articulation point
                        if not self.isArticulationPoint(u):
                            # This means it's the first time it's determined that u is an articulation point
                            self.articulation_points.append(u)
                            self.component_of_u[u] = []
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
            u = self.g_inverse[i]
            parent = self.parent[u]
            j = self.g[parent]
            if self.isArticulationPoint(parent):
                if self.h[u] >= j or j == 0:
                    self.component_of_u[parent].append(self.component_count)
                    self.addNewComponent(u)
                else:
                    self.assignComponent(u, self.component_of_u[parent][0])
            else:
                self.assignComponent(u, self.component_of_u[parent])
        for u in range(n):
            if isinstance(self.component_of_u[u], int):
                self.component_contains[self.component_of_u[u]].append(u)
            else:
                for i in self.component_of_u[u]:
                    self.component_contains[i].append(u)
                    self.component_AP_count[i] += 1
        for B in range(self.component_count):
            for i in range(len(self.component_contains[B])):
                u = self.component_contains[B][i]
                if self.isArticulationPoint(u):
                    self.index_AP_in_component[(B, u)] = i
                else:
                    self.index_in_component[u] = i
        self.construct_blocks_completed = True
        return

    def constructWeightedBlockTree(self):
        # See Algorithm 1 in Heuristics for Speeding up Betweenness Centrality Computation
        if self.construct_weighted_block_tree_completed:
            return
        self.constructBlocks()
        treeEdgesBlockToAP = [[] for x in range(self.component_count)]
        unknownNeighboursOfAP = {}
        unknownNeighboursOfBlock = [0] * self.component_count
        for u in self.articulation_points:
            unknownNeighboursOfAP[u] = len(self.component_of_u[u])
            for B in self.component_of_u[u]:
                treeEdgesBlockToAP[B].append(u)
                self.c[(B, u)] = -1
        Q = deque()
        for B in range(self.component_count):
            unknownNeighboursOfBlock[B] = self.component_AP_count[B]
            if unknownNeighboursOfBlock[B] == 1:
                Q.append((B, treeEdgesBlockToAP[B][0], True))
        while len(Q) > 0:
            triple = Q.popleft()
            if triple[2]:  # Pair is of the form (B, v)
                B = triple[0]
                u = triple[1]
                if self.c[(B, u)] == -1:
                    size = len(self.component_contains[B]) - 1
                    for v in treeEdgesBlockToAP[B]:
                        if self.c[(B, v)] != -1:
                            size += self.n - self.c[(B, v)] - 1
                    self.c[(B, u)] = size
                    unknownNeighboursOfAP[u] -= 1
                    if unknownNeighboursOfAP[u] == 1:
                        for C in self.component_of_u[u]:
                            if self.c[(C, u)] == -1:
                                Q.append((u, C, False))
                                break
            else:
                B = triple[1]
                u = triple[0]
                if self.c[(B, u)] == -1:
                    size = 1
                    for C in self.component_of_u[u]:
                        if self.c[(C, u)] != -1:
                            size += self.c[(C, u)]
                    self.c[(B, u)] = self.n - size
                    unknownNeighboursOfBlock[B] -= 1
                    if unknownNeighboursOfBlock[B] == 1:
                        for v in treeEdgesBlockToAP[B]:
                            if self.c[(B, v)] == -1:
                                Q.append((B, v, True))
                                break
        self.construct_weighted_block_tree_completed = True
        return

    def compute_tau(self, B):
        length = len(self.component_contains[B])
        h = [1] * length
        for i in range(length):
            u = self.component_contains[B][i]
            if self.isArticulationPoint(u):
                h[i] = self.n - self.c[(B, u)]
        return h

    def brandesForBCBCC(self, B, h):
        n = len(self.component_contains[B])
        V = [x for x in range(n)]
        edges = [[] for x in range(n)]
        bc = [0] * n
        for i in range(n):
            u = self.component_contains[B][i]
            if self.isArticulationPoint(u):
                for v in self.edges[u]:
                    if self.isInBlock(v, B):
                        j = self.findIndex(v, B)
                        edges[i].append(j)
            else:
                for v in self.edges[u]:
                    j = self.findIndex(v, B)
                    edges[i].append(j)
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
                S.append(i)
                for j in edges[i]:
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
                    delta[i] += (sigma[i] / sigma[j]) * (h[j] + delta[j])
                if j != s:
                    bc[j] += h[s] * delta[j]
        for i in range(n):
            u = self.component_contains[B][i]
            self.bc[u] += bc[i]
        return

    # Utility functions

    def isArticulationPoint(self, u):
        return isinstance(self.component_of_u[u], list)

    def isInBlock(self, u, B):
        if self.isArticulationPoint(u):
            return B in self.component_of_u[u]
        else:
            return B == self.component_of_u[u]

    def findIndex(self, u, B):
        if self.isArticulationPoint(u):
            return self.index_AP_in_component[(B, u)]
        else:
            return self.index_in_component[u]

    def addNewComponent(self, u):
        if self.isArticulationPoint(u):
            self.component_of_u[u].append(self.component_count)
        else:
            self.component_of_u[u] = self.component_count
        self.component_contains.append([])
        self.component_AP_count.append(0)
        self.component_count += 1
        return

    def assignComponent(self, u, component):
        if self.isArticulationPoint(u):
            self.component_of_u[u].append(component)
        else:
            self.component_of_u[u] = component
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
