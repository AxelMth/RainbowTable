from hashlib import md5, sha1, sha224, sha256, sha384, sha512
from random import randrange
import sys

# Define an example of chars that can be part of a simple password
lowers = "abcdefghijklmnopqrstuvwxyz"
uppers = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "0123456789"
all_covered_chars = lowers + uppers + numbers

class Rainbow:

    # Define the correspondance between string and hashing functions given by
    # the hashlib library
    hashFuncTable = {
        sha1.__name__: sha1,
        'sha1': sha1,
        sha224.__name__: sha224,
        'sha224': sha224,
        sha256.__name__: sha256,
        'sha256': sha256,
        sha384.__name__: sha384,
        'sha384': sha384,
        sha512.__name__: sha512,
        'sha512': sha512,
        md5.__name__: md5,
        'md5': md5
    }

    def __init__(self, encode_func='md5', pass_length=2, chain_length=20,
                    number_of_chains=500, covered_chars=lowers, debug=False):
        """ Initialize the Rainbow class and generate the rainbow table according
            to the arguments passed through the constructor.

            Parameters
            ----------
            encode_func : string
                Define the hashing function to be used to build the rainbow
                table.
            pass_length : integer
                Define the length of the password to be guessed.
            chain_length : integer
                Define the length of one chain. Can also be seen as the number
                of columns.
            number_of_chains : integer
                Define the number of rainbow chains. Can also be seen as the
                number of rows.
            covered_chars : string
                Define all characters with which you can construct any password.
            debug : boolean
                Enable or not debugging informations.
        """
        self.debug = debug
        if (encode_func in self.hashFuncTable.keys()):
            self.encode_func = encode_func
        else:
            print("Error: Bad hash function passed as argument of the Rainbow constructor.")
            sys.exit()
        if pass_length > 4:
            print("Warning ! A password length greater than 4 involves a huge calculus time.")
            res = input("Do you want to continue ? (y/n) Then press enter. ")
            if res == "y" or res == "Y":
                self.pass_length = pass_length
            else:
                print("Exiting...")
                sys.exit()
        else:
            self.pass_length = pass_length
        self.chain_length = chain_length
        if number_of_chains > len(covered_chars)**pass_length:
            print("Error ! Please specify a number_of_chains lower than the length of covered_chars.")
            print("Exiting...")
            sys.exit()
        self.number_of_chains = number_of_chains
        self.covered_chars = covered_chars
        if self.debug:
            print("Generating the rainbow table.")
        self.generateTable()
        if self.debug:
            print("Rainbow table successfully created.")

    def generatePassword(self):
        """ This function generates a random password to build the rainbow
            table and to test the lookAtPasswd function.
        """
        covered_chars_length =  len(self.covered_chars)
        word = ""
        for i in range(self.pass_length):
            word += self.covered_chars[randrange(covered_chars_length)]
        return word

    def hashWord(self, word):
        """ Hash the given word with the hashing function passed as
            argument in the constructor.

            Parameter
            ---------
            word : string
                Word to hash.
        """
        return self.hashFuncTable[self.encode_func](word.encode('utf-8')).hexdigest()

    def generateTable(self):
        """ Construct the rainbow table with number_of_chains rows and
            chain_length (hidden) columns. Return in the rainbow_table
            attribute a dictionnary associating a word to the final hash.
        """
        self.rainbow_table = {}
        all_keys = []
        for i in range(self.number_of_chains):
            entry_word = self.generatePassword()
            while entry_word in all_keys:
                entry_word = self.generatePassword()
            next_word = entry_word
            for k in range(self.chain_length):
                hashW = self.hashWord(next_word)
                next_word = self.reduce(hashW, k)
            self.rainbow_table[entry_word] = hashW
            all_keys.append(entry_word)

    def reduce(self, hashWord, chain_index_position):
        """ Transform the hashWord in a word with length equal to pass_length.
            Take the chain_index_position to extract a sub string from the
            hashWord parameter. This index defines at each step the char to be
            taken from the covered_chars table.

            Parameter
            ---------
            hashWord : string
                Hash word to reduce in a word with length equal to pass_length.
            chain_index_position : integer
                Define which reducing function will be executed. Each reducing
                function is recognizable with this unique integer.
        """
        word = ""
        hash_len = len(hashWord)
        covered_chars_length = len(self.covered_chars)
        for i in range(self.pass_length):
            sub_hash = ""
            for j in range(2):
                sub_hash += hashWord[(i + j + chain_index_position) % hash_len]
            index = int("0x" + sub_hash, 16)
            word += self.covered_chars[index % covered_chars_length]
        return word

    def findInChain(self, hash_word, hashW):
        """
            Find the corresponding password according to the given hash_word.

            Parameter
            ---------
            hash_word : string
                Hashed word found in the iterative part of the lookAtPasswd
                function. Define the final hash where a correspondance has
                been found.
            hashW : string
                Initial hashed word to be found by the lookAtPasswd function.
                Hashed word to be cracked.
        """
        words = []
        for entry_word, final_hash in self.rainbow_table.items():
            if final_hash == hash_word:
                words.append(entry_word)
        hash_word_copy = hash_word
        for word in words:
            if self.debug:
                if self.rainbow_table[word] != hash_word_copy:
                    print("The findInChain function is not working properly...")
            hash_word = self.hashWord(word)
            if hash_word == hashW:
                return word
            for k in range(self.chain_length-1):
                next_word = self.reduce(hash_word, k)
                hash_word = self.hashWord(next_word)
                if hash_word == hashW:
                    return next_word
        return None

    def hashFromChainIndex(self, hash_word, chain_index):
        """
            Function programmed to do the successive hash - reduce calls to
            find if the hash returned is in the rainbow table.

            Parameter
            ---------
            hash_word : string
                Initial hashed word to be craked.
            chain_index : integer
                Define the number of iteration that will be done to obtain
                the hash to be found in the rainbow table.
        """
        hash_W = hash_word
        for i in range(chain_index, self.chain_length-1):
            pwd = self.reduce(hash_W, i)
            hash_W = self.hashWord(pwd)
        return hash_W

    def lookAtPasswd(self, hashW):
        """
            Function that return the cracked password depending on the hashed
            word given.

            Parameter
            ---------
            hashW: string
                Hash to be cracked.
        """
        values = self.rainbow_table.values()
        self.should_have_worked = False
        for i in range(self.chain_length-1,-1,-1):
            hash_word = self.hashFromChainIndex(hashW, i)
            if hash_word in values:
                self.should_have_worked = True
                return_value = self.findInChain(hash_word, hashW)
                if not return_value is None:
                    return return_value
                else:
                    self.should_have_worked = False
        return None
