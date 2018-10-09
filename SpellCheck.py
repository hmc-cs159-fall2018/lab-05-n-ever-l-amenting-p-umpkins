from EditDistance import EditDistanceFinder
from LanguageModel import LanguageModel 
import spacy 
from spacy.tokenizer import Tokenizer

class SpellChecker():
    def __init__(self, channel_model=None, language_model=None, max_distance=100): 
        self.nlp = spacy.load("en", pipeline=["tagger", "parser"])
        self.channel_model = channel_model 
        self.language_model = language_model 
        self.max_distance = max_distance
        

    def load_channel_model(self, fp): 
        self.channel_model = EditDistanceFinder()
        self.channel_model.load(fp)
        

    def load_language_model(self, fp): 
        self.language_model = LanguageModel()
        self.language_model.load(fp)
        
    def bigram_score(self, prev_word, focus_word, next_word): 
        """
        takes 3 words and returns the average bigram probability of the first and last pair
        """
        return (self.language_model.bigram_prob(prev_word, focus_word) + self.language_model.bigram_prob(focus_word, next_word)) / 2

    def unigram_score(self, word): 
        """
        takes a word and returns the unigram probability
        """
        return self.language_model.unigram_prob(word)

    def cm_score(self, error_word, corrected_word): 
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

    def inserts(self, word):
        wordsFound = []
        wordLen = len(word)
        for v in self.language_model.vocabulary: 
            if v.isalpha() and len(v) == (wordLen + 1):
                if self.subseq(word, v):
                    wordsFound.append(v)
        return wordsFound

    def subseq(self, word1, word2):
        """
        returns true if word1 is a subsequence of word2  
        """
        for i in range(len(word1)):
            if (word1[i] not in word2):
                return False
            else: 
                index = word2.index(word1[i])
                word2 = word2[index+1:]
        return True 

    def deletes(self, word):
        wordsFound = []
        wordLen = len(word)
        for v in self.language_model.vocabulary:
            if v.isalpha() and len(v) == (wordLen - 1):
                if self.subseq(v, word):
                    wordsFound.append(v) 
        return wordsFound      

    def substitutions(self, word):
        """
        take a word as input and return a list of words (that are in the LanguageModel) that are 
        within one substitution of word.
        """
        subList = []
        wordLen = len(word)

        for candidate in self.language_model.vocabulary:
            if candidate.isalpha() and len(candidate) == wordLen:
                for i in range(wordLen):
                    candidateDel = candidate[:i] + candidate[i+1:]
                    wordDel = word[:i] + word[i+1:]
                    if candidateDel == wordDel:
                        if candidate not in subList:
                            subList.append(candidate)
                        break
        
        return subList
    
    def transpositions(self, word):
        """
        take a word as input and return a list of words in LanguageModel that 
        are within one substitution of the word.
        """
        wordsFound = []
        wordLen = len(word)
        for v in self.language_model.vocabulary:
            if v.isalpha() and len(v) == wordLen:
                transps = 0
                for i in range(wordLen-1):
                    if (word[i] == v[i+1] and word[i+1] == v[i]) and (word[i] != word[i+1]):
                        transps += 1
                    if transps >= 2:
                        break
                if transps == 1:
                    wordsFound.append(v)  
        return wordsFound 


    def generate_candidates(self, word):
        """
        returns a list of words within max_distance edits of the given word
        """
        words = {word}
        for i in range(self.max_distance):
            # find all words within edit distance 1 of the words currently in words
            new_words = set()
            for candidate in words:
                new_words |= set(self.inserts(candidate)) | set(self.deletes(candidate)) | set(self.substitutions(candidate)) | set(self.transpositions(candidate))
            words |= new_words
        if word not in self.language_model: # we started with word to generate first set of candidates, but we don't want it in the final return if it isn't actually a word
            words.remove(word)
        return list(words)

    def check_non_words(self, sentence, fallback=False):
        words = []
        for i in range(len(sentence)):
            if sentence[i] in self.language_model:
                words.append([sentence[i]])
            else:
                candidates = self.generate_candidates(sentence[i])
                prev_word = '<s>' if i == 0 else sentence[i - 1]
                next_word = '</s>' if i == len(sentence) - 1 else sentence[i + 1]
                candidates.sort(key=lambda x: 0.7*(0.7*self.bigram_score(prev_word, x, next_word) + 0.3*self.unigram_score(x)) + 0.3*self.cm_score(sentence[i], x), reverse=True)
                if fallback and not candidates:
                    candidates = sentence[i]
                words.append(candidates)
        return words

    def check_sentence(self, sentence, fallback=False):
        return self.check_non_words([''.join([char for char in token.text if char.isalpha()]) for token in sentence], fallback)

    def check_text(self, text, fallback=False): 
        """
        takes a string as input, tokenize and sentence segment it with spacy, 
        and then return the concatenation of the result of calling check_sentence 
        on all of the resulting sentence objects.
        """
        self.nlp.tokenizer = Tokenizer(self.nlp.vocab)
        doc = self.nlp(text.lower())
        result = []
        for sent in doc.sents:
            correctionList = self.check_sentence(sent, fallback)
            result.extend(correctionList)
        return result

    def autocorrect_sentence(self, sentence):
        """Take a tokenized sentence (as a list of words) as input, 
        call check_sentence on the sentence with fallback=True, and 
        return a new list of tokens where each non-word has been
         replaced by its most likely spelling correction
        """ 
        words = self.check_sentence(sentence, True)
        newSentence = []
        for i in range(len(sentence)):
            newSentence.append(words[i][0])
        return newSentence



    def autocorrect_line(self, line):
        """Take a string as input, tokenize and segment it with spacy, 
        and then return the concatenation of the result
        of calling autocorrect_sentence on all of the resulting sentence objects.
        """
        checkLines = self.check_text(line, True)
        newSentence = []
        for i in range(len(checkLines)):
            newSentence.append(checkLines[i][0])
        return ' '.join(newSentence)

    def suggest_sentence(self, sentence, max_suggestions): 
        
        words = self.check_sentence(sentence, True)
        newSentence = []
        for i in range(len(sentence)):
            if sentence[i].text in self.language_model:                
                newSentence.append(sentence[i].text)
            else:
                newSentence.append(words[i][0:max_suggestions])
        return newSentence

    def suggest_text(self, text, max_suggestions): 
        # checkLines = self.check_text(text, True)
        # newSentence = []
        # for i in range(len(checkLines)):
        #     if checkLines[i] in self.language_model:
        #         newSentence.append(checkLines[i])
        #     else:
        #         newSentence.append(checkLines[i][0:max_suggestions])
        # return newSentence
        self.nlp.tokenizer = Tokenizer(self.nlp.vocab)
        doc = self.nlp(text.lower())
        result = []
        for sent in doc.sents:
            # if sent.text in self.language_model:
            #     result.extend(sent.text) 
            # else:
            correctionList = self.suggest_sentence(sent, max_suggestions)
            result.extend(correctionList)
        return result
        
