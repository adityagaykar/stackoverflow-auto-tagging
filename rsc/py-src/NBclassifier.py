import csv
from random import shuffle
import numpy as np
import sklearn
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB

def compute(k):
	with open('title-index/title-tag-'+k+'k.out','rb') as f:   
	        reader=csv.reader(f)
	        l=list(reader)


	alltags=[]
	alltitle=[]
	for data in l:
		s=data[0]
		s=s.split('#@#')    
		title=s[0]
		alltitle.insert(-1,title)
		tags=s[1]
		tags=tags.split('|')
		alltags.insert(-1,tags)



	alltags.reverse()
	alltitle.reverse()
	alltags=MultiLabelBinarizer().fit_transform(alltags)


	count_vect = CountVectorizer(stop_words='english')
	X_train_counts = count_vect.fit_transform(alltitle)


	tfidf_transformer = TfidfTransformer()
	X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)


	print X_train_tfidf.shape, alltags.shape


	#clf = OneVsRestClassifier(MultinomialNB())
	clf = OneVsRestClassifier(BernoulliNB())
	clf.fit(X_train_tfidf, alltags)
	#MultinomialNB(alpha=1.0, class_prior=None, fit_prior=False)
	BernoulliNB(alpha=1.0, class_prior=None, fit_prior=False)


	result=clf.predict(X_train_tfidf)

	cnt=0
	for i in range(len(l)):
		for j in range(len(result[i])):
			if result[i][j] and alltags[i][j]:
				cnt+=1
				break

	print cnt, (cnt/float(len(l)))*	100		

for k in [35, 40, 45, 50]:
	print " For k = ", k
	compute(str(k))
# for i in result[0]:
# 	if i==1:
# 		print i
