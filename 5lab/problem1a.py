import random
from pyspark import SparkContext
sc = SparkContext(master = 'local[4]')

distFile = sc.textFile("datasnippet.txt")
splitData = distFile.map(lambda l : l.split()).map(lambda t:float(t[2]))
count = splitData.count()
_sum = splitData.reduce(lambda a,b: a+b)
_expsum = splitData.map(lambda a: a**2).reduce(lambda a,b:a+b)
median = -1
ordered = splitData.takeOrdered(count)
if count % 2 == 0:
    median = (ordered[count//2] + ordered[count//2 - 1]) / 2
else:
    median = ordered[count//2]
_min = ordered[0]
_max = ordered[count-1]

interval = (_max - _min)
nrOfBins = 10
histogram = splitData.map(lambda a: (int(((a-_min)/interval)*nrOfBins),1)).reduceByKey(lambda a,b:a+b)

hg = histogram.collect()
hg[nrOfBins-1] += hg[nrOfBins]
del hg[nrOfBins]
avg = _sum / count
std = (_expsum/count - avg**2)**(0.5)
print("Count: ",count)
print("Avg: ",avg)
print("Standard deviation: ",std)
print("Median: ",median)
print("Min: ",_min)
print("Max: ",_max)
print(hg)