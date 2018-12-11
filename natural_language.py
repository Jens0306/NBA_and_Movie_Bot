import nltk
# nltk.download()
from nltk.tokenize import sent_tokenize
import nltk.data
spanish_tokenizer = nltk.data.load('tokenizers/punkt/spanish.pickle')

def translate():
    para = "Hello World. It’s good to see you. Thanks for buying this book."
    # sent_tokenize(para)
    print(sent_tokenize(para))
    return para