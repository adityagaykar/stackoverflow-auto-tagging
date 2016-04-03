import sys
import random
import numpy as np
import json

def get_likelihood(data, param_index, param, class_val):
	count = 1
	class_count = 1
	#print class_val
	for line in data:
		if param == line[param_index] and class_val == line[-1]:
			count += 1
		if class_val == line[-1]:
			class_count += 1	
	return float(count)/float(class_count)

data = []
with open(sys.argv[1]) as f:
	for line in f.readlines():
		line = line.strip()
		parts = line.split("#@#")
		train = parts[0].split(":")
		train_class = parts[1].split("|")
		
		for tc in train_class:
			tmp = train[:]
			tmp.append(tc)
			data.append(tmp)
			#print tmp[-5:]
	#data = [ i.strip().split(";") for i in f.readlines() ]
print "data read complete"
#data = data[1:]
likelihoods = []
def nav_bayes(id):
	random.shuffle(data)
	training = data[:-1000]
	testing = data[-1000:]

	#['job', 'marital', 'education', 'default', 'housing', 'loan', 'contact', 'month', 'poutcome', 'y']

	# calculating prior
	prior = dict()
	evidence = 0.0 # sum of prod(likelihood * prior)

	vals = dict()
	vals["total"] = 0
	for j in range(len(training)):
		if vals.has_key(training[j][-1]) :
			vals[training[j][-1]] += 1
		else :
			vals[training[j][-1]] = 1
		vals["total"] += 1

	for key in vals.keys():
		if key != "total":
			prior[key] = float(vals[key])/float(vals["total"])

	classes = [ i for i in vals.keys() if i != "total"]

	#generate likelihood matrix

	likelihood = dict()

	for c in classes:
		likelihood[c] = dict()
		for train in training:
			for i in range(len(train)-1):
				if likelihood[c].has_key(train[i]) == False:
					likelihood[c][train[i]] = get_likelihood(training, i, train[i], c)				


	likelihoods.append(likelihood)

	correct = 0
	wrong = 0
	confusion_mat = dict()
	for test_case in testing:
		class_likelihood = []
		evidence = 0.0
		for curr_class in classes:
			total_likelihood = 1.0
			for t in range(len(test_case) - 1):	
				total_likelihood *= likelihood[curr_class][test_case[t]]
				#total_likelihood *= get_likelihood(training, t, test_case[t], curr_class)
			curr_likelihood = total_likelihood * prior[curr_class]
			class_likelihood.append(curr_likelihood)
			evidence += curr_likelihood
		class_prob = [0.0] * len(classes)
		for c in range(len(classes)):
			class_prob[c] = float(class_likelihood[c])/float(evidence)
		class_prob = np.array(class_prob)
		#print class_prob
		predicted_class = classes[np.argmax(class_prob)]
		print "Predicted : ", predicted_class, " | actual : ", test_case[-1]
		if(predicted_class == test_case[-1]):
			correct += 1
		else:
			wrong += 1
			# if wrong < 4:
			# 	print class_prob
			# 	print test_case
		# if confusion_mat.has_key(test_case[-1]):
		# 	if confusion_mat[test_case[-1]].has_key(predicted_class):
		# 		confusion_mat[test_case[-1]][predicted_class] += 1
		# 	else:
		# 		confusion_mat[test_case[-1]][predicted_class] = 1
		# else:
		# 	confusion_mat[test_case[-1]] = dict()
		# 	confusion_mat[test_case[-1]][predicted_class] = 1

	# print "\nConfusion matrix : ",id
	# mat_keys = confusion_mat.keys()
	# sprint = ""
	# for k in mat_keys:
	# 	sprint += "\t"+k
	# print sprint
	# for k in mat_keys:
	# 	sprint = k
	# 	for k1 in mat_keys:
	# 		sprint +="\t"+str(confusion_mat[k][k1])
	# 	print sprint

	acc = 100*(float(correct)/ float(correct + wrong))
	# print "Corrects : ", correct
	# print "Wrongs   : ", wrong
	# print "Accuracy : ", acc
	return acc	

accs = []
prints = []
for i in range(1):
	tmp= nav_bayes(i+1)
	prints.append(str(i+1)+"\t"+str(tmp))
	accs.append(tmp)
print "\n\nSr.no","\t","Accuracy"
for p in prints:
	print p

accs = np.array(accs)
print "\nMean : ", accs.mean()
print "\nStandard deviation : ", accs.std()
print "Best accuracy : ", np.max(accs)
#print "Best model : ",json.dumps(likelihoods[np.argmax(accs)], indent=4)




