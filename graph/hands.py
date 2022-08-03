import sys
sys.path.insert(0, '')
sys.path.extend(['../'])

import numpy as np

from graph import tools

# Joint index:
# {0,  "WRIST"}
# {1,  "THUMB_CMC"},
# {2,  "THUMB_MCP"},
# {3,  "THUMB_IP"},
# {4,  "THUMB_TIP"},
# {5,  "INDEX_FINGER_MCP"},
# {6,  "INDEX_FINGER_PIP"},
# {7,  "INDEX_FINGER_DIP"},
# {8,  "INDEX_FINGER_TIP"},
# {9,  "MIDDLE_FINGER_MCP"},
# {10, "MIDDLE_FINGER_PIP"},
# {11, "MIDDLE_FINGER_DIP"},
# {12, "MIDDLE_FINGER_TIP"},
# {13, "RING_FINGER_MCP"},
# {14, "RING_FINGER_PIP"},
# {15, "RING_FINGER_DIP"},
# {16, "RING_FINGER_TIP"},
# {17, "PINKY_MCP"},
# {18, "PINKY_PIP"},
# {19, "PINKY_DIP"},
# {20, "PINKY_TIP"}

num_node = 21
self_link = [(i, i) for i in range(num_node)]
inward = [(1, 0), (2, 1), (3, 2), (4, 3), (5, 0), (6, 5), (7, 6), (8, 7),
          (9, 0), (10, 9), (11, 10), (12, 11), (13, 0), (14, 13), (15, 14), (16, 15),
          (17, 0), (18, 17), (19, 18), (20, 19)]
outward = [(j, i) for (i, j) in inward]
neighbor = inward + outward


class AdjMatrixGraph:
    def __init__(self, *args, **kwargs):
        self.num_nodes = num_node
        self.edges = neighbor
        self.self_loops = [(i, i) for i in range(self.num_nodes)]
        self.A_binary = tools.get_adjacency_matrix(self.edges, self.num_nodes)
        self.A_binary_with_I = tools.get_adjacency_matrix(self.edges + self.self_loops, self.num_nodes)


if __name__ == '__main__':
    graph = AdjMatrixGraph()
    A_binary = graph.A_binary
    import matplotlib.pyplot as plt
    print(A_binary)
    plt.matshow(A_binary)
    plt.show()
