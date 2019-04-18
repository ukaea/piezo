from __future__ import print_function

import os
import sys

from pyspark.sql import SparkSession

if __name__ == "__main__":
    output_dir = sys.argv[1]
    num_mappers = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    num_kv_pairs = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
    val_size = int(sys.argv[4]) if len(sys.argv) > 4 else 1000
    num_reducers = int(sys.argv[5]) if len(sys.argv) > 5 else num_mappers

    spark = SparkSession \
        .builder \
        .appName("GroupBy") \
        .getOrCreate()

    def f(_):
        return [os.urandom(val_size) for _ in range(num_kv_pairs)]


    count = spark.sparkContext \
        .parallelize(range(1, num_mappers + 1), num_mappers) \
        .map(f) \
        .groupByKey(numPartitions=num_reducers)\
        .count()

    print(count)

    spark.stop()
