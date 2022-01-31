from matplotlib import pyplot as plt
import networkx as nx
import random as rnd
import math

# Adjust the variables below to simulate [simulations] amount of networks with [nodes] density (nodes/km2)
# where each node has a transmission range of [transmissionRange].
nodes = 2000 
transmissionRange = 25
simulations = 100

# List of results (maximum clique in each simulation)
cliques = []

# Generate a Graph G with all the nodes
G = nx.Graph()

for sim in range(simulations):
    G.clear()
    G.add_nodes_from(list(range(nodes)))

    # Generate x-coordinates and y-coordinates for all the nodes
    x_coords = [rnd.randint(0, 999) for i in range(nodes)]
    y_coords = [rnd.randint(0, 999) for i in range(nodes)]
    # print(x_coords)
    # print(y_coords)

    # Check which combination of nodes are within each other's transmission range. Create an edge between them if true.
    for nodeA in range(nodes):
        # nx.set_node_attributes(G, nodeA, (x_coords[nodeA], y_coords[nodeA])) [can I set coordinates to each node?]
        for nodeB in range(nodeA + 1, nodes):
            # print("compare node " + str(nodeA) + " with node " + str(nodeB))
            nodeA_x = x_coords[nodeA]
            nodeA_y = y_coords[nodeA]
            nodeB_x = x_coords[nodeB]
            nodeB_y = y_coords[nodeB]
            distance_x = min(max(nodeA_x, nodeB_x) - min(nodeA_x, nodeB_x), 1000-(max(nodeA_x, nodeB_x) - min(nodeA_x, nodeB_x)))
            # print(distance_x)
            distance_y = min(max(nodeA_y, nodeB_y) - min(nodeA_y, nodeB_y), 1000-(max(nodeA_y, nodeB_y) - min(nodeA_y, nodeB_y)))
            # print(distance_y)
            distanceAB = math.sqrt(distance_x ** 2 + distance_y ** 2)
            if distanceAB <= transmissionRange:
                G.add_edge(nodeA, nodeB)

    maxClique = nx.algorithms.approximation.clique.large_clique_size(G)
    print("Simulation: " + str(sim) + ". Max clique: " + str(maxClique))
    cliques.append(maxClique)
    #nx.draw(G)
    #plt.show()

for i in range(min(cliques),max(cliques)+1):
    print("A max clique of " + str(i) + " occurred " + str(cliques.count(i)) + " times.")
