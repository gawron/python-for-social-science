# -*- coding: utf-8 -*-
"""Insults_with_Naive_Bayes.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/gawron/python-for-social-science/blob/master/text_classification/Insults_with_Naive_Bayes.ipynb

## Analyzing insults with Naive Bayes: pandas and sklearn
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV as gs
import sklearn.feature_extraction.text as text
import sklearn.naive_bayes as nb
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score, recall_score
# %matplotlib inline

"""## Loading and preparing the data

Let's open the CSV file with `pandas`.
"""

import os.path
site = 'https://gawron.sdsu.edu/python_for_ss/course_core/book_draft/_static/'
df = pd.read_csv(os.path.join(site,"troll.csv"))

"""Each row is a comment  taken from a blog or online forum. There are three columns: whether the comment is insulting (1) or not (0), the data, and the unicode-encoded contents of the comment."""

df[['Insult', 'Comment']].tail()

"""Write a pandas command to give you just the insults."""

# Solution replaces df on the RHS
insult_df = df[df['Insult'] ==1]

insult_df[:25]

df['Comment'][79:85]

df['Comment'][79]

"""NB:  `insult_df` is **not** modified by the following sort."""

insult_df = df

insult_df['Size'] = df['Comment'].apply(len)
insult_df['Size'].sort_values(ascending = False)

"""Now we define the feature matrix $\mathbf{X}$ and the labels $\mathbf{y}$."""

len(insult_df.loc[3208]['Comment'].split())

insult_df.loc[755]

insult_df.loc[45]

y = df['Insult']

"""We want to use one of the linear classifiers in `sklearn`,
bit the learners in `sklearn` only work with numerical arrays. How to convert text into a matrix of numbers?
As discussed in lecture and in our text,
obtaining the feature matrix from the text is not trivial.

The classical solution is to first extract a **vocabulary**: a list of words used throughout the corpus. Then, we can count, for each document in the sample, the frequency of each word. We end up with a **sparse matrix**: a huge matrix containing mostly zeros. Here, `sklearn` and `pandas` make it possible to do this in two lines.
"""

print(text.TfidfVectorizer.__doc__)

tf = text.TfidfVectorizer()
X = tf.fit_transform(df['Comment'])

X.shape

"""
The TFIDF vectorizer uses a simple formula to assign a significance score to the
count of each vocabulary item in each document. Our TFIDF matrix is stored in `X`.

Say a word occurs n times in a document.
TFIDF is a very popular measure of the significance of that fact
first proven to be useful in
document retrieval.  It has some competitors in classification, but
we have used it here mainly because it's the easiest **feature weighting scheme**
to use in `sklearn`."""

# Shape and Number of non zero entries
print(f'Shape: ({X.shape[0]:,} x {X.shape[1]:,})  Non-zero entries: {X.nnz:,}')

"""There are 3,947 comments and 16,469 different words. Let's estimate the sparsity of this feature matrix."""

print(("The document matrix X is ~{0:.2%} non-zero features.".format(
          X.nnz / float(X.shape[0] * X.shape[1]))))

"""A `TdidfVectorizer` instance stores its `decode` dictionary in the attribute `vocabulary_` (note
the trailing underscore!):
"""

tf.vocabulary_['moron']

"""The `sklearn` module stores many of its internally computed arrays as **sparse matrices**.  This is basically a 
very clever computer science device for not wasting all the space that very sparse matrices 
waste.  Natural language representations are often **quite** sparse.  The .15% non zero features
firgure we just looked at was typical.  Sparse matrices come at a cost, however; although some
computations can be done while the matrix is in sparse form, some cannot, and to do those
you have to convert the matrix to a nonsparse matrix, do what you need to do, and then, probably,
convert it back.  This is costly.  We're going to do it now, but only because we're goofing
around. Conversion to non-sparse format should in general be avoided whenever possible.
"""

XA = X.toarray()

"""Consider Tweet 3942:"""

insult_df.loc[3942]['Comment']

"""Ok, now we can check the TFIDF matrix for the statistic for `'moron'` in this tweet:"""

XA[3942][8704]

"""Oh, maybe we didn't learn that:"""

tf.vocabulary_['morons']

"""Totally different word, found at a totally different place in XA:"""

XA[3942][8707]

"""## Training

Now, we are going to train a classifier as usual. We first split the data into a train and test set.
"""

am

"""We use a **Bernoulli Naive Bayes classifier**."""

bnb =nb.BernoulliNB()

bnb.fit(X_train, y_train);

bnb.score(X_test, y_test)

"""Now try re-executing the previous three cells.  The results shoudl be the same, right?

Well, are they?  

Ok, re-execute the same three cells again.  Now one more time.  Now try the following
piece of code:

#### Basic train and test loop
"""

def split_and_fit(X,Y,test_size=.2):
    (X_train, X_test,
       y_train, y_test) = train_test_split(X, y,
                                         test_size=test_size)
    bnb = nb.BernoulliNB()
    return bnb.fit(X_train, y_train),X_train, X_test, y_train,y_test

num_runs = 10
for test_run in range(num_runs):
    clf, X_train, X_test, y_train,y_test = split_and_fit(X,y)
    print('{0}'.format(clf.score(X_test, y_test)))

"""What's happening?  How should we deal this with this when we report our evaluations?

Explain the purpose of the code in the next cell.

#### Refined train and test loop
"""

num_runs = 100
#a_total = 0
#p_total = 0
#r_total = 0
#insults_total = 0

stats = np.zeros((4,))
for test_run in range(num_runs):
    clf, X_train, X_test, y_train,y_test = split_and_fit(X,y)
    #score = clf.score(X_test, y_test)
    predicted = clf.predict(X_test)
    y_array = y_test.values
    prop_insults = y_array.sum()/len(y_array)
    stats = stats + np.array([clf.score(X_test, y_test),
                              precision_score(predicted, y_test),
                              recall_score(predicted, y_test),
                              prop_insults])
    #p_score = precision_score(predicted, y_test)
    #r_score = recall_score(predicted, y_test)
    #a_total += score
    #p_total += p_score
    #r_total += r_score
    #insults_total += prop_insults
normed_stats = stats/num_runs
labels = ['Accuracy','Precision','Recall','Pct Insults']
for (i,s) in enumerate(normed_stats):
    print(f'{labels[i]} {s:.2f}')
#print('Accuracy {:.2%}'.format(a_total/num_runs))
#print('Precision {:.2%}'.format(p_total/num_runs))
#print('Recall {:.2%}'.format(r_total/num_runs))
#print('Avg Pct Insults {:.2%}'.format(insults_total/num_runs))

"""Let's take a look at the words corresponding to the largest coefficients (the words we find frequently in insulting comments)."""

dir(bnb)

bnb.feature_count_.shape

# We first get the words corresponding to each feature.
names = np.asarray(tf.get_feature_names())
# Next, we display the 50 words with the largest
# coefficients.
# NB Wajnt to switch over to using bnb.feature_count_.shape[0]
coefficient_matrix = bnb.coef_[0,:]
print(coefficient_matrix.shape)
# Sorting gives us smallest first, we reverse the order and take top 50
top_fifty_feat_indices = np.argsort(coefficient_matrix)[::-1][:50]
print((','.join(names[top_fifty_feat_indices])))

"""Finally, let's test our estimator on a few test sentences.

"""

predicted = bnb.predict(tf.transform([
    "I totally agree with you.",
    "You are so stupid.",
    "I love you."
    ]))

print(predicted)

print(predicted)
print(y_test[:3])

"""Not real impressive.  The word *stupid* was not recognized as an insult.

> You'll find all the explanations, figures, references, and much more in the book (to be released later this summer).

> [IPython Cookbook](http://ipython-books.github.io/), by [Cyrille Rossant](http://cyrille.rossant.net), Packt Publishing, 2014 (500 pages).
"""

print((bnb.predict(tf.transform([ "I totally agree with you.", "You are so stupid.", "I love you." ]))))

"""## Homework

Read the on line book draft chapter about doing the movie review data,
and try the clasifier used there, an SVM, on this data.  Be sure
top stick with the scikit learn (it has an SVM implementation).

Show your code, and print out results.  Which classifier does better?

#### Help with getting the movie reviews data.

Execute the next two cells.
"""

import nltk
nltk.download('movie_reviews')

from nltk.corpus import movie_reviews as mr

def get_get_file_strings (corpus, file_ids):
    return [corpus.words(file_id) for file_id in file_ids]

data = dict(pos = mr.fileids('pos'),
            neg = mr.fileids('neg'))

pos_file_ids = data['pos']
neg_file_ids = data['neg']

pos_file_ids[:5]

"""This illustrates how to get all the positive reviews."""

pos_file_reviews = get_get_file_strings (mr, pos_file_ids)
neg_file_reviews = get_get_file_strings (mr, neg_file_ids)

# First 20 words of first positive review
print(pos_file_reviews[0][:20])
print()
# First 20 words of second positive review
print(pos_file_reviews[1][:20])



"""After executing the code above, the names `pos_file_reviews` and `neg_file_reviews` each contain a list of reviews.  Each review is a list of words.  A list of word lists like `pos_file_reviews`  can be passed to `text.TfidfVectorizer()` via the `fit_transform` method to train a vectorizer for machine learning.

Just remember when testing the trained vectorizer use
`transform` in place of `fit_transform`.

What you will need to do to train the classifier (call it `clf`) is pass the matrix of vectorized training data
(you will call `X`) to `clf`'s
`fit(...)` method, along with an aligned sequence
of labels `y`.  By saying the two sequences are aligned, I mean this:  `X[i][:]` is the vector representation for a review that has the class 
`y[i]`.

The steps  are

1.  Create training data: a sequence of reviews (the code above did this) and an aligned sequence of review labels(each label is either `pos` or `neg`)  The training sequence should be a balanced mix of positive and negative reviews.

2.  Same procedure to create test data. Use 9 times as many training documents as test documnts (1000 positive reviews  + 1000 negative reviews means 1800 training examples and 200 test examples).

3.  Train and test the models multiple times and take the averege precision. recall and accuracy scores as the measure of your model's performance. The cells above labeled **Training and Test loops** illustrate this step.


The code cell below illustrates one way of 
getting randomly mixed data with
aligned labels (steps 1 and 2)

#### Help with steps 1 and 2
"""

# Lets work on letters instead of documents
# There are 2 classes, letters from the first half of the
# alphabet ('f') and letters frmm the last half ('l')

from random import shuffle
from string import ascii_lowercase
f_lets = ascii_lowercase[:13]
print(f_lets)
l_lets = ascii_lowercase[13:]
print(l_lets)
f_pairs = [(let,'f') for let in f_lets]
l_pairs = [(let,'l') for let in l_lets]
# Way too orderly, the classes arent mixed yet.
data = f_pairs + l_pairs
shuffle(data)
prepared_data, prepared_labels = zip(*data)
print(prepared_data)
print(prepared_labels)

"""###  Sumary for step 3:  The basic training of the vectorizer and the classifier."""

# what we did above
#tf = text.TfidfVectorizer()
#X = tf.fit_transform(df['Comment'])

#Edit the next line to train your TFIDF vectorizer
# of you training set
#X = tf.fit_transform(...)