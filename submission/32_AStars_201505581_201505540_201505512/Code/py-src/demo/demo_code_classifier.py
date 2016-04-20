import csv
from random import shuffle
import numpy as np
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import svm
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.datasets import load_svmlight_file
from sklearn.metrics import f1_score
from sklearn.externals import joblib
import sys
import warnings
import re
warnings.filterwarnings("ignore")

if len(sys.argv)!=3 :
    print "Provide the traing file"
    sys.exit(0)

with open(sys.argv[1],'rb') as f:   
        reader=csv.reader(f)
        l=list(reader)
with open(sys.argv[2],'rb') as f:
    reader=csv.reader(f,delimiter='|')
    l1=list(reader)
tagsdict={}

for i in l1:
    if i[0] not in tagsdict:
        tagsdict[i[0]]=1

alltitle=[]
alltags=[]
d={}
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

#print len(alltitle), len(l)       


count_vect = CountVectorizer(stop_words='english')
X_train_counts = count_vect.fit_transform(alltitle)     

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

clf = svm.SVC(kernel='linear')
clf.fit(X_train_tfidf, alltags)

while 1:

    title=raw_input('Title:')
    end=''
    print "Body: ",
    body=''
    for line in iter(raw_input,end):
        body=body+' '+line
    code=''
    print 'Code: '
    for line in iter(raw_input,end):
        code=code+' '+line
    #code=re.sub('[^a-zA-Z0-9#@]',"",code)    
    #code=code.lower()
    tags=raw_input( "Tags: ")

    alltitle.insert(0,code)
    count_vect = CountVectorizer(stop_words='english')
    X_train_counts = count_vect.fit_transform(alltitle)     

    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

    #print X_train_tfidf.shape, len(alltags)

    
    #clf.fit(X_train_tfidf,alltags)


    result=clf.predict(X_train_tfidf[0])
    # result=clf.predict(X_train_tfidf)

    #print len(result)
    print "Predicted Tag : ", result[0]
    alltitle.pop(0)
    #acc=accuracy_score(alltags[ind:], result)
    #prec=precision_score(alltags[ind:], result, average='macro')
    #rec=recall_score(alltags[ind:], result,  average='macro')
    #f1=f1_score(alltags[ind:], result,  average='macro')

    #print acc, prec, rec, f1

