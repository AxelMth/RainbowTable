import Rainbow
from RainbowTest import *
import progressbar
import argparse

parser = argparse.ArgumentParser(description="Crack a given number of password.")
parser.add_argument('-n', help="The number of passwords to be cracked"
                        ,nargs=1, type=int, action="store", dest="number_of_pwds"
                        , required=True)
parser.add_argument('-p', help="The length of passwords to be cracked"
                        , type=int, nargs=1, default=3, action="store"
                        , dest="pass_length")
parser.add_argument('-c', help="The length of each chain"
                        , type=int, nargs=1, default=100, action="store"
                        , dest="chain_length")
parser.add_argument('-r', help="The number of rows in the rainbow table"
                        , type=int, nargs=1, default=5000, action="store"
                        , dest="number_of_chains")
args = parser.parse_args()

def test(nb_iterations):
    pass_length = args.pass_length if type(args.pass_length) is int else args.pass_length[0]
    number_of_chains = args.number_of_chains if type(args.number_of_chains) is int else args.number_of_chains[0]
    chain_length = args.chain_length if type(args.chain_length) is int else args.chain_length[0]
    print("Tempting to crack {} passwords of length equals to {}"
                .format(nb_iterations, pass_length))
    succeded_guess = 0
    hypothetic_succeed = 0
    nb_of_guesses = 0
    with progressbar.ProgressBar(max_value=nb_iterations) as bar:
        for i in range(nb_iterations):
            rainbow = Rainbow.Rainbow(pass_length=pass_length, chain_length=chain_length, number_of_chains=number_of_chains)
            pwd_to_guess = rainbow.generatePassword()
            hashed_pwd = rainbow.hashWord(pwd_to_guess)
            guess = rainbow.lookAtPasswd(hashed_pwd)
            if guess is not None:
                nb_of_guesses += 1
                if guess == pwd_to_guess:
                    succeded_guess += 1
            if rainbow.should_have_worked:
                hypothetic_succeed += 1
            bar.update(i)
    print("Hypothetical efficiency : {}%".format(str(hypothetic_succeed/nb_iterations*100)))
    print("Algorith efficiency on {1} passwords : {0}%".format(int(succeded_guess/nb_iterations*100), nb_iterations))
    if nb_of_guesses != 0:
        print("Percentage of good guessed password out of the number of password guessed by the algorithm : {}%".format(succeded_guess/nb_of_guesses*100))

if __name__ == "__main__":
    print("Passing all tests on the Rainbow class...")
    with progressbar.ProgressBar(max_value=5) as bar:
        for counter in doAllTests():
            bar.update(counter)
    print("All tests passed successfully ! ")
    test(args.number_of_pwds[0])
