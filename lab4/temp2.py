from mrjob.job import MRJob
from collections import defaultdict
import tempfile
tempfile.tempdir = '/data/tmp'

class MRWordFreqCount(MRJob):
    def mapper(self, _, line):
        id,group,value = line.split()
        yield ("value",float(value))

    def combiner(self, key, values):
        d = defaultdict(int)
        for _,v in enumerate(values):
            d[int(v)] += 1
        
        for key in d:
            yield key, d[key]

    def reducer(self, key, values):
        yield (key, sum(values))

if __name__ == '__main__':
    MRWordFreqCount.run()
