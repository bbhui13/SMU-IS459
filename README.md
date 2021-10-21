# IS459-hardwarezone

# Done by: Hui Hon Yu Bryan 01357687

Instructions: 
- clone repo

# prerequisites

1. Python3 is installed.
2. Hadoop File System (HDFS), Spark (Pyspark), and the extension for Pyspark, GraphFrames is installed and activated.
3. hardwarezone.parquet is inside /user/your_username/parquet-input (change the directory in assignment_2.py)
4. set the checkpoint to your own directory as well

Instructions: 
- clone repo ()


Assignment 2:

# how to run

1. run "pyspark --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2"
2. Run each command in `assignment_2.py` line-by-line into the shell.

note: the answers to the assignment questions are in the email i sent for assignment 2

Assignment 3:

Skip step 1 if assuming zookeeper and kafka are already running
1. Run zookeeper and kafka (using docker)
- make sure docker application is active
- open a wsl ubuntu and do "cd docker"
- run docker compose using "docker-compose up"

2. scrape from hardwarezone
- open another wsl ubuntu and do "cd Scrapy/hardwarezone/hardwarezone/spiders"
- run "scrapy crawl hardwarezone"

3. run spark submit for author
- open another wsl ubuntu and run "$SPARK_HOME/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 ./spark/kafka_authorcount.py"

4. run spark submit for words
- open another wsl ubuntu and run "$SPARK_HOME/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 ./spark/kafka_wordcount.py"