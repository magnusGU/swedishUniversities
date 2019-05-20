from mrjob.job import MRJob
import tempfile
tempfile.tempdir = '/data/tmp'

class MRWordFreqCount(MRJob):
    def mapper(self, _, line):
        id,group,value = line.split()
        yield ("value",float(value))
    def combiner(self, word, counts):
        total = total_2 = max_val = 0
        min_val = 100
        for i,v in enumerate(counts):
            total += v
            total_2 += v**2
            if(v > max_val):
                max_val = v
            if(v < min_val):
                min_val = v
        yield("min",min_val)
        yield("max",max_val)
        yield("total_count",(total,i+1,total_2))

    def reducer(self, key, values):
        if key == 'total_count':
            total = count = total_2 = 0
            for _,tup in enumerate(values):
                total += tup[0]
                count += tup[1]
                total_2 += tup[2]
            avg = total / count
            exp = total_2 / count
            std = (exp - (avg**2))**(0.5)
            yield("average",avg)
            yield("standard deviation",std)
            yield("count",count)
        elif key == "min":
            yield(key,min(values))
        elif key == "max":
            yield(key,max(values))

if __name__ == '__main__':
    MRWordFreqCount.run()
