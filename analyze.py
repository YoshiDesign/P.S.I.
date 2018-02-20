
import sys
from twython import Twython
from nltk.tokenize import TweetTokenizer
#from nltk.tokenize import tokenize


class Analyzer():
    """Implements tokenizer and sentiment analysis."""

    _pos_words_n = 0
    _neg_words_n = 0
    _pos_words = []
    _neg_words = []


    def __init__(self, positive, negative, stats):
        """Initialize Analyzer."""
        # This will store 2 lists / all_p and all_n words
        self.dict_words = {"pos" : [], "neg" : []}
        self.tokenizer = TweetTokenizer()
        #Building all_words dictionary
        with open(positive, "r") as fp:
            try:
                for item in fp:
                    if not item.startswith(";"):
                        self.dict_words["pos"].append(item.lower().strip())
            except RuntimeError:
                self.f_Err = 1
                stats.game_active = False
        """ 
            If game_active && f_Err -> start other game, perhaps
        """
        with open(negative, "r") as fp:
            try:
                for item in fp:
                    if not item.startswith(";"):
                        self.dict_words["neg"].append(item.lower().strip())
            except RuntimeError:
                self.f_Err = 1
                stats.game_active = False
        
        # ["I", "am", "a", "tweet"]
        #self.words = []
        self.pResult = []
        self.nResult = []
    

    def analyze(self, tweet):
        """ Sentiment Analyzer """

        # Proper tokenizing
        self.words = self.tokenizer.tokenize(tweet)
        #print("WORDS == {}".format(words))

        # Positive analysis
        for word in self.words:

            self.pResult = [item for item in self.dict_words["pos"] if item.strip() == word.lower().strip()]
            # Cache Data
            if self.pResult:
                self.track_words(p=self.pResult)

        # Negative analysis
        for word in self.words:
            self.nResult = [item for item in self.dict_words["neg"] if item.strip() == word.lower().strip()]
            # Cache Data
            if self.nResult:
                self.track_words(n=self.nResult)

        # Clean up the dict
        if Analyzer._pos_words_n > 0 or Analyzer._neg_words_n > 0:
            dict_words = {"pos" : [], "neg" : []}

        return self.words

    @classmethod
    def track_words(cls, p=[], n=[]):
        """ Center for Opinion Research """
        cls._pos_words_n += len(p)
        cls._neg_words_n += len(n)
        if p:
            for word in p:
                cls._pos_words.append(word)
        elif n:
            for word in n:
                cls._neg_words.append(word)

    # @staticmethod <-- Just in case I add prams to this class and begin to wonder
    def get_difficulty():
        """ Asshead meter """ 
        x = Analyzer._pos_words_n
        y = Analyzer._neg_words_n
        z = x + y
        return round(100 * (y / z))








            

