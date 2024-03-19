"""
The function Bit_Security_Estimation estimates how much bit security a bit sequence (e.g., cryptographic key) achieves
under the assumption that an adversary can determine the value of bits within the bit sequence with a probability
strictly greater than 50% and strictly lower than 100%. The adversary may enjoy such an advantage when the bit sequence
establishment (e.g., key establishment) process leaks information against a particular side-channel attack.

The function takes as inputs the bit sequence length (seqLength) and the adversarial bit inference rate (inferenceRate).
The function determines the computational effort required by an adversary, launching a key search attack by trialing
keys (i.e., bit sequences) in order of decreasing probability. The adversary goes through an iterative process where
it first trials the most likely key (i.e., the bit sequence where each bit is the adversary's inferred bit) and
subsequent iterations trials the set of keys where an additional bit is assumed incorrectly inferred.

This algorithm is covered and featured in the published research paper below:
M. de Ree et al., "Bit Security Estimation for Leakage-Prone Key Establishment Schemes," IEEE Communications Letters,
vol. 27, no. 7, 2023. [DOI: 10.1109/LCOMM.2023.3275647]
"""

def Bit_Security_Estimation(seq_length, inference_rate):
    import math

    guesses = 0
    sum_upperBound = 0

    for bits_false in range(seq_length):
        # Prepares the starting index for the guessed keys.
        sum_lowerBound = sum_upperBound + 1
    
        # Estimates the number of keys of length [n] in which [0 to n] bits were guessed (in)correctly
        # (i.e., binomial coefficient).
        trialed_keys_in_iteration = math.comb(seq_length, bits_false)

        # Sets and sums the indexes of the guessed keys within the current set of most likely keys.
        sum_upperBound = sum_upperBound + trialed_keys_in_iteration
        ordinality_summation = (sum_lowerBound + sum_upperBound) * (sum_upperBound - sum_lowerBound + 1) / 2

        # Increases the number of guesses required by the adversary from trying the set of most likely, remaining, keys.
        guesses = guesses + ordinality_summation * inference_rate ** (seq_length - bits_false) * (1 - inference_rate) ** bits_false

        # Prepares the indexes for the next round of adversarial guesses.
        sum_lowerBound = sum_lowerBound + trialed_keys_in_iteration

    # Determine the bit security from the average number of guesses required by an adversary to find the correct key.
    return math.log2(2 * (guesses - 1))


# Example
print(Bit_Security_Estimation(seq_length = 128, inference_rate = 0.6))