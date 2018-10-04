1. In Writeup.md, explain how Laplace smoothing works in general and how it is implemented in the EditDistance.py file. Why is Laplace smoothing needed in order to make the prob method work? In other words, the prob method wouldn’t work properly without smoothing – why?

Laplace smoothing works generally by adding 1 to all of the number of occurrences so that there is nothing with 0 probability. Specifically, in EditDistance.py, 

2. Describe the command-line interface for EditDistance.py. What command should you run to generate a model from /data/spelling/wikipedia_misspellings.txt and save it to ed.pkl?
