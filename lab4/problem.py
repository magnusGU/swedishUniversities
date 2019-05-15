from mrjob.job import MRJob


class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        _id, group, value = line.split()
        #yield "id", data[0]
        #yield "group", data[1]
        yield "value", float(value)

    def reducer(self, key, values):
        yield key, sum(values)


if __name__ == '__main__':
    MRWordFrequencyCount.run()
    