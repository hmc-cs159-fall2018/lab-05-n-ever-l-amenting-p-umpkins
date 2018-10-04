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

```python3 LanguageModel.py '/data/gutenberg/*.txt' --store 'lm.pkl' --alpha 0.1 --vocab 40000```