import matplotlib.pyplot as plt
import sys
import numpy as np


x,acc,preci,recall,f_score,ac_acc = [],[],[],[],[],[]
with open(sys.argv[1]) as f:
	for line in f.readlines():
		line = [float(i.strip()) for i in line.split("\t")]
		x.append(line[0])
		acc.append(line[1])
		ac_acc.append(line[2])
		preci.append(line[3])
		recall.append(line[4])
		f_score.append(float(line[5]))

x = np.array(x)
y = np.array(acc)

plt.grid(True)
plt.axis([0, x.max()+5000, 0,80])
plt.bar(x,y,1000,color="blue",label="Accuracy")
plt.xlabel("Number of training samples")
plt.ylabel("Atleast one Accuracy(%)")
plt.legend()
plt.savefig("svm_results/svm_accuracy.png")
plt.clf()

y = np.array(ac_acc)
plt.grid(True)
plt.axis([0, x.max()+5000, 0,10])
plt.bar(x,y,1000,color="blue",label="Accuracy")
plt.xlabel("Number of training samples")
plt.ylabel("Set equal Accuracy(%)")
plt.legend()
plt.savefig("svm_results/svm_actual_accuracy.png")
plt.clf()

y = np.array(preci)
plt.grid(True)
plt.axis([0, x.max()+5000, 0.0,1.0])
plt.bar(x,y,1000,color="blue",label="Precision")
plt.xlabel("Number of training samples")
plt.ylabel("Precision")
plt.legend()
plt.savefig("svm_results/svm_pricision.png")
plt.clf()

y = np.array(recall)
plt.grid(True)
plt.axis([0, x.max()+5000, 0.0,1.0])
plt.bar(x,y,1000,color="blue",label="Recall")
plt.xlabel("Number of training samples")
plt.ylabel("Recall")
plt.legend()
plt.savefig("svm_results/svm_recall.png")
plt.clf()

y = np.array(f_score)
plt.grid(True)
plt.axis([0, x.max()+5000, 0.0,1.0])
plt.bar(x,y,1000,color="blue",label="F1 Score")
plt.xlabel("Number of training samples")
plt.ylabel("F1 Score")
plt.legend()
plt.savefig("svm_results/svm_f1_score.png")
plt.clf()


