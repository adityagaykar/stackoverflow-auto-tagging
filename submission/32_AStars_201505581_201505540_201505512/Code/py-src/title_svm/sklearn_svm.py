import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, HashingVectorizer
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.multiclass import OneVsRestClassifier
from sklearn import preprocessing
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import recall_score, precision_score,accuracy_score, f1_score,confusion_matrix
import warnings
warnings.filterwarnings("ignore")
import random
import sys


X_train = []
Y_train = []
X_test = []
actual = []
test_labels = []
total_train_data = 0.0
with open(sys.argv[1]) as f:
	for line in f.readlines():
		X_test.append(line.split("#@#")[0])		
		test_labels.append([i.strip() for i in line.split("#@#")[1].split("|")])

with open(sys.argv[2]) as f:
#with open("title-index/title-tag-5k.out") as f:
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
    ('vectorizer', CountVectorizer(stop_words='english')),
    ('tfidf', TfidfTransformer()),
    ('clf', OneVsRestClassifier(LinearSVC()))])


#random.shuffle(X_test)
classifier.fit(X_train, Y)
predicted = classifier.predict(X_test)
all_labels = lb.inverse_transform(predicted)

i = 0
c = 0
true_val = []
predicted = []
flag,flag2 = 0,0
for item, labels in zip(X_test, all_labels):
	#print labels,"\t ==> \t",test_labels[i]
	labels = set(labels)
	x_text = set(test_labels[i])
	#print labels,test_labels[i]
	if len(list(x_text.intersection(labels))) > 0:
		if flag == 0:
			true_val.append("1")
			predicted.append("1")
			flag = 1
		else:
			true_val.append("0")
			predicted.append("0")
			flag = 0
		c+=1
	else:
		if flag2 == 0:
			true_val.append("1")
			predicted.append("0")
			flag2 = 1
		else:
			true_val.append("0")
			predicted.append("1")
			flag2 = 0
	i+=1

actual_acc = accuracy_score(test_labels, all_labels) * 100
prici = precision_score(test_labels, all_labels, average="samples")
recall =  recall_score(test_labels, all_labels, average="samples")
f1_score = f1_score(test_labels, all_labels, average="samples")

print total_train_data,"\t",(float(c)/float(i))*100,"\t",actual_acc,"\t",prici,"\t",recall,"\t",f1_score
