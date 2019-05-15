from mrjob.job import MRJob


class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        _id, group, value = line.split()
        #yield "id", data[0]
        #yield "group", data[1]
        yield "value", float(value)


    def reducer(self, key, values):
        total = 0
        l = []
        for i, v in enumerate(values):
            l.append(v)
            total += v
        l.sort()
        avg = total / i
        median = 0
        length = len(l)
        if length % 2 == 0:
            median = (l[length//2] + l[length//2 - 1]) / 2
        else:
            median = l[length // 2]
        yield ("avg",avg)
        yield ("min", l[0])
        yield ("max", l[-1])
        yield ("median", median)
        

    
        


if __name__ == '__main__':
    MRWordFrequencyCount.run()
    