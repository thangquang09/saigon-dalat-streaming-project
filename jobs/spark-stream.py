import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, TimestampType
from datetime import datetime
try:
    from config import KAFKA_CONFIG, HDFS_NAMENODE
except ImportError as e:
    print(f"Error importing KAFKA_CONFIG: {e}")
    exit(1)



if __name__ == "__main__":
    spark = (
        SparkSession.builder
        .appName("SaiGonDaLatStreamingData")
        .master("spark://spark-master:7077")
        .config("spark.jars.packages", 
                "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.scala-lang:scala-library:2.12.15")
        .getOrCreate()
    )

    # define schemas
    vehicle_schema = StructType([
        StructField('id', StringType(), True),
        StructField('deviceId', IntegerType(), True),
        StructField('timestamp', TimestampType(), True),
        StructField('controlPlate', StringType(), True),
        StructField('deviceType', StringType(), True),
        StructField('model', StringType(), True),
        StructField('year', IntegerType(), True),
    ])

    gps_schema = StructType([
        StructField('id', StringType(), True),
        StructField('deviceId', IntegerType(), True),
        StructField('timestamp', TimestampType(), True),
        StructField('latitude', DoubleType(), True),
        StructField('longitude', DoubleType(), True),
        StructField('speed', DoubleType(), True),
        StructField('direction', IntegerType(), True),
        StructField('accuracy', StringType(), True),
        StructField('satelliteCount', IntegerType(), True),
    ])
    
    camera_schema = StructType([
        StructField('id', StringType(), True),
        StructField('deviceId', IntegerType(), True),
        StructField('cameraId', StringType(), True),
        StructField('timestamp', TimestampType(), True),
        StructField('snapshot', StringType(), True),
    ])

    weather_schema = StructType([
        StructField('id', StringType(), True),
        StructField('deviceId', IntegerType(), True),
        StructField('timestamp', TimestampType(), True),
        StructField('latitude', DoubleType(), True),
        StructField('longitude', DoubleType(), True),
        StructField('temperature', DoubleType(), True),
        StructField('humidity', IntegerType(), True),
        StructField('windSpeed', DoubleType(), True),
        StructField('weatherCondition', StringType(), True),
    ])

    emergency_schema = StructType([
        StructField('id', StringType(), True),
        StructField('deviceId', IntegerType(), True),
        StructField('timestamp', TimestampType(), True),
        StructField('latitude', DoubleType(), True),
        StructField('longitude', DoubleType(), True),
        StructField('incidentId', StringType(), True),
        StructField('type', StringType(), True),
    ])

    def read_stream_from_kafka(topic, schema):
        return (
            spark.readStream
            .format('kafka')
            .option('kafka.bootstrap.servers', 'broker:29092')
            .option('subscribe', topic)
            .option('startingOffsets', 'earliest')
            .load()
            .selectExpr('CAST(value AS STRING)')
            .select(from_json(col('value'), schema).alias('data'))
            .select('data.*')
            .withWatermark('timestamp', '1 minutes')
        )

    def streamWriter(input, checkpointFolder, output):
        return (
            input.writeStream
            .format('parquet')
            .option('checkpointLocation', checkpointFolder)
            .option('path', output)
            .outputMode('append')
            .start()
        )

    try:
        vehicle_df = read_stream_from_kafka(KAFKA_CONFIG['VEHICLE_TOPIC'], vehicle_schema).alias('vehicle')
        gps_df = read_stream_from_kafka(KAFKA_CONFIG['GPS_TOPIC'], gps_schema).alias('gps')
        camera_df = read_stream_from_kafka(KAFKA_CONFIG['CAMERA_TOPIC'], camera_schema).alias('camera')
        weather_df = read_stream_from_kafka(KAFKA_CONFIG['WEATHER_TOPIC'], weather_schema).alias('weather')
        emergency_df = read_stream_from_kafka(KAFKA_CONFIG['EMERGENCY_TOPIC'], emergency_schema).alias('emergency')
        
        query1 = streamWriter(
            vehicle_df, 
            os.path.join(HDFS_NAMENODE, 'user/spark/checkpoints/vehicle_data'), 
            os.path.join(HDFS_NAMENODE, 'user/spark/data/vehicle_data')
        )

        query2 = streamWriter(
            gps_df, 
            os.path.join(HDFS_NAMENODE, 'user/spark/checkpoints/gps_data'), 
            os.path.join(HDFS_NAMENODE, 'user/spark/data/gps_data')
        )

        query3 = streamWriter(
            camera_df, 
            os.path.join(HDFS_NAMENODE, 'user/spark/checkpoints/camera_data'), 
            os.path.join(HDFS_NAMENODE, 'user/spark/data/camera_data')
        )

        query4 = streamWriter(
            weather_df, 
            os.path.join(HDFS_NAMENODE, 'user/spark/checkpoints/weather_data'), 
            os.path.join(HDFS_NAMENODE, 'user/spark/data/weather_data')
        )

        query5 = streamWriter(
            emergency_df, 
            os.path.join(HDFS_NAMENODE, 'user/spark/checkpoints/emergency_data'), 
            os.path.join(HDFS_NAMENODE, 'user/spark/data/emergency_data')
        )

        query5.awaitTermination()
    except Exception as e:
        print(f"Error in streaming process: {e}")
        spark.stop()
        exit(1)
    finally:
        spark.stop()
