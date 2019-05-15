from mrjob.job import MRJob
from collections import defaultdict


class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        _id, group, value = line.split()
        #yield "id", data[0]
        #yield "group", data[1]
        yield "value", float(value)

    def __looper__(self, values):
        l = []
        total = 0
        
        return l.sort(), total, i

    def combiner(self, key, values):
        total = 0
        l = []
        #l, total, i = self.__looper__(values)
        for i, v in enumerate(values):
            l.append(v)
            total += v
        l.sort()
        interval = (l[-1] - l[0]) / 10
        thres = l[0]# + interval
        d = defaultdict(float)
		#
        for e in l:
            if e > thres + interval:
                thres += interval
            d[thres] += 1
        
        yield ("dict", (d,l[0],l[-1]))
        yield ("count", i)
        yield ("total",total)
        yield ("min", l[0])
        yield ("max", l[-1])
        
    def reducer(self, key, values):
        if key == 'dict':
            d = []
            l = []
            for i, v in enumerate(values):
                d.append(v[0])
                l.append(v[1])
                l.append(v[-1])
            l.sort()
            
            interval = (l[-1] - l[0]) / 10
            thres = l[0] #+ interval
            finalD = defaultdict(float)
            #since these are not sorted, another approach is used
            for dic in d:
                for key in dic:
                    for i in range(10):
                        if float(key) >= thres + interval*i and float(key) < thres + interval*(i+1):
                            #thres += interval
                            finalD[thres + interval*i] += dic[key]
            for key in finalD:
                yield round(key,3), finalD[key]
            yield 'min', l[0]
            yield 'max', l[-1]

        #if key == "min":
        #    l = []
        #    for i, v in enumerate(values):
        #        l.append(v)
        #    l.sort()
        #    yield key, l[0]
        #if key == "max":
        #    l = []
        #    for i, v in enumerate(values):
        #        l.append(v)
        #    l.sort()
        #    yield key, l[-1]
        


if __name__ == '__main__':
    MRWordFrequencyCount.run()
    