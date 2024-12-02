import numpy as np
import nltk #nltk.download('punkt')
from nltk.stem.porter import PorterStemmer

Stemmer = PorterStemmer()

def tokenize(sentence):
    return nltk.word_tokenize(sentence)

def stem(word):
    return Stemmer.stem(word.lower())

def tas_kata(tokenized_sentence,words):
    sentence_word = [stem(word) for word in tokenized_sentence]
    tas = np.zeros(len(words),dtype=np.float32)

    for idx , w in enumerate(words):
        if w in sentence_word:
            tas[idx] = 1

    return tas