#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from __future__ import print_function

import sys
from operator import add

from pyspark.sql import SparkSession


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: wordcount <file>", file=sys.stderr)
        sys.exit(-1)

    spark = SparkSession\
        .builder\
        .appName("PythonWordCount")\
        .getOrCreate()

    lines = spark.read.text(sys.argv[1]).rdd.map(lambda r: r[0])
    counts = lines.flatMap(lambda x: x.split(' ')) \
                  .map(lambda x: (x, 1)) \
                  .reduceByKey(add)
    
    
    counts.saveAsTextFile(sys.argv[2])

    output = counts.collect()
    # string = ""
    # for (word, count) in output:
    #     string += ("%s: %i\n" % (word, count))

    # with open(sys.argv[2], 'w+') as output_file:
    #     output_file.write(string)
 
        
    # print(sys.argv[2])
    # output.map(lambda row: str(row[0]) + "\t" + str(row[1])).saveAsTextFile(sys.argv[2])
    #output.saveAsTextFile(sys.argv[2])

    for (word, count) in output:
        print("%s: %i\n" % (word, count))
        
    
    spark.stop()