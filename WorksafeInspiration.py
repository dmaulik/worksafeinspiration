from __future__ import division
import re
import string
import random
import sys
import json
import os

class WorksafeInspirationGenerator:
    def __init__(self):
        self.markovChainTree = dict()

    def train_helper(self, file):
        lines = file.read().splitlines()
        for line in lines:
            self.train(line)

        with open('stored/markovChainTree.json', 'w') as f:
            json.dump(self.markovChainTree, f)

    def train(self, text):
        # Make lower case then split at spaces
        text = text.lower()
        words = re.split(r'[\s]', text)

        # For each word pair either add it to our tree or increase rank
        for a, b in [(words[i], words[i + 1]) for i in range(len(words) - 1)]:
            if a not in self.markovChainTree:
                self.markovChainTree[a] = dict()

            if b not in self.markovChainTree[a]:
                self.markovChainTree[a][b] = 1
            else:
                self.markovChainTree[a][b] = self.markovChainTree[a][b] + 1

    def generate_helper(self):
        with open('stored/markovChainTree.json', 'r') as f:
            try:
                self.markovChainTree = json.load(f)
            except ValueError:
                self.markovChainTree = dict()

        len = 0
        punctuation = False
        inspiration = ""
        for word in self.generate():
            # capitilize the first word
            if len == 0:
                word = ' '.join(w[0].upper() + w[1:] for w in word.split())

            # capitilize after sentence end
            if punctuation == True:
                word = ' '.join(w[0].upper() + w[1:] for w in word.split())
                punctuation = False

            punc = set('?.!')
            if any(c in punc for c in word):
                punctuation = True

            # capitilize 'I'
            if word == "i":
                word = word.upper()

            len += 1
            inspiration += word + " "

        print(inspiration)

    def generate(self):
        start = random.choice(self.markovChainTree.keys())
        yield start

        cur = start

        i = 1
        while i == 1:
            top = -100
            topWord = ""
            if cur in self.markovChainTree:
                for w in self.markovChainTree[cur]:
                    value = random.random()*(self.markovChainTree[cur][w]/len(self.markovChainTree[cur]))
                    if(value > top):
                        top = value
                        topWord = w
                yield topWord
                cur = topWord
            else:
                return

def main(args):
    sfwGen = WorksafeInspirationGenerator()
    for i in range(0, len(args)):
        if args[i] == "-t":
            file = open(args[i + 1], 'r')
            sfwGen.train_helper(file)
        if args[i] == "-g":
            sfwGen.generate_helper()

if __name__ == "__main__":
    main(sys.argv)