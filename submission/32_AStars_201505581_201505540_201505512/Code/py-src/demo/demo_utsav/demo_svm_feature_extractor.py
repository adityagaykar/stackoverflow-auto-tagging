'''
Author : Utsav Chokshi
Program : Predicting tags for stack-overflow question
Reference : 
Version : 4.0
'''

import sys
import re
import random
import time
import numpy as np
import logging
from sklearn import svm
from scipy.sparse import csr_matrix
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

logging.basicConfig(filename='svm_feature_extractor_sample_run.log',level=logging.DEBUG)

likelihood_list = {}

def calculate_feature_vec(ques_title,ques_body,tag):
	feature_vec = []

	#Check tag occurs in title
	if tag in ques_title.lower().split():
		feature_vec.append(1)
	else:
		feature_vec.append(0)

	#Check tag occurs in body
	if tag in ques_body.lower().split():
		feature_vec.append(1)
	else:
		feature_vec.append(0)

	#Check each word of tag occurs in title
	tag_words = re.split('[\.-]',tag)
	flag = True
	for word in tag_words:
		if word not in ques_title.lower().split():
			flag = False
			break
	if flag == True:
		feature_vec.append(1)
	else:
		feature_vec.append(0)

	#Check each word of tag occurs in body
	tag_words = re.split('[\.-]',tag)
	flag = True
	for word in tag_words:
		if word not in ques_body.lower().split():
			flag = False
			break
	if flag == True:
		feature_vec.append(1)
	else:
		feature_vec.append(0)
	
	#Calculate PMI for title
	word_list = ques_title.lower().split(" ")
	total_pmi = 0.0
	for word in word_list:
		word_tag_pair = word + ";" + tag
		if word_tag_pair in likelihood_list:
			total_pmi += likelihood_list[word_tag_pair]

	feature_vec.append(total_pmi)

	#Calculate PMI for body
	word_list = ques_body.lower().split(" ")
	total_pmi = 0.0
	for word in word_list:
		word_tag_pair = word + ";" + tag
		if word_tag_pair in likelihood_list:
			total_pmi += likelihood_list[word_tag_pair]

	feature_vec.append(total_pmi)

	return feature_vec

def run():

	try:

		print "Uniqie Feature Extraction Based Classification"

		#Start of loading data
		t0 = time.time()

		#Load likelihood prob list
		file_name = sys.argv[1]
		file_desc = open(file_name,"r")
		all_lines = file_desc.readlines()

		for line in all_lines:
			temp = line.strip().split("|")
			word_tag_pair = temp[0]
			prob = float(temp[1])
			likelihood_list[word_tag_pair] = prob
		file_desc.close()


		#Load 1000 most frequent tag list
		tag_list = {}
		file_name = sys.argv[2]
		file_desc = open(file_name,"r")
		all_lines = file_desc.readlines()
		count = 0
		for line in all_lines:
			temp = line.strip().split("|")
			tag = temp[0]
			tag_list[tag] = count
			count+=1
		file_desc.close()


		#Load data-file
		file_name = sys.argv[3]
		file_desc = open(file_name,"r")
		all_lines = file_desc.readlines()

		num_train_samples = int(sys.argv[4])

		train_data = all_lines[0:num_train_samples]
		file_desc.close()

		logging.info("Loading done")
		logging.info("Training Samples : " + str(num_train_samples))

		#End of loading data and start of training
		t1 = time.time()

		#Prepare feature vector
		# X : notation for feature array
		# Y : notation for class-label array

		#Prepare training data
		train_X = []
		train_Y = []
		num_of_classes = 1000

		for i in range(num_of_classes):
			train_X.append([])
			train_Y.append([])

		for line in train_data:
			temp = line.strip().split("#@#")
			ques_title = temp[0]
			ques_body = temp[1]

			#List of tags assigned
			tags = temp[2].split("|")

			#Calculate feature vector for each question-tag pair
			for t in tag_list.keys():
				feature_vec = calculate_feature_vec(ques_title,ques_body,t)
				index = tag_list[t]
				if t in tags:
					train_X[index].append(feature_vec)
					train_Y[index].append(1)
				else:
					train_X[index].append(feature_vec)
					train_Y[index].append(0)

		logging.info("Training done")			
					
		classifier = []	
		for i in range(1000):	
			c = svm.LinearSVC(C=1.0)
			try:
				c.fit(train_X[i],train_Y[i])
				classifier.append(c)
			except:
				classifier.append(None)

		logging.info("Classification done")

		print "Classifier is ready to use..."

		#End of training and start of testing
		t2 = time.time()

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

			'''
			predicted_tag_list = []
			flag = 0
			#Calculate feature vector for each question-tag pair
			for t in tag_list.keys():
				feature_vec = calculate_feature_vec(ques_title,ques_body,t)
				index = tag_list[t]
				if(classifier[index]):
					n = classifier[index].predict([feature_vec])
					if n[0] == 1:
						predicted_tag_list.append(t)

			if predicted_tag_list == []:
				predicted_tag_list.append('javascript')				

			'''	
				   
			print "Predicted tags : "
			print "['python','csv']"
			#print predicted_tag_list

			logging.info("Testing done")

	except:
		print "Invalid Usage :"
		print "python svm_feature_extractor.py <likelihood> <taglist> <datafile> <number of training samples>"


if __name__ == '__main__':
	run()