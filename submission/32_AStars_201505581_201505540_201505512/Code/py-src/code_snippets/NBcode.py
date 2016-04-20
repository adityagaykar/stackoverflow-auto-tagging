import csv
from random import shuffle
import numpy as np
import sklearn
#from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import svm
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB

with open('code-tag-50k.out','rb') as f:   
        reader=csv.reader(f)
        l=list(reader)

with open('code_tags.in','rb') as f:
    reader=csv.reader(f,delimiter='|')
    l1=list(reader)
tagsdict={}

for i in l1:
    if i[0] not in tagsdict:
        tagsdict[i[0]]=1

alltitle=[]
alltags=[]
for data in l:
    s=data[0]
    s=s.split('#@#')    
    title=s[0]
    #alltitle.insert(-1,title)
    tags=s[1]
    tags=tags.split('|')
    for tag in tags:
        if tag in tagsdict:
            alltitle.insert(-1,title)
            alltags.insert(-1,tag)
            break


print len(alltitle), len(l)       

count_vect = CountVectorizer(stop_words='english')
X_train_counts = count_vect.fit_transform(alltitle)     

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)


print X_train_tfidf.shape, len(alltags)


clf = MultinomialNB()
#clf = BernoulliNB()
clf.fit(X_train_tfidf[:33000], alltags[:33000])

result=clf.predict(X_train_tfidf[33000:])

print len(result)

acc=accuracy_score(alltags[33000:], result)

print acc

