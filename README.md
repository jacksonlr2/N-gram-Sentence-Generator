# N-Gram Sentence Generator

## Overview
This program is a simple implementation of ngrams. It will learn an N-gram language model from an arbitrary number of
plain text files. After forming a model, it will generate a given number of sentences based on that N-gram model.

## Usage Instructions:
Run python file with n (desired ngram model), m (number of sentences to be generated), followed by the text files
being used in the command line: ngram.py n m input-file/s

## Usage Example:
ngram.py 3 10 pg2554.txt pg2600.txt pg1399.txt would generate 10 sentences using a trigram model using text from the
three files.

## Output Example:
ngram.py 10 5 alice.txt dracula.txt gatsby.txt warPeace.txt odyssey.txt sherlock.txt twoCities.txt

Total Sentences: 8466

Total Tokens: 1906049

1.) i’ll go in and hand the letter to the emperor myself so.

2.) the place was a long way off and while they were judging what with one thing and another filling in the papers.

3.) he writes about this war said the prince with the ironic smile that had.

4.) there were wounded in the yards at the windows.

5.) for six days my men kept driving in the best cows and feasting upon them but when jove the son of saturn had added
    a seventh day the fury of the gale abated we therefore went on board.

## Algorithm Overview:
1) Program takes in the info given in the command line (n, m, and files).
2) A tag is generated with and end tag followed by a series of start tags where the number of start tags is equal to
   n - 1
3) For each file, end punctuation (.!?) are replaced with the generated tag and variables such as "\n" are removed.
4) Each sentence is split based on the <end> tags at the end of the sentences.
5) For each sentence, words and remaining tags are extracted into an array. All other punctuation is ignored except
   for '’'.
6) Going through the array for each sentence, the program tracks how often n word and n-1 word combinations occur
   throughout all files to help form the ngram model.
7) After forming the ngram model, the statistics for all files (sentences and tokens) are printed and the given number
   of sentences are generated from the ngrams.
8) To form the sentences, a number is randomly generated. The program generates a list of most probable word that
   would come next based on the previous history. It would then go through the list until the sum of the probability
   equals to or surpasses the randomly generated number.
9) If n is 1, the program while simply print out the unigram.
