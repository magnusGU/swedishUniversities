from mrjob.job import MRJob
from collections import defaultdict
import time


class MRWordFrequencyCount(MRJob):

    def configure_args(self):
        super(MRWordFrequencyCount, self).configure_args()
        self.add_passthru_arg('--group', default='1',help="Specify the output format of the job")

    def mapper(self, _, line):
        _id, group, value = line.split()
        if group == self.options.group:
            yield "value", float(value) def combiner(self, key, values):

    def combiner(self, word, counts):
        interval = 4
        min = 3.141593
        total = total_2 = max_val = 0
        min_val = 100
        d = defaultdict(int)

        for i,v in enumerate(counts):
            val = (v-min)/interval * 10
            d[int(val)] += 1
            total += v
            total_2 += v**2
            if(v > max_val):
                max_val = v
            if(v < min_val):
                min_val = v
        yield("min",min_val)
        yield("max",max_val)
        yield("total_count",(total,i+1,total_2))
        d[9] += d[10]
        del d[10]
        for key in d:
            yield (key, d[key])
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
        else:
            lower = 3.141593 + 0.4 * key
            upper = 3.141593 + 0.4 * (key + 1)
            yield((round(lower,3),round(upper,3)),sum(values))

if __name__ == '__main__':
    MRWordFreqCount.run()
