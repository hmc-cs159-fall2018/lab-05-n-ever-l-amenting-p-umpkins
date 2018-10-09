1. In Writeup.md, explain how Laplace smoothing works in general and how it is implemented in the EditDistance.py file. Why is Laplace smoothing needed in order to make the prob method work? In other words, the prob method wouldn’t work properly without smoothing – why?

Laplace smoothing works generally by adding 1 to all of the number of occurrences so that there is nothing with 0 probability. Specifically, in EditDistance.py, in line 68, we add .1 to every character we will come across so that none of the characters have a probability of 0. We do this for the prob method so that when we come across a character pair in our testing data that we haven't seen before, that pair still exists in `self.probs` so that all of our calculations work out. 

2. Describe the command-line interface for EditDistance.py. What command should you run to generate a model from /data/spelling/wikipedia_misspellings.txt and save it to ed.pkl?

It takes in two arguments of FileType, a source file to read from, and a store file to save to.

```python3 EditDistance.py --source "/data/spelling/wikipedia_misspellings.txt" --store "ed.pkl"```

3. What n-gram orders are supported by the given LanguageModel class?

The given LanguageModel class supports unigrams and bigrams.

4. How does the given LanguageModel class deal with the problem of 0-counts?

We add a value of 0.1 to every numerator and 0.1 times the length of the vocabulary to the denominator in order to avoid dividing by 0. 

5. What behavior does the “__contains__()” method of the LanguageModel class provide?

It allows you to use `in` as an operator to look up whether a word is in the vocabulary. 

6. Spacy uses a lot of memory if it tries to load a very large document. To avoid that problem, LanguageModel limits the amount of text that’s processed at once with the get_chunks method. Explain how that method works.

We specify how many bytes we want to read in for a single chunk, and while a chunk of that size exists in the file, it reads in some lines that are about that many bytes, making sure to end at a newline character. Then we join the lines in the chunk into a single string, and use the Python `yield` command to return an iterable. This way, when we iterate through each chunk, we only have to read in one chunk at a time from memory, avoiding memory issues.

7. Describe the command-line interface for LanguageModel.py. What command should you run to generate a model from /data/gutenberg/*.txt and save it to lm.pkl if you want an alpha value of 0.1 and a vocabulary size of 40000?

```python3 LanguageModel.py  --store 'lm.pkl' --alpha 0.1 --vocab 40000 /data/gutenberg/*.txt```

6. How often did your spell checker do a better job of correcting than ispell? Conversely, how often did ispell do a better job than your spell checker?

ispell did a much better job than our spell checker. 

7. Can you characterize the type of errors your spell checker tended to best at, and the type of errors ispell tended to do best at?

ispell was able to keep capitalization and punctuation, which our spell checker didn't do. With more time and effort (but we've spent hours on this already) we could probably check for this.  

8. Comment on anything else you notice that is interesting about spell checking – either for your model or for ispell.

Our spell checker didn't know the word edit. It would replace it with "exit" or "edict". It also didn't know the word "banned" and replaced it with banner. We think these words, "edit" and "banned", are less likely to be in these old texts we trained our language model on. 

We also noticed that using bigrams may not always work. For example, we kept getting "be" and "men" instead of "by" and "means" as our top choices. This is likely because "not be" and "any men" are very likely to occur. Perhaps trigrams would fix this, but would be much more computationally expensive. 


9. Describe your approach

We had a function similar to insert, delete and substitution that checked if a word was one transposition away from any word in the vocabulary, by iterating through the string, switching letters, and seeing if that new word was in the vocabulary. 

10. Give examples of how your approach works, including specific sentences where your new model gives a different (hopefully better!) result than the baseline model.

We didn't find any actual changes unfortunately. 

11. Discuss any challenges you ran into, design decisions you made, etc.

We kept the design similar to inserting, deleting and substituting. 
