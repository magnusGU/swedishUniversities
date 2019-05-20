from mrjob.job import MRJob
from collections import defaultdict
import tempfile
tempfile.tempdir = '/data/tmp'

class MRWordFreqCount(MRJob):
    def mapper(self, _, line):
        id,group,value = line.split()
        yield ("value",float(value))

    def reducer(self, key, values):
        l = []
        for _,v in enumerate(values):
            l.append(v)
        l.sort()

        interval = (l[-1] - l[0]) / 10
        thres = l[0] #+ interval
        d = defaultdict(float)
        #since these are not sorted, another approach is used

        for i in l:
            if i >= thres + interval:
                thres += interval
            d[thres] += 1
        for key in d:
            yield round(key,3), d[key]

if __name__ == '__main__':
    MRWordFreqCount.run()
