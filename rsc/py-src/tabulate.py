import sys
import math
primary_index = "/Users/adityagaykar/Dropbox/Development/MtechCSE/Sem2/SMAI/Stackoverflow-auto-tagging/backup/body-10k-post-index/primary.in"
secondary_index = "/Users/adityagaykar/Dropbox/Development/MtechCSE/Sem2/SMAI/Stackoverflow-auto-tagging/backup/body-10k-post-index/secondary.in"

primary_file_name = str(primary_index)
secondary_file_name = str(secondary_index)

primary_file_desc = open(primary_file_name,'r')
secondary_file_desc = open(secondary_file_name,'r')

output_file_desc = open("rare_features.in",'w')
#logging.basicConfig(filename='likelihood.log',level=logging.DEBUG)

#logging.info("Tag Index Processing Started.")

#logging.info("Tag Index Processing ended.")

#logging.info("Writing to likelihood.in Started.")
count=0
data = dict()
N = 0
for line in secondary_file_desc.readlines():
	temp = line.strip().split(":")
	word = str(temp[0])
	offset = int(temp[1].split(";")[0])
	primary_file_desc.seek(offset)
	temp = primary_file_desc.readline().split(";")
	# use word vs temp list to calculate Idf
	data[word] = len(temp)
	N += len(temp)	

for k in data.keys():
	data[k] = math.log(N/data[k])

important_terms = sorted(data.items(), key=lambda x: x[1], reverse=True)

features = []
limit = 20000
for t in important_terms:
	features.append(t[0])
	limit -= 1
	if limit == 0:
		break;
features.sort()

for t in features:	
	output_file_desc.write(t+"\n")
output_file_desc.close()

#logging.info("Number of word;tag pairs : " + str(count))
#logging.info("Writing to likelihood.in ended.")