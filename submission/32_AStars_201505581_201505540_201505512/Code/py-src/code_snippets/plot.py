import numpy as np
import matplotlib.pyplot as plt

N = 10
ind = np.arange(N)  # the x locations for the groups
width = 0.2      # the width of the bars

fig = plt.figure()
ax = fig.add_subplot(111)

#yvals = [4, 9, 2,5]
svm=[29.9, 30.35, 28.82, 28.97, 30.10, 30.07, 30.29, 31.52, 32.13, 31.98]
rects1 = ax.bar(ind, svm, width, color='r')
#zvals = [1,2,3,5]
bnb=[19.14, 15.82, 16.08, 15.5, 16.92, 18.89, 17.18, 19.3, 19.01, 20.02]
rects2 = ax.bar(ind+width, bnb, width, color='g')
#kvals = [11,12,13,5]
mnb=[23.33, 22.63, 25.94, 23.49, 24.56, 25.87, 25.4, 27.58, 26.69, 27.66]
rects3 = ax.bar(ind+width*2, mnb, width, color='b')

ax.set_ylabel('Accuracy')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('5k', '10k', '15k', '20k', '25k', '30k', '35k', '40k', '45k', '50k') )
ax.legend( (rects1[0], rects2[0], rects3[0]), ('SVM', 'BernoulliNB', 'MultinomialNB') )

def autolabel(rects):
    for rect in rects:
        h = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*h, '%d'%int(h),
                ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)
plt.axis([-1,10,0,50])
plt.show()