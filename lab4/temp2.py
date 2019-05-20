from mrjob.job import MRJob
from collections import defaultdict
import tempfile
tempfile.tempdir = '/data/tmp'

class MRWordFreqCount(MRJob):
    def mapper(self, _, line):
        id,group,value = line.split()
        yield ("value",float(value))

    def reducer(self, key, values):
        d = defaultdict(float)
        interval = 1
        thres = 0
        for _,v in enumerate(values):
            for i in range(10):
                if v >= thres + interval*i and v < thres + interval*(i+1):
                    d[thres + interval*i] += 1
        
        for key in d:
            yield round(key,3), d[key]

if __name__ == '__main__':
    MRWordFreqCount.run()
