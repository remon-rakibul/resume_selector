from sklearn.datasets import load_files
from nltk.corpus import stopwords
import numpy as np
import pickle
import nltk
import re
#nltk.download('stopwords')

reviews = load_files('dataset/')
X, y = reviews.data, reviews.target
'''
with open('X.pickle', 'wb') as f:
    pickle.dump(X, f)
with open('y.pickle', 'wb') as f:
    pickle.dump(y, f)
    
with open('X.pickle', 'rb') as f:
    X = pickle.load(f)
with open('y.pickle', 'rb') as f:
    y = pickle.load(f)
''' 
corpus = []
for i in range(len(X)):
    review = str(X[i]).lower()
    review = re.sub(r"\\n|\\r|\\xef|\\xbb|\\xb|\\x|\\x0|'b'|\*|b'|/|\(|\)", ' ', review)
    review = re.sub(r'@#\$%&\*\(\)\<\>?\'\":;\]\[-]/', ' ', review)
    review = re.sub(r"'|,|\t", ' ', review)
    review = re.sub(r'\s+[a-z]\s+', ' ', review)
    review = re.sub(r'^[a-z]\s+', ' ', review)
    review = re.sub(r'\s+f', ' ', review)
    review = re.sub(r'\s+', ' ', review)
    corpus.append(review)

from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(max_features=500, min_df=3, max_df=0.6, stop_words=stopwords.words('english'))
X = vectorizer.fit_transform(corpus).toarray()

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression()
classifier.fit(X_train, y_train)

prediction = classifier.predict(X_test)

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, prediction)


with open('classifier.pickle', 'wb') as f:
    pickle.dump(classifier, f)
    
with open('tfidfmodel.pickle', 'wb') as f:
    pickle.dump(vectorizer, f)
    
    
with open('classifier.pickle', 'rb') as f:
    clf = pickle.load(f)
    
with open('tfidfmodel.pickle', 'rb') as f:
    tfidf = pickle.load(f)
    
sample = ['working as a software engineer for 5 years']
sample = tfidf.transform(sample).toarray()
print(clf.predict(sample))

sample2 = ['marketing officer and head of sales manager for a year']
sample2 = tfidf.transform(sample2).toarray()
print(clf.predict(sample2))