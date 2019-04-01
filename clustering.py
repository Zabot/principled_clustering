#!/usr/bin/env python2

import collections 
import math
import random
import sys

try:
    edge_filepath = sys.argv[1]
    cluster_count = int(sys.argv[2])
except IndexError as e:
    print("Usage: {} edge_file cluster_count".format(sys.argv[0]))
    sys.exit(1)

# Read edge list where each line contains the two endpoints of an edge
# seperated by a space
edges = []
with open(edge_filepath, "r") as edge_file:
    for line in edge_file:
        if line.strip():
            edges.append(tuple(map(int, line.strip().split(" "))))

clusters = range(cluster_count)
nodes = set([i for edge in edges for i in edge])

# Do the actual clustering
k = collections.defaultdict(lambda: collections.defaultdict(lambda: random.random()))
for n in range(1, 100):
    kappa = collections.defaultdict(lambda: 0)
    k_prime = collections.defaultdict(lambda: collections.defaultdict(lambda: 0))
    for z in clusters:
        for i in nodes:
            kappa[z] += k[i][z]

    for i, j in edges:
        D = 0
        for z in clusters:
            D += (k[i][z] * k[j][z]) / kappa[z]

        for z in clusters:
            q = (k[i][z] * k[j][z]) / (D * kappa[z])
            k_prime[i][z] += q
            k_prime[j][z] += q
    k = k_prime

# Output per-node community membership
for i in nodes:
    expected_colors = k[i].items()
    expected_degree = sum(zip(*expected_colors)[1])
    membership = map(lambda x: (x[0], 100*x[1]/expected_degree), expected_colors)
    
    print("{}:\t{}".format(i, "\t".join(["{}: {:0.2f}%".format(cluster, weight) for cluster, weight in membership])))

