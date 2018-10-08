from EditDistance import EditDistanceFinder
from LanguageModel import LanguageModel 
import spacy 

class SpellChecker():
    def __init__(channel_model=None, language_model=None, max_distance=100): 
        self.nlp = spacy.load("en", pipeline=["tagger", "parser"])
        self.channel_model = channel_model 
        self.language_model = language_model 
        self.max_distance = max_distance
        

    def load_channel_model(fp): 
        self.channel_model = EditDistanceFinder()
        self.channel_model.load(fp)
        

    def load_language_model(fp): 
        self.language_model = LanguageModel()
        self.language_model.load(fp)
        
    def bigram_score(prev_word, focus_word, next_word): 
        """
        takes 3 words and returns the average bigram probability of the first and last pair
        """
        return (self.language_model.bigram_prob(prev_word, focus_word) + self.language_model.bigram_prob(focus_word, next_word)) / 2

    def unigram_score(word): 
        """
        takes a word and returns the unigram probability
        """
    	return self.language_model.unigram_prob(word)

    def cm_score(error_word, corrected_word): 
        """
        gives the probability of a word having been transformed into a given erroneous form

        params
        ------
        error_word     - the observed misspelling
        corrected_word - the proposed corrected word

        returns
        -------
        prob           - the probability of the corrected word having been transformed into the error word
        """
    	return self.channel_model.prob(error_word, corrected_word)

    def inserts(word):
    	return 

    def deletes(word):
    	return 

    def substitutions(word):
    	return 

    def generate_candidates(word):
    	return

    def check_sentence(sentence, fallback=False): 
    	return 

    def check_sentence(sentence, fallback=False): 
    	return 

    def check_text(text, fallback=False): 
    	return 

    def autocorrect_sentence(sentence): 
    	return 

    def autocorrect_line(line):
    	return 

    def suggest_sentence(sentence, max_suggestions): 
    	return 

    def suggest_text(text, max_suggestions): 
    	return 
    	
