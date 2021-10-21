from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import explode
from pyspark.sql.functions import split
from pyspark.sql.functions import window,col,desc

def parse_data_from_kafka_message(sdf, schema):
    from pyspark.sql.functions import split
    assert sdf.isStreaming == True, "DataFrame doesn't receive treaming data"
    col = split(sdf['value'], ',')

    #split attributes to nested array in one Column
    #now expand col to multiple top-level columns
    for idx, field in enumerate(schema):
        sdf = sdf.withColumn(field.name, col.getItem(idx).cast(field.dataType))
    return sdf

if __name__ == "__main__":

    spark = SparkSession.builder \
               .appName("KafkaWordCount") \
               .getOrCreate()

    #Read from Kafka's topic scrapy-output
    df = spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "localhost:9092") \
            .option("subscribe", "scrapy-output") \
            .option("startingOffsets", "earliest") \
            .load()

    #Parse the fields in the value column of the message
    lines = df.selectExpr("CAST(value AS STRING)", "timestamp")

    #Specify the schema of the fields
    hardwarezoneSchema = StructType([ \
        StructField("topic", StringType()), \
        StructField("author", StringType()), \
        StructField("content", StringType()) \
        ])

    #Use the function to parse the fields
    lines = parse_data_from_kafka_message(lines, hardwarezoneSchema) \
        .select("topic","author","content","timestamp")

    windowed = lines \
        .withWatermark("timestamp", "2 minutes") \
        .groupBy(
            window("timestamp", "2 minutes", "1 minutes"),
            "author"
        ) \
        .count() \
        .limit(10)

    windowed = windowed.orderBy(col('count').desc())

    #Select the content field and output
    contents = windowed \
        .writeStream \
        .queryName("WriteContent") \
        .outputMode("complete") \
        .format("console") \
        .start()

    #Start the job and wait for the incoming messages
    contents.awaitTermination()