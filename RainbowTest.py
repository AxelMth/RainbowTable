import Rainbow
from hashlib import md5, sha1, sha224, sha256, sha384, sha512

rainbow = Rainbow.Rainbow()
words = ["hey", "azertyuiop12356", "Hello World !","12345678&é"'(-è_ç$*^``){]:/.']

def doAllTests():
    """
        Run all tests on a Rainbow object
    """
    funcTable = {
        "Hash_Test": testHash(),
        "Reduce_Test": testReduce(),
        "Table_Test": testTable(),
        "PassLength_Test": testPassLengthGeneration(),
        "NumberChains_Test": testNumberOfChains(),
    }
    counter = 0
    yield counter
    for key in funcTable.keys():
        funcTable[key]
        counter += 1
        yield counter

def testHash():
    """
        Check if the hashWord function of the Rainbow class is
        working properly
    """
    global words
    for word in words:
        rainbow = Rainbow.Rainbow(encode_func="md5")
        assert(rainbow.hashWord(word)
                    == md5(word.encode("utf-8")).hexdigest())
        rainbow = Rainbow.Rainbow(encode_func="sha1")
        assert(rainbow.hashWord(word)
                    == sha1(word.encode("utf-8")).hexdigest())
        rainbow = Rainbow.Rainbow(encode_func="sha224")
        assert(rainbow.hashWord(word)
                    == sha224(word.encode("utf-8")).hexdigest())
        rainbow = Rainbow.Rainbow(encode_func="sha256")
        assert(rainbow.hashWord(word)
                    == sha256(word.encode("utf-8")).hexdigest())
        rainbow = Rainbow.Rainbow(encode_func="sha384")
        assert(rainbow.hashWord(word)
                    == sha384(word.encode("utf-8")).hexdigest())
        rainbow = Rainbow.Rainbow(encode_func="sha512")
        assert(rainbow.hashWord(word)
                    == sha512(word.encode("utf-8")).hexdigest())

def testReduce():
    """
        Check if the Rainbow class is reducing words in a good way
    """
    global words
    for word in words:
        for i in range(rainbow.chain_length):
            hashed_word = rainbow.hashWord(word)
            assert(len(rainbow.reduce(hashed_word, i)) == rainbow.pass_length)

def testTable():
    """
        Check if the rainbow table is coherent
    """
    for test_iteration in range(1000):
        for word in rainbow.rainbow_table.keys():
            pwd = word
            break
        next_pwd = pwd
        for i in range(rainbow.chain_length):
            hashed_word = rainbow.hashWord(next_pwd)
            next_pwd = rainbow.reduce(hashed_word, i)
        assert(hashed_word == rainbow.rainbow_table[pwd])

def testNumberOfChains():
    """
        Test if the number of chains respects
    """
    assert(rainbow.number_of_chains < len(rainbow.covered_chars)**rainbow.pass_length)

def testPassLengthGeneration():
    assert(len(rainbow.generatePassword()) == rainbow.pass_length)
