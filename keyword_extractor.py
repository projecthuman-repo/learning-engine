"""
author: The princeling Jay Edwards

This class handles extracting keywords and paragraphs from a text.
"""

from collections import Counter
import spacy


class ExtractText:

    # Download and load the spacy tokenizer for english
    def __init__(self):
        # Download English tokenizer
        spacy.cli.download("en_core_web_sm")
        # Load English tokenizer, tagger, parser and NER
        self.nlp = spacy.load("en_core_web_sm")

    # Return a list of keywords found in the text
    def get_keywords(self, text="", frequency=1):
        initial_keys = []
        doc = self.nlp(text)

        # find the entities in the text that are NOT text
        for entity in doc.ents:
            if str(entity.text).isalpha() and len(entity.text) > 2:
                initial_keys.append(entity.text)

        # find the tokens in the text that are pronouns, adjectives and nouns (these are good candidates for keys)
        # temporarily blocked off unless anyone finds it useful
        # for token in doc:
          #  if token.text in ['PROPN', 'ADJ', 'NOUN']:
           #     initial_keys.append(token.text)

        # remove repeat elements from the initial keywords
        initial_keys = sorted(list(set(initial_keys)))

        # this is for returning keywords when the frequency for keywords is higher than 1
        if frequency > 1:
            keywords = []
            word_frequencies = Counter(text.split()).items()
            for word in word_frequencies:
                if word[0] in initial_keys and word[1] > frequency:
                    keywords.append(word[0])
            return keywords
        # if no frequencies are returned, just use a default
        return initial_keys

    # Return a list of sentences detected
    def get_sentences(self, text=""):
        doc = self.nlp(text)
        sentences = list(doc.sents)
        return sentences

    # This function is quite simple, determine a list of paragraphs by splitting at  newlines
    # This needs to be better in the future as it may and certainly WILL cause issues. For now it will suffice.
    def get_paragraphs(self, text=""):
        if text is not None:
            return text.split('\n')
        return []
