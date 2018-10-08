

class SpellChecker():
    def __init__(channel_model=None, language_model=None, max_distance): 
    	return 

    def load_channel_model(fp): 
    	return 

    def load_language_model(fp): 

    def bigram_score(prev_word, focus_word, next_word): 
    	return 

    def unigram_score(word): 
    	return 

    def cm_score(error_word, corrected_word): 
    	return

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
    	