import math

# How many guesses does an adversary, on average, have to try to find the correct key (probability 2^-n)?
# Input parameters (adversarial bit estimation accuracy, range of key lengths).
est_Accuracy = 0.6
min_keySize = 1
max_keySize = 514

# Computes the Bit Security level for all key lengths in the pre-selected range.
for keySize in range(min_keySize, max_keySize + 1):

    # Resets the index of the guessed keys.
    sum_upperBound = 0

    # Resets the average number of guesses that an adversary needs to try to find the correct key.
    guesses = 0

    for bits_false in range(0, keySize + 1):
        #Prepares the starting index for the guessed keys.
        sum_lowerBound = sum_upperBound + 1
    
        # Estimates the number of keys of length [n] in which [0 to n] bits were guessed (in)correctly
        # (i.e., binomial coefficient).
        trialed_keys_in_iteration = math.comb(keySize, bits_false)

        # Sets and sums the indexes of the guessed keys within the current set of most likely keys.
        sum_upperBound = sum_upperBound + trialed_keys_in_iteration
        ordinality_summation = (sum_lowerBound + sum_upperBound) * (sum_upperBound - sum_lowerBound + 1) / 2

        # Increases the number of guesses required by the adversary from trying the set of most likely, remaining, keys.
        guesses = guesses + ordinality_summation * est_Accuracy**(keySize-bits_false) * (1-est_Accuracy)**bits_false

        # Prepares the indexes for the next round of adversarial guesses.
        sum_lowerBound = sum_lowerBound + trialed_keys_in_iteration

    # Computes and prints the bit security based on the average number of guesses that an adversary has to try to
    # find the correct key.
    bitSecurity = math.log2(2*guesses-1)
    print("Key size " + str(keySize) + " with bit-sec: " + str(bitSecurity))
