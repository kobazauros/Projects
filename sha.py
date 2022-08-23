"""
generate sha_256 fingerprint
"""
import math

TEST_MESSAGE = "46546464654654545455fgdfgsfdgfkljj'lklkj'lj'lk'111111111111111"
def to_binary(input_str, conv_type = 'string'):
    """
    converts argument to binary string
    conv_type = 'string' - string is converted as a string even if it contains digits
    conv_type = 'digits' - if string contains only digits it is converted to binary as an integer
    """
    if conv_type == 'string':
        try:
            byte_str = "".join(f"{ord(i):08b}" for i in input_str)
        except TypeError as err:
            print(err)
            byte_str = -1
    elif conv_type == 'digits':
        input_str = bin(int(input_str))[2:]
        while len(input_str) % 8 != 0:
            input_str = '0' + input_str
        byte_str = input_str
    else:
        byte_str = -1

    return byte_str

def pad_512(input_str):
    """
    get string padded up to multiples of 512
    """
    bin_input_str = to_binary(input_str, 'string')
    #add 1 as separator
    bin_input_str_sep = bin_input_str + '1'
    #pad with zeroes up to length of multiples of 512
    #reserving length of 64 to contain binary value of initial string length
    while (len(bin_input_str_sep) + 64) % 512 != 0:
        bin_input_str_sep += '0'

    #append length of initial string as binary
    bin_init_len_str = to_binary(len(bin_input_str), 'digits')

    try:
        return bin_input_str_sep + bin_init_len_str.zfill(64)
    except TypeError as err:
        print(err)

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
    res = bin(int(res*(1<<32)))[2:].zfill(32)
    return res

def split_string(string, length):
    """
    split string to list of elements of specified length
    """
    return [string[x:x+length] for x in range(0, len(string), length)]

def rightrotate(string, num):
    """
    rotate string right for num positions
    """
    return string[len(string)-num:len(string)] + string[0:len(string)-num]

def rightshift(string, num):
    """
    shift string right for num positions
    """
    return string[0:len(string)-num].zfill(32)

def logical_xor(a_str, b_str, c_str):
    """
    imitate xor operation on three strings
    """
    res = int(a_str, 2) ^ int(b_str, 2) ^ int(c_str, 2)
    res = f"{res:b}".zfill(32)
    if len(res) < 32:
        print("")
    return res

def logical_add(a_str,
                b_str = "0b00000000000000000000000000000000",
                c_str = "0b00000000000000000000000000000000",
                d_str = "0b00000000000000000000000000000000",
                e_str = "0b00000000000000000000000000000000"):
    """
    imitate add operation on four strings
    """
    res = int(a_str, 2) + int(b_str, 2) + int(c_str, 2) + int(d_str, 2) + int(e_str, 2)
    res = f"{res:b}"[-32:].zfill(32)
    return res




# 8 hash values,
# hard-coded constants that represent the first 32 bits of the fractional parts
# of the square roots of the first 8 primes: 2, 3, 5, 7, 11, 13, 17, 19

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

# split message into 512 chunks
message = pad_512(TEST_MESSAGE)
message_chunks = split_string(message, 512)

h0 = hash_values[0]
h1 = hash_values[1]
h2 = hash_values[2]
h3 = hash_values[3]
h4 = hash_values[4]
h5 = hash_values[5]
h6 = hash_values[6]
h7 = hash_values[7]

for i in message_chunks:
    #split each chunk into 32-bit words
    word_32bit = split_string(i, 32)
    #add 48 more words initialized to zero to make 64
    word_32bit.extend(['0'*32]*48)
    for j in range(16,len(word_32bit)):
        s0 = logical_xor(rightrotate(word_32bit[j - 15], 7), \
                        rightrotate(word_32bit[j - 15], 18), \
                        rightshift(word_32bit[j - 15], 3))
        s1 = logical_xor(rightrotate(word_32bit[j - 2], 17), \
                        rightrotate(word_32bit[j - 2], 19), \
                        rightshift(word_32bit[j - 2], 10))
        word_32bit[j] = logical_add(word_32bit[j - 16], s0, word_32bit[j - 7], s1)
        word_32bit[j] = word_32bit[j].zfill(32)

    a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7

    for i in range(0, 64):
        S1 = logical_xor(rightrotate(e, 6), rightrotate(e, 11), rightrotate(e, 25))
        ch = (int(e, 2) & int(f, 2)) ^ ((~int(e, 2)) & int(g, 2))
        ch = f"{ch:b}".zfill(32)
        temp1 = logical_add(h, S1, ch, round_constants[i], word_32bit[i])
        S0 = logical_xor(rightrotate(a, 2), rightrotate(a, 13), rightrotate(a, 22))
        maj = (int(a, 2) & int(b, 2)) ^ (int(a, 2) & int(c, 2)) ^ (int(b, 2) & int(c, 2))
        maj = f"{maj:b}".zfill(32)
        temp2 = logical_add(S0, maj)
        h = g
        g = f
        f = e
        e = logical_add(d, temp1)
        d = c
        c = b
        b = a
        a = logical_add(temp1, temp2)
    h0 = logical_add(h0, a)
    h1 = logical_add(h1, b)
    h2 = logical_add(h2, c)
    h3 = logical_add(h3, d)
    h4 = logical_add(h4, e)
    h5 = logical_add(h5, f)
    h6 = logical_add(h6, g)
    h7 = logical_add(h7, h)

    result = hex(int(h0, 2))[2:] + \
                hex(int(h1, 2))[2:] + \
                hex(int(h2, 2))[2:] + \
                hex(int(h3, 2))[2:] + \
                hex(int(h4, 2))[2:] + \
                hex(int(h5, 2))[2:] + \
                hex(int(h6, 2))[2:] + \
                hex(int(h7, 2))[2:]

try:
    assert result == "28e30cd2269981f9b2825756b5423e572710a9ed7146b6e2271e8e40ee69b31f"
except AssertionError as assert_err:
    print(assert_err)
