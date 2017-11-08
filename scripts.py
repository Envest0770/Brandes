from collections import deque
import graphs

n = 11
m = 13
edges = {0: [1, 4], 1: [0, 2], 2: [1, 3, 5], 3: [2, 6], 4: [0, 5], 5: [2, 4, 6, 9], 6: [3, 5, 7], 7: [6], 8: [9],
         9: [5, 8, 10], 10: [9]}
G = graphs.Graphs(edges)
# G.findArticulationPoints()
# for u in G.articulationPoints:
#     print(u)
# G.constructBlocks()

for i in G.blockContains:
    print('component: '+ str(i))
T = G.constructWeightedBlockTree()