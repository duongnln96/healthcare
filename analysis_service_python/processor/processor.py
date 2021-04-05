from py4j.java_gateway import set_field
import pyspark.sql.functions as F
import pyspark.sql.types as T


from config import (
    AppConfig,
)

raw_record_schema = T.StructType([ \
    T.StructField('age',                      T.StringType(), True),\
    T.StructField('sex',                      T.StringType(), True),\
    T.StructField('chest_pain_type',          T.StringType(), True),\
    T.StructField('resting_blood_pressure',   T.StringType(), True),\
    T.StructField('cholesterol',              T.StringType(), True),\
    T.StructField('fasting_blood_sugar',      T.StringType(), True),\
    T.StructField('rest_ecg',                 T.StringType(), True),\
    T.StructField('max_heart_rate_achieved',  T.StringType(), True),\
    T.StructField('exercise_induced_angina',  T.StringType(), True),\
    T.StructField('st_depression',            T.StringType(),  True),\
    T.StructField('st_slope',                 T.StringType(), True)
])

field_name = []

class HealthCareApplication:
    def __init__(self, config: AppConfig, spark_session) -> None:
        self._kafka_config = config.kafka_config
        self._topic_result = config.topic_result
        self._topic_raw = config.topic_raw
        self._ml_model_path = config.model_path
        self._spark = spark_session
        
        self._df = None

    def _read_stream_from_source(self):
        df = self._spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", self._kafka_config.bootstrap_servers) \
            .option("subscribe", self._topic_raw) \
            .load() \
            .selectExpr("CAST(timestamp AS TIMESTAMP) as timestamp", "CAST(value AS STRING) as message")

        self._df = df \
            .withColumn("value", F.from_json("message", raw_record_schema)) \
            .select('timestamp', 'value.*')                   

    def _processing_data(self):
        #TODO
        pass

    def _query_data(self, format=None, output_mode=None):
        stream_query = self._df \
                        .writeStream \
                        .format("json") \
                        .outputMode("append") \
                        .option("path", "./tmp/json_data")\
                        .option("checkpointLocation", "./tmp/checkpoint")\
                        .start()

        stream_query.awaitTermination()
        

    def start(self):
        self._read_stream_from_source()
        self._query_data()
        