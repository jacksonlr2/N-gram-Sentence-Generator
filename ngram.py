############################################################################
# ngram.py
############################################################################
#
# This program is a simple implementation of ngrams. It will learn an N-gram language model from an arbitrary number of
# plain text files. After forming a model, it will generate a given number of sentences based on that N-gram model.
#
# Usage Instructions:
# Run python file with n (desired ngram model), m (number of sentences to be generated), followed by the text files
# being used in the command line: ngram.py n m input-file/s
# Usage Example:
# ngram.py 3 10 pg2554.txt pg2600.txt pg1399.txt would generate 10 sentences using a trigram model using text from the
# three files.
#
# Output Example:
# main.py 10 5 alice.txt dracula.txt gatsby.txt warPeace.txt odyssey.txt sherlock.txt twoCities.txt
# Total Sentences: 8466
# Total Tokens: 1906049
# 1.) i’ll go in and hand the letter to the emperor myself so.
# 2.) the place was a long way off and while they were judging what with one thing and another filling in the papers.
# 3.) he writes about this war said the prince with the ironic smile that had.
# 4.) there were wounded in the yards at the windows.
# 5.) for six days my men kept driving in the best cows and feasting upon them but when jove the son of saturn had added
#     a seventh day the fury of the gale abated we therefore went on board.
#
# Algorithm Overview:
# 1) Program takes in the info given in the command line (n, m, and files).
# 2) A tag is generated with and end tag followed by a series of start tags where the number of start tags is equal to
#    n - 1
# 3) For each file, end punctuation (.!?) are replaced with the generated tag and variables such as "\n" are removed.
# 4) Each sentence is split based on the <end> tags at the end of the sentences.
# 5) For each sentence, words and remaining tags are extracted into an array. All other punctuation is ignored except
#    for '’'.
# 6) Going through the array for each sentence, the program tracks how often n word and n-1 word combinations occur
#    throughout all files to help form the ngram model.
# 7) After forming the ngram model, the statistics for all files (sentences and tokens) are printed and the given number
#    of sentences are generated from the ngrams.
# 8) To form the sentences, a number is randomly generated. The program generates a list of most probable word that
#    would come next based on the previous history. It would then go through the list until the sum of the probability
#    equals to or surpasses the randomly generated number.
# 9) If n is 1, the program while simply print out the unigram.
# _____________________________________________________
# Lenice Jackson
# Last Modified: February 21, 2022
# CMSC 416 Section 001
############################################################################

from sys import argv
from collections import Counter
from random import random
import re

# initialize input variables
inputLine = argv
n = 0
m = 0
files = []


# take in input variables from command line
inputLine = argv
n = int(inputLine[1])
m = int(inputLine[2])
files = inputLine[3:]


n_1dict = {}
tokens = 0
sent = 0
history = {}
search = ()


# generate tag
tag = "<e> <end>"
temp = n
while temp > 1:
    tag += " <s>"
    search += ("<s>",)
    temp -= 1

begin = search

for file in files:
    # read each file and remove irrelevant information
    with open(file, encoding="utf-8") as f:
        contents = f.read().lower().strip()
        contents = contents.replace("\n", " ")
        contents = contents.replace(",", "")
        contents = contents.replace("_", "")
        contents = contents.replace("—", " ")

        # add the generated tag to the end of each sentence
        contents = contents.replace(".", tag)
        contents = contents.replace("?", tag)
        contents = contents.replace("!", tag)

        # split the files into separate sentences
        contents = contents.split('<end> ')

    # isolate the words in each sentence
    for count, sentence in enumerate(contents):
        contents[count] = re.findall(r"[\w’]+|<e>|<s>", sentence)

    # count how many sentences were formed
    contents.pop()
    sent += len(contents)

    # keep track of n word and n-1 word combinations occurrences
    for count, sentence in enumerate(contents):
        tokens += len(contents[count])
        if len(sentence) > n + (n-1) + 1 and n > 1:
            for i, word in enumerate(sentence):
                if len(sentence) - i > n + (n-1) + 1:
                    history[tuple(sentence[i:i + (n - 1)])] = history.get(tuple(sentence[i:i+(n-1)]), ()) + (sentence[i+(n-1)],)
                if len(sentence) - i >= n - (n-1):
                    n_1dict[tuple(sentence[i:i+(n-1)])] = n_1dict.get(tuple(sentence[i:i+(n-1)]), 0) + 1
        if len(sentence) > 0 and n == 1:
            for i, word in enumerate(sentence):
                history[sentence[i]] = history.get(sentence[i], 0) + 1


# print stats
print("----------------------------------------")
print("Total Sentences: " + str(sent))
print("Total Tokens: " + str(tokens))

# sentence creation
ori_m = m
while m > 0 and n > 1:
    gen_sent = ""
    finish = False
    j = 0
    while not finish and j != 50:
        total_count = 0
        r_num = random()
        done = False
        options = Counter(history.get(search))
        options = options.most_common()
        for count, word in enumerate(options):
            total_count += (options[count][1] / n_1dict.get(search))
            if total_count >= r_num and not done:
                gen_sent += " " + str(options[count][0])
                done = True
                if options[count][0] == '<e>':
                    finish = True
                else:
                    search = search[1:]
                    search += (options[count][0],)
        j += 1

    print(str((ori_m+1) - m) + ".)" + gen_sent + ".")
    search = begin
    m -= 1
# Prints base case (unigram)
if n == 1:
    print("Unigram: " + str(sorted(history, key= history.get, reverse=True)))
