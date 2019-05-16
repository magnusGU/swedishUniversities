from mrjob.job import MRJob
from collections import defaultdict
import time


class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        _id, group, value = line.split()
        yield "value", float(value)

    def combiner(self, key, values):
        total = 0
        total_2 = 0
        min_val = 100
        max_val = 0
        for i, v in enumerate(values):
            if(v > max_val):
                max_val = v
            if(v < min_val):
                min_val = v
            total += v
            total_2 += v**2
            yield('val',v)
        interval = (max_val - min_val) / 10
        thres = min_val
        d = defaultdict(float)
    
        for _,e in enumerate(values):
            if e > thres + interval:
                thres += interval
            d[thres] += 1
        
        yield ("dict", (d,min_val,max_val))
        yield ("total_count",(total,i+1,total_2))
        
    def reducer(self, key, values):
        if key == "total_count":
            total = 0
            count = 0
            total_2 = 0
            for _,tup in enumerate(values):
                total += tup[0]
                count += tup[1]
                total_2 += tup[2]
            avg = total / count
            exp = total_2 / count
            std = (exp - (avg**2))**(0.5)
            yield ("avg", avg)
            yield ("std",std)
            yield ("count",count)
        
        if key == 'val':
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
        


if __name__ == '__main__':
    start = time.time()
    MRWordFrequencyCount.run()
    end = time.time()
    print("Time spent: ", end-start)
    