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
        yield ("total_count",(total,i))
        yield ("min", l[0])
        yield ("max", l[-1])
        
    def reducer(self, key, values):
        if key == "total_count":
            total = 0
            count = 0
            for _,tup in enumerate(values):
                total += tup[0]
                count += tup[1]
            avg = total / count
            yield ("avg", avg)
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
            for dic in d:
                for key in dic:
                    if float(key) > thres + interval:
                        thres += interval
                    finalD[thres] += dic[key]
            for key in finalD:
                yield key, finalD[key]
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
    