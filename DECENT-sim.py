'''
The function Optimal_Threshold estimates the maximum clique present within 95% of simulated random networks. This
maximum clique is a parameter important to the DECENT key management scheme since it relies on executing key management
functions in a decentralized manner. One key management function, the distributed share updating protocol, requires a
threshold of nodes to be within each other's transmission range. Thus, this function simulates random networks and,
given a particular node density (in nodes/km^2) and transmission range (in meters), determines the largest set of nodes
which are all within each other's transmission range such that a threshold matching this 'clique' ensures that there
exists a set of nodes within the network that can execute the distributed share updating protocol.

The current implementation allows the visualization of these random networks using the matplotlib library and estimates
an approximation of the maximum clique using a networkx library function. Since determining the maximum clique is a
computationally complex problem, the program may run relatively long for particular inputs. Future updates will attempt
to improve the performance and/or incorporate a progress bar such that the user can track the progress of the program.

This algorithm is covered and featured in the published research paper below:
M. de Ree et al., "DECENT: Decentralized and Efficient Key Management to Secure Communication in Dense and Dynamic
Environments," IEEE Transactions on Intelligent Transportation Systems, vol. 24, no. 7, pp. 7586-7598, 2022. [DOI:
10.1109/TITS.2022.3160068]
'''


def Optimal_Threshold(node_density, transmission_range):
    # The matplotlib library can visualize the randomly generated networks.
    from matplotlib import pyplot as plt
    import networkx as nx
    import random as rnd
    import math

    # Define the list containing the maximum clique for each simulation.
    cliques = []

    # Define G as a network graph.
    G = nx.Graph()

    simulations = 100
    for sim in range(simulations):
        G.clear()
        G.add_nodes_from(list(range(node_density)))

        # Generate random x-coordinates and y-coordinates for all the nodes within a unit area (i.e., km^2).
        x_coords = [rnd.randint(0, 999) for i in range(node_density)]
        y_coords = [rnd.randint(0, 999) for i in range(node_density)]

        # Check which nodes are within each other's transmission range. Create an edge between them if true.
        for nodeA in range(node_density):
            # nx.set_node_attributes(G, nodeA, (x_coords[nodeA], y_coords[nodeA])) [can I set coordinates to each node?]
            for nodeB in range(nodeA + 1, node_density):
                nodeA_x = x_coords[nodeA]
                nodeA_y = y_coords[nodeA]
                nodeB_x = x_coords[nodeB]
                nodeB_y = y_coords[nodeB]
                distance_x = min(max(nodeA_x, nodeB_x) - min(nodeA_x, nodeB_x), \
                                 1000-(max(nodeA_x, nodeB_x) - min(nodeA_x, nodeB_x)))
                distance_y = min(max(nodeA_y, nodeB_y) - min(nodeA_y, nodeB_y), \
                                 1000-(max(nodeA_y, nodeB_y) - min(nodeA_y, nodeB_y)))
                distanceAB = math.sqrt(distance_x ** 2 + distance_y ** 2)
                if distanceAB <= transmission_range:
                    G.add_edge(nodeA, nodeB)

        maxClique = nx.algorithms.approximation.clique.large_clique_size(G)
        print("Simulation: " + str(sim) + ". Max clique: " + str(maxClique))
        cliques.append(maxClique)
        # nx.draw(G)
        # plt.show()

    key_management_service_availability = 1
    for i in range(min(cliques),max(cliques)+1):
        if (key_management_service_availability - (cliques.count(i) / simulations)) < 0.95:
            return i


# Example
print(Optimal_Threshold(node_density = 500, transmission_range = 25))