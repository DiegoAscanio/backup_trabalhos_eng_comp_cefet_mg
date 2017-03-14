#!/usr/bin/python

import random

# functions that generate "random" sentences and dictionary words
def gimme(what):
    ind = random.randint(0,len(what)-1)
    return what[ind]

articles = [line.strip() for line in open('dict/articles')]
adjectives = [line.strip() for line in open('dict/adjectives')]
nouns = [line.strip() for line in open('dict/nouns')]
verbs = [line.strip() for line in open('dict/verbs')]
words = [line.strip() for line in open('dict/words')]

def get_sentence():
    return (gimme(articles) + ' ' + gimme(adjectives) + ' ' + gimme(nouns) + ' ' + gimme(verbs) + ' ' +
              gimme(articles) + ' ' + gimme(adjectives) + ' ' + gimme(nouns))

def get_word():
    return gimme(words)
