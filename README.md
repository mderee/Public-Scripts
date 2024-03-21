# Public-Scripts
This repository contains 3 Python scripts, related to my research in Applied Cryptography and Physical Layer Security. 

### 1. DECENT-sim.py.
This script contains the function "Optimal_Threshold". This function estimates the maximum clique present within 95% of simulated random networks. This
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

### 2. Security-vs-Leakage.py
This script contains the function "Bit_Security_Estimation". This function estimates how much bit security a bit
sequence (e.g., cryptographic key) achieves under the assumption that an adversary can determine the value of bits
within the bit sequence with a probability strictly greater than 50% and strictly lower than 100%. The adversary may
enjoy such an advantage when the bit sequence establishment (e.g., key establishment) process leaks information against
a particular side-channel attack.

The function takes two inputs; the bit sequence length ("seqLength") and the adversarial bit inference rate
("inferenceRate"). From these inputs, the function determines the computational effort required by an adversary,
launching a key search attack by trialing keys (i.e., bit sequences) in order of decreasing probability. The adversary
goes through an iterative process where it first trials the most likely key (i.e., the bit sequence where each bit is
the adversary's inferred bit) and subsequent iterations trials the set of keys where an additional bit is assumed
incorrectly inferred.

This algorithm is covered and featured in the published research paper below:
M. de Ree et al., "Bit Security Estimation for Leakage-Prone Key Establishment Schemes," IEEE Communications Letters,
vol. 27, no. 7, 2023. [DOI: 10.1109/LCOMM.2023.3275647]

### 3. Grain128-PLE.py
This script contains the function ...