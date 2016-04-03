import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, HashingVectorizer
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.multiclass import OneVsRestClassifier
from sklearn import preprocessing
from sklearn.naive_bayes import MultinomialNB
import random
import sys

X_train = []
Y_train = []
X_test = []
actual = []
test_labels = []
total_train_data = 0.0
with open("/Users/adityagaykar/Dropbox/Development/MtechCSE/Sem2/SMAI/Stackoverflow-auto-tagging/backup/titles-tag.out") as f:
	for line in f.readlines():
		X_test.append(line.split("#@#")[0])		
		test_labels.append([i.strip() for i in line.split("#@#")[1].split("|")])

with open(sys.argv[1]) as f:
	c = 1
	for line in f.readlines()[:-1]:
		parts  = line.split("#@#")
		X_train.append(parts[0])		
		Y_train.append([ i.strip() for i in parts[1].split("|")])
		# if c % 10000 == 0:
		# 	print "lines read = ",str(c)
		c+=1

total_train_data = c

lb = preprocessing.MultiLabelBinarizer() #preprocessing.LabelBinarizer()
Y = lb.fit_transform(Y_train)

classifier = Pipeline([
    ('vectorizer', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', OneVsRestClassifier(MultinomialNB()))])


#random.shuffle(X_test)
classifier.fit(X_train, Y)
predicted = classifier.predict(X_test)
all_labels = lb.inverse_transform(predicted)

i = 0
c = 0
for item, labels in zip(X_test, all_labels):
	labels = set(labels)
	x_text = set(test_labels[i])
	if len(list(x_text.intersection(labels))) > 0:
		c+=1
	i+=1
    #print '%s => %s' % (item, ', '.join(labels))
#print "True classified : ",c
#print "Total : ",i
#print "Accuracy : ", float(c)/float(i)
#print "================================="
print total_train_data,",",c,",",i,",",(float(c)/float(i))*100
