import numpy as np
import pandas as pd
import json

class Wordle():
    """
    Parameters
    ----------
    must_have_letters: dict
        dictionary containing a letter key and optional position value.
        if the position of the letter is unknown, set the value to None.
    must_not_have_letters: list
        A list of letters that can be excluded from the search.
    """
    def __init__(self,
                 must_have_letters: dict,
                 must_not_have_letters: list):
        self.must_have_letters = must_have_letters
        self.must_not_have_letters = must_not_have_letters
        
    def get_5_letter_words(self):
        with open('dictionary_compact.json', 'r') as f:
            words = pd.Series(json.load(f).keys())
        return list(words[words.str.len() == 5].values)
    
    def shortlist_must_haves(self):
        """Find words with the required letters
        """
        five_letter_words = self.get_5_letter_words()
        word_shortlist = []
        for word in five_letter_words:
            word = word.lower()
            got_must_haves = 0
            for letter in self.must_have_letters.keys():
                got_must_haves += (letter in word) * 1
            if got_must_haves == len(self.must_have_letters):
                word_shortlist.append(word)
        return word_shortlist
    
    def _filter_dict(self):
        """Filter dictionary to leave only letters with a
        known location.
        """
        loc_dict = {}
        for k, v in self.must_have_letters.items():
            if v != None:
                loc_dict[k] = v
        return loc_dict
    
    def shortlist_by_location(self):
        """Second run over the shortlist specifying 
        the correct location of a word if known.
        """
        words = self.shortlist_must_haves()
        loc_dict = self._filter_dict()
        words_to_remove = []
        for word in words:
            for k, v in loc_dict.items():
                if word[v] != k:
                    words_to_remove.append(word)
        for word in np.unique(words_to_remove):
            words.remove(word)
        return words
    
    def shortlist_must_not_have(self):
        """Return words not containing excluded letters.
        """
        shortlist = self.shortlist_by_location()
        words_to_remove = []
        for word in shortlist:
            word_removed = False
            for letter in self.must_not_have_letters:
                if (letter in word) & (word_removed == False):
                    words_to_remove.append(word)
                    word_removed = True
        for word in words_to_remove:
            shortlist.remove(word)
        return shortlist
    
    def get_help(self):
        """Function pulls the above together, returns final shortlist.
        """        
        return self.shortlist_must_not_have()