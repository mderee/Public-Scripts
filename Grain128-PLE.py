import numpy as np
import binascii

lfsr = []
nfsr = []

# Helper functions for interconversion of bits and strings
def get_rnd_bitstream(num):
    import random
    r_int = random.randint(0, 2 ** num - 1)
    r_bin = format(r_int, 'b')
    r_bin = (num - len(r_bin)) * '0' + r_bin
    return r_bin

def string2bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def bits2string(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))


# Main functions: register initialization, clocking, keystream generation
#                 encryption, and decryption.
def init(iv, key):
    global lfsr, nfsr
    nfsr = np.zeros(len(key), dtype=bool)
    nfsr[:] = [bool(int(key[ix])) for ix in range(len(key))]
    lfsr = np.zeros(len(key), dtype=bool)
    lfsr[:len(iv)] = [bool(int(iv[ix])) for ix in range(len(iv))]
    lfsr[len(iv):-1] = 1
    lfsr[-1] = 0

def init_clock(rounds, key):
    global lfsr, nfsr
    for ix in range(rounds):
        fx = (lfsr[0] ^ lfsr[7] ^ lfsr[38] ^ lfsr[70] ^ lfsr[81] ^ lfsr[96])
        gx = (nfsr[0] ^ nfsr[26] ^ nfsr[56] ^ nfsr[91] ^ nfsr[96] ^ (nfsr[3] & nfsr[67]) ^ (nfsr[11] & nfsr[13]) ^
              (nfsr[17] & nfsr[18]) ^ (nfsr[27] & nfsr[59]) ^ (nfsr[40] & nfsr[48]) ^ (nfsr[61] & nfsr[65]) ^
              (nfsr[68] & nfsr[84]) ^ (nfsr[22] & nfsr[24] & nfsr[25]) ^ (nfsr[70] & nfsr[78] & nfsr[82]) ^
              (nfsr[88] & nfsr[92] & nfsr[93] & nfsr[95]))
        hx = ((nfsr[12] & lfsr[8]) ^ (lfsr[13] & lfsr[20]) ^ (nfsr[95] & lfsr[42]) ^ (lfsr[60] & lfsr[79]) ^
              (nfsr[12] & nfsr[95] & lfsr[94]))
        yx = hx ^ lfsr[93] ^ nfsr[2] ^ nfsr[15] ^ nfsr[36] ^ nfsr[45] ^ nfsr[64] ^ nfsr[73] ^ nfsr[89]
        if ix in range(0, 320):
            nfsr[:-1] = nfsr[1:]
            nfsr[-1] = gx ^ lfsr[0] ^ yx
            lfsr[:-1] = lfsr[1:]
            lfsr[-1] = fx ^ yx
        elif ix in range(320, 384):
            nfsr[:-1] = nfsr[1:]
            nfsr[-1] = gx ^ lfsr[0] ^ yx ^ bool(int(key[ix - 320]))
            lfsr[:-1] = lfsr[1:]
            lfsr[-1] = fx ^ yx ^ bool(int(key[ix - 256]))
        elif ix >= 384:
            nfsr[:-1] = nfsr[1:]
            nfsr[-1] = gx ^ lfsr[0]
            lfsr[:-1] = lfsr[1:]
            lfsr[-1] = fx

def gen_key_stream():
    global lfsr, nfsr
    while True:
        fx = (lfsr[0] ^ lfsr[7] ^ lfsr[38] ^ lfsr[70] ^ lfsr[81] ^ lfsr[96])
        gx = (nfsr[0] ^ nfsr[26] ^ nfsr[56] ^ nfsr[91] ^ nfsr[96] ^ (nfsr[3] & nfsr[67]) ^ (nfsr[11] & nfsr[13]) ^
              (nfsr[17] & nfsr[18]) ^ (nfsr[27] & nfsr[59]) ^ (nfsr[40] & nfsr[48]) ^ (nfsr[61] & nfsr[65]) ^
              (nfsr[68] & nfsr[84]) ^ (nfsr[22] & nfsr[24] & nfsr[25]) ^ (nfsr[70] & nfsr[78] & nfsr[82]) ^
              (nfsr[88] & nfsr[92] & nfsr[93] & nfsr[95]))
        hx = ((nfsr[12] & lfsr[8]) ^ (lfsr[13] & lfsr[20]) ^ (nfsr[95] & lfsr[42]) ^ (lfsr[60] & lfsr[79]) ^
              (nfsr[12] & nfsr[95] & lfsr[94]))
        yx = hx ^ lfsr[93] ^ nfsr[2] ^ nfsr[15] ^ nfsr[36] ^ nfsr[45] ^ nfsr[64] ^ nfsr[73] ^ nfsr[89]
        nfsr[:-1] = nfsr[1:]
        nfsr[-1] = gx ^ lfsr[0]
        lfsr[:-1] = lfsr[1:]
        lfsr[-1] = fx
        yield yx

def encrypt(iv, key, clock_rounds, plain):
    init(iv, key)
    init_clock(clock_rounds, key)
    plain = string2bits(plain)
    stream = gen_key_stream()
    cipher = [str(int(bool(int(plain[ix])) ^ next(stream))) for ix in range(len(plain))]
    cipher = ''.join(cipher)
    return cipher

def decrypt(iv, key, clock_rounds, cipher):
    init(iv, key)
    init_clock(clock_rounds, key)
    stream = gen_key_stream()
    plain = [str(int(bool(int(cipher[ix])) ^ next(stream))) for ix in range(len(cipher))]
    plain = ''.join(plain)
    plain = bits2string(plain)
    return plain


# Run Grain-128PLE with a random key, IV, and channel-induced errors
def demo_grain(variant):
    iv_size = 96
    key_size = 128
    clock_rounds = 512
    print("=== demo using Grain-{variant} ===".format(variant=variant))

    plaintext = 'grain cipher-based encryption'
    iv = get_rnd_bitstream(iv_size)
    print("IV:                 ", iv, "(", iv_size, "bits )")
    key = get_rnd_bitstream(key_size)
    print("key:                ", key, "(", key_size, "bits )")
    print("plaintext:          ", plaintext)
    ciphertext = encrypt(iv, key, clock_rounds, plaintext)
    print("ciphertext (bin):   ", ciphertext)

    # The ciphertext is sent although there will be some (2) bit flips introduced into the received_ciphertext.
    # The bit flips can (sometimes) not be converted back to a printable string, in that case rerun the script.
    from random import randint
    error_pattern = np.zeros(len(ciphertext), dtype=int)
    error_pattern = [str(error_pattern[ix]) for ix in range(len(error_pattern))]
    for errors in range(2):
        index = randint(0, len(ciphertext) - 1)
        error_pattern[index] = '1'
    error_pattern = ''.join(error_pattern)
    print("error patt. (bin):  ", error_pattern)
    rec_ciphertext = [str(int(bool(int(ciphertext[ix])) ^ bool(int(error_pattern[ix])))) for ix in range(len(ciphertext))]
    rec_ciphertext = ''.join(rec_ciphertext)
    print("received (bin):     ", rec_ciphertext)

    # received = decrypt(iv, key, clock_rounds, ciphertext)
    received = decrypt(iv, key, clock_rounds, rec_ciphertext)
    print("received:           ", received)

if __name__ == "__main__":
    demo_grain("128_PLE")
