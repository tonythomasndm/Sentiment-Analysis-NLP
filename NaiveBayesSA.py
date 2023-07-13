# Sentiment Analysis using Naive Bayes
import nltk
nltk.download('movie_reviews')
#You will be implementing Naive Bayes classifier using NLTK which stands for Natural Language Toolkit. It is a library dedicated to NLP and NLU related tasks. NLTK's documentation- http://www.nltk.org/
from nltk.corpus import movie_reviews
import random
print(movie_reviews.categories())
# print(movie_reviews.fileids('neg'))
f = movie_reviews.open('neg/cv012_29411.txt')
d = f.read()
print(d)
f.close()
#You will construct a list of documents, labeled with the appropriate categories.
movie_reviews.words('neg/cv012_29411.txt')
documents = [(list(movie_reviews.words(fileid)), category)
              for category in movie_reviews.categories()
              for fileid in movie_reviews.fileids(category)]

random.shuffle(documents)
print(documents[0])
#Next, you will define a feature extractor for documents, so the classifier will know which aspects of the data it should pay attention too. In this case, you can define a feature for each word, indicating whether the document contains that word. To limit the number of features that the classifier needs to process, you start by constructing a list of the 2000 most frequent words in the overall corpus. You can then define a feature extractor that simply checks if each of these words is present in a given document.
# Define the feature extractor

all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
word_features = list(all_words)[:2000]

print(word_features)
def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    return features
#You have defined the feature extractor. Now, you can use it to train a Naive Bayes classifier to predict the sentiments of new movie reviews. To check your classifier's performance, you will compute its accuracy on the test set. NLTK provides show_most_informative_features() to see which features the classifier found to be most informative.
# Train Naive Bayes classifier
featuresets = [(document_features(d), c) for (d,c) in documents]
train_set, test_set = featuresets[100:], featuresets[:100]
classifier = nltk.NaiveBayesClassifier.train(train_set)
featuresets[0]
# Test the classifier
print(nltk.classify.accuracy(classifier, test_set))
# Show the most important features as interpreted by Naive Bayes
classifier.show_most_informative_features(5)