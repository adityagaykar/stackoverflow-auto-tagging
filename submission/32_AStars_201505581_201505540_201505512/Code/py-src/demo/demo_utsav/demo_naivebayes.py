import sys
import math
import heapq
import logging
import re
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from scipy.sparse import csr_matrix

print 'Index dump based Simple Naive Bayes Approach'

#test_file_name = str(sys.argv[1])
#test_file_desc = open(test_file_name,'r')

prior_file_name = str(sys.argv[1])
prior_file_desc = open(prior_file_name,'r')

likelihood_file_name = str(sys.argv[2])
likelihood_file_desc = open(likelihood_file_name,'r')

logging.basicConfig(filename='naivebayes.log',level=logging.DEBUG)

logging.info("Processing Prior Index started.")
prior_dict={}
for line in prior_file_desc.readlines():
	temp = line.split("|")
	tag = str(temp[0])
	prob = float(temp[1])
	prior_dict[tag] = prob 
logging.info("Processing Prior Index ended.")


logging.info("Processing Likelihood Index started.")
likelihood_dict={}
for line in likelihood_file_desc.readlines():
	temp = line.split("|")
	tag_word = str(temp[0])
	prob = float(temp[1])
	likelihood_dict[tag_word] = prob 
logging.info("Processing Likelihood Index ended.")

print "Classifier is ready to use..."

while True:

	end = ''
	
	print "Enter title : "
	ques_title = str(raw_input())
	ques_title = re.sub("[^a-zA-Z0-9#@]"," ",ques_title)
	ques_title = ques_title.lower()
	
	print "Enter body : "
	ques_body = ''
	for line in iter(raw_input,end):
		ques_body = ques_body + ' ' + line
	ques_body = re.sub("[^a-zA-Z0-9#@]"," ",ques_body)
	ques_body = ques_body.lower()	 
	
	print "Enter code : "
	ques_code=''
	for line in iter(raw_input,end):
		ques_code = ques_code + ' ' + line 
	ques_code = re.sub("[^a-zA-Z0-9#@]"," ",ques_code)
	ques_code = ques_code.lower()	 
	
	print "True tags : "
	tags = str(raw_input())

	title_words = ques_title.strip().split()

	assigned_tags = []
	for tag in prior_dict.keys():
		logging.info("Processing tag : " + str(tag))
		total_prob = 0.0
		prior_prob =  prior_dict[tag]
		for word in title_words:
			logging.info("Processing title word : " + str(word))
			key = word+";"+tag
			if key in likelihood_dict:
				prob = prior_prob*likelihood_dict[key]
			else:
				prob = 0.0
			total_prob += prob
		assigned_tags.append((total_prob,tag))

	predicted_tags = heapq.nlargest(3,assigned_tags)
	assigned_tags = [tag[1] for tag in predicted_tags]

	print "Predicted tags : "
	print assigned_tags
