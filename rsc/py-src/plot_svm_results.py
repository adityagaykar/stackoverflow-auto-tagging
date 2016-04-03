import matplotlib.pyplot as plt
import sys
import numpy as np


x,y = [],[]
with open(sys.argv[1]) as f:
	for line in f.readlines():
		line = [float(i.strip()) for i in line.split(",")]
		x.append(line[0])
		y.append(float(line[-1]))
x = np.array(x)
y = np.array(y)
print x, y
plt.grid(True)
plt.axis([0, x.max()+5000, 0,100])
plt.bar(x,y,1000,color="blue",label="Accuracy")
plt.legend()
plt.show()

