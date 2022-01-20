import re   # for RegEx
from random import choice

class WordleSolver:
    WORD_LIST = "./data/word_list.txt"
    
    def __init__(self, dict_path = None):
        self.WORD_LIST = dict_path if dict_path else self.WORD_LIST
        # Load words list
        with open(self.WORD_LIST, 'r') as file:
            self.word_list = file.readlines()
        if not self.word_list:
            print("[Error] Unable to load dictionary at {}".format(self.WORD_LIST))
        else:
            print("[/] Successfully loaded {} lines from dictionary.".format(len(self.word_list)))
            
    def run(self, delims = ['x','o','.']):
        if len(self.word_list) == 0: self.__init__()
        # Setup tracking for letters
        wrong_spot = []
        correct_spot = dict([(i,[]) for i in range(5)])
        # Setup solutions, guesses, and match_results
        solutions, guesses = self.word_list, []
        while len(guesses) < 5 or len(solutions) > 0:
            guesses.append(choice(solutions))
            print("Guess:", guesses[-1])
            # Loop to cycle though invalid words
            while (match_results := input("Enter  matches({}), misplaced({}), and misses({}) or <Enter> for invalid words:\n>> ".format(*delims))) == "": 
                guesses[-1] = choice(solutions)
                print("[Skipping invalid word]\nNew Guess:", guesses[-1])
            # Return immediately once solution is found
            if match_results == delims[0] * 5: 
                return (True, "[Solution Found]")
            # Check for matches
            for i, c in enumerate(match_results):
                if c == delims[0]:                      # Letter is in correct spot
                    correct_spot[i] = [guesses[-1][i]]
                elif c == delims[1]:                    # Letter in word somewhere
                    wrong_spot.append(guesses[-1][i])
                if c == delims[1] or c == delims[2]:    # Letter is in the wrong spot
                    correct_spot[i].append('^' + guesses[-1][i])
            # Generate Regex from known information
            regexp = "^" + "".join(["(?=.*[" + w + "])" for w in wrong_spot]) + \
                    "[" + "][".join(["".join(c) for c in correct_spot.values()]) + "]$"
            # Update the solutions
            solutions = [s for s in solutions if re.match(regexp, s)]
        return (False, "[No Solution Found]")

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 3:
        WordleSolver(sys.argv[1]).run(list(sys.argv[2]))
    elif len(sys.argv) == 2:
        WordleSolver(sys.argv[1]).run()
    else:
        WordleSolver().run()