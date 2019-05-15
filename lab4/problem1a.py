from mrjob.job import MRJob
from collections import defaultdict


class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        _id, group, value = line.split()
        #yield "id", data[0]
        #yield "group", data[1]
        yield "value", float(value)


    def combiner(self, key, values):
        total = 0
        l = []
        for i, v in enumerate(values):
            l.append(v)
            total += v
        l.sort()
        interval = (l[-1] - l[0]) / 10
        thres = l[0] + interval
        d = defaultdict(float)
		#
        for e in l:
            if e > thres:
                thres += interval
            d[thres] += 1
        
        yield ("dict", d)
        yield ("count", i)
        yield ("total",total)
        yield ("min", l[0])
        yield ("max", l[-1])
        
    def reducer(self, key, values):
        yield "dead", True
        


if __name__ == '__main__':
    MRWordFrequencyCount.run()
    