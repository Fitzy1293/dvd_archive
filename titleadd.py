import os
from operator import itemgetter
from pprint import pprint

path = os.getcwd()
#we shall store all the file names in this list
filelist = []

for root, dirs, files in os.walk(path):
	for file in files:
        #append the file name to the list
		filelist.append(os.path.join(root,file))

#print all the file names
titleTxtPaths = [name for name in filelist if name.endswith('Titles.txt')]


titleTuples = []
for path in titleTxtPaths:
    dvdNum = int(path.split('/')[-2].replace('DVD_', ''))

    titles = open(path, 'r+').read().splitlines()
    titleTuples.append((dvdNum, titles))

sortedTups = sorted(titleTuples, key=lambda x: x[0])

with open('Find Videos With This File.txt', 'w+') as f:
    for i in sortedTups:
        f.write('DVD ' + str(i[0]) + '\n')
        for j in i[1]:
            f.write('\t' + j + '\n')
        f.write('\n')
