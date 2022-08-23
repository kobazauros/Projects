"""
generate sha_256 fingerprint
"""
import math

TEST_MESSAGE = "46546464654654545455fgdfgsfdgfkljj'lklkj'lj'lk'111111111111111"

def get_primes(num):
    """
    function getting list of first n primes
    """
    if num < 1:
        return -1
    f_p = 2
    primes_list = []
    while len(primes_list) != num:
        divider = 2
        test_prime = True
        while divider < f_p // 2 + 1:
            if f_p % divider == 0:
                test_prime = False
                break
            divider += 1
        if test_prime:
            primes_list.append(f_p)
        f_p += 1
    return primes_list

def get_32_bits(value, power = 2):
    """
    get first 32 bits of fractional part of value root
    pow = 2 means square root
    """
    if power < 2:
        print("bad power value")
    #take a first value in tuple made by math.modf - fractional part
    res = math.modf(value**(1/power))[0]
    res = int(res*(1<<32))
    return res

def split_bytes(byte_input, length):
    """
    split bytes to list of elements of specified length in bytes
    """
    return [byte_input[x:x+length] for x in range(0, len(byte_input), length)]

hash_values = []
round_constants = []

FIRST_8_PRIMES = get_primes(8)
FIRST_64_PRIMES = get_primes(64)
#get first 32 bits of fractional part of square roots
for i in range(8):
    hash_values.append(get_32_bits(FIRST_8_PRIMES[i], 2))
#get first 32 bits of fractional part of cubic roots
for i in range(64):
    round_constants.append(get_32_bits(FIRST_64_PRIMES[i], 3))
# convert initial message to bytes
bytes_input = bytes(str(TEST_MESSAGE), "utf8")
# get length of initial message in 64-bytes big-endian
len_b = len(bytes_input)*8
len_bits = len_b.to_bytes(8, 'big')
#print_bytes(len_bits)
# get zero fill with 1 as a separator
SEP = 128
zero_fill = SEP.to_bytes(((len(bytes_input) + 8)//64 + 1)*64 - len(bytes_input) - 8, 'little')
#print_bytes(zero_fill)

padded_message = bytes_input + zero_fill + len_bits
message_chunks = split_bytes(padded_message, 64)

h0 = hash_values[0]
h1 = hash_values[1]
h2 = hash_values[2]
h3 = hash_values[3]
h4 = hash_values[4]
h5 = hash_values[5]
h6 = hash_values[6]
h7 = hash_values[7]

ROR = lambda x, y: (((x & 0xffffffff) >> (y & 31)) | (x << (32 - (y & 31)))) & 0xffffffff
Ch = lambda x, y, z: (z ^ (x & (y ^ z)))
Maj = lambda x, y, z: (((x | y) & z) | (x & y))
R = lambda x, n: (x & 0xffffffff) >> n
Sigma0 = lambda x: (ROR(x, 2) ^ ROR(x, 13) ^ ROR(x, 22))
Sigma1 = lambda x: (ROR(x, 6) ^ ROR(x, 11) ^ ROR(x, 25))
Gamma0 = lambda x: (ROR(x, 7) ^ ROR(x, 18) ^ R(x, 3))
Gamma1 = lambda x: (ROR(x, 17) ^ ROR(x, 19) ^ R(x, 10))

for i in message_chunks:
    ZERO = 0
    zero = ZERO.to_bytes(4, 'big')
    i += zero*48
    #split each chunk into 4-byte words
    word = split_bytes(i, 4)
    for j in range(16,len(word)):
        word_0 = int.from_bytes(word[j-15], "big")
        word_1 = int.from_bytes(word[j-2], "big")
        g0 = Gamma0(word_0)
        g1 = Gamma1(word_1)
        word[j] = ((int.from_bytes(word[j-16], "big") + \
                    g0 + \
                    int.from_bytes(word[j-7], "big") + \
                    g1) & 0xffffffff).to_bytes(4, 'big')

    a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7

    for i in range(0, 64):
        temp0 = (h + Sigma1(e) + Ch(e, f, g) + \
                round_constants[i] + \
                int.from_bytes(word[i], "big")) & 0xffffffff
        temp1 = (Sigma0(a) + Maj(a, b, c)) & 0xffffffff
        h, g, f = g, f, e
        e = (d + temp0) & 0xffffffff
        d, c, b = c, b, a
        a = (temp0 + temp1) & 0xffffffff
    h0 = (h0 + a) & 0xffffffff
    h1 = (h1 + b) & 0xffffffff
    h2 = (h2 + c) & 0xffffffff
    h3 = (h3 + d) & 0xffffffff
    h4 = (h4 + e) & 0xffffffff
    h5 = (h5 + f) & 0xffffffff
    h6 = (h6 + g) & 0xffffffff
    h7 = (h7 + h) & 0xffffffff

result = hex(h0)[2:] + \
        hex(h1)[2:] + \
        hex(h2)[2:] + \
        hex(h3)[2:] + \
        hex(h4)[2:] + \
        hex(h5)[2:] + \
        hex(h6)[2:] + \
        hex(h7)[2:]


try:
    assert result == "28e30cd2269981f9b2825756b5423e572710a9ed7146b6e2271e8e40ee69b31f"
except AssertionError:
    print("value mismatch")
