# Naive Bayer Classifier

As an assignment of AI course, we iplemented this text classifier. The link for the data used during development and tests can be found below. It contains distinct reviews about different movies, ranked as positive or negative so we can actually understand whether our algorithm works or not. We only used data from neg and pos folders for supervised learning. We splited up thw train folder randomly; 90% of the data for the training and 10% for the development. 
Inside the code you will find m and hyper-parameters, the meaning of which is: From the current dictionary skip the first n words and then keep the next m words. We tried different values for them and we also run the train and development process for different percentages of the total data. This is the learning graph of our algorithm for m = 100 and n = 300:

Also here is the graph showing the best Recall, Precision and F_1 values, reached by our algorithm for m = 200 and n = 100:



# Data Link

https://ai.stanford.edu/~amaas/data/sentiment/