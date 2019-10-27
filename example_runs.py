from itertools import chain
import spotreader


def get_words_from_file(fname):
    """ Extracts text from a text file and returns
    a list of words. Punctuation is not separated 
    from the words.
    """
    text_elements = []
    lines = open(fname, 'r').read().splitlines()
    for text in lines:
        text_elements.extend(text.split(' '))
    return text_elements

def word_generator():
    """ Generator that returns an endless loop of words. """
    words = ('Hello my name is Waldo and today '
             'I am going to find myself'.split())
    index = 0
    while True:
        yield words[index % len(words)]
        index += 1


if __name__ == "__main__":
    # First example: using a list of words.    
    words = get_words_from_file('input_text.txt')

    # Second example: using a generator.
    # words = word_generator()
    
    myApp = spotreader.SpotReader(words)
