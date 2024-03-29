
"""
author: Jay Edwards

This class handles generating definition matching using a library of dictionary terms.
note: this library (as well as others in other classes) require quite a bit of time to load. be mindful of that.
"""
from PyDictionary import PyDictionary


class DefinitionMatch:
    """
    A class for handling definition matching

    Dependencies:
    - PyDictionary

    Attributes:
    - words: a tuple of words to find definitions for
    - pairings: a dictionary that stores the pairings of words and their corresponding definitions
    - dictionary: a PyDictionary object that provides access to a library of dictionary terms

    Methods:
    - find_definitions(): searches for the definitions of the words in the 'words' attribute using the PyDictionary library. Returns a dictionary that contains word-definition pairs for only those words that have a definition in the library.
    - modify_definition(word, new_definition): modifies the definition of an existing word-definition pair in the 'pairings' attribute.
    - get_dictionary_entry(word): returns the dictionary entry (definition) for a given word from the 'pairings' attribute. Returns None if the word is not found in the 'pairings' attribute.
    """
    def __init__(self, words=()):
        # the tuple of words should ideally come from a list of words
        self.words = words
        # the pairings for the definition game
        self.pairings = {}
        # Load our dictionary library
        self.dictionary = PyDictionary()

    # This method returns a definition if it exists in the PyDictionary library
    # it will not return any words that do NOT have a definition in the dictionary
    def find_definitions(self):
        if len(self.words) != 0:
            for word in self.words:
                terms = self.dictionary.meaning(word)  # find the meaning of a word if it exists
                if terms is not None:  # if the word returns any values add it to the list of pairs
                    vals = terms.values()
                    self.pairings[word] = list(vals)[0][0]  # take the first (most commonly used) definition.
        return self.pairings  # return the definition-word matches

    # change a preexisting definition to a new one
    def modify_definition(self, word="", new_definition=""):
        self.pairings[word] = new_definition

    # return a dictionary term from a headword
    # if no match exists return nothing
    def get_dictionary_entry(self, word):
        if word in self.pairings.keys():
            return self.pairings[word]
        # return None if no matching term
        return None
