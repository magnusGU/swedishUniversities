from pyspark import SparkContext

def run():
    sc = SparkContext(master = 'local[4]')
    #sc.setLogLevel(0)
    quiet_logs(sc)
    distFile = sc.textFile("datasnippet.txt")

    counts = distFile.map(lambda l: l.split('\t')).map(lambda t:(int(t[0]),1)).reduceByKey(lambda a, b: a + b).filter(lambda t:t[1] > 1)

    print(counts)
    cc = counts.collect()

    print("*******************************************************************")
    print(cc)

def quiet_logs( sc ):
  logger = sc._jvm.org.apache.log4j
  logger.LogManager.getLogger("org"). setLevel( logger.Level.OFF )
  logger.LogManager.getLogger("akka").setLevel( logger.Level.OFF )


if __name__ == '__main__':
    run()