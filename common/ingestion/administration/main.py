from common.schema.administration.organization import organization
from common.util.constants import file_status
from common.util.database import update_file_status, get_connection
import os
from pyspark.sql.functions import input_file_name, expr, element_at

def ingest(process, spark, data_dir, data_dest, files):
    connection = get_connection()
    all_files = [f"{data_dir}/{item.strip()}" for item in files.split(",")]
    try:
        process(spark, all_files, data_dest)
        all_status = [{
            'file_name': item,
            'status': file_status['INGESTION_SUCCESS'],
            'description': 'Ingested successfully'
        } for item in files.split(",")]
        update_file_status(connection, all_status)
        for f in all_files:
            if os.path.isfile(f):
                os.remove(f)
    except Exception as e:
        all_status = [{
            'file_name': item,
            'status': file_status['INGESTION_FAILED'],
            'description': str(e)
        } for item in files.split(",")]
        update_file_status(connection, all_status)
    finally:
        connection.close()


def ingest_organization(spark, all_files, data_dest):
    df = spark.read.schema(organization).json(all_files, multiLine=True)
    df = df.withColumn("abs_file_name", input_file_name())
    df = df.withColumn("file_name", element_at(expr("SPLIT(abs_file_name, '/')"), -1))
    df \
        .repartition(1) \
        .write \
        .mode("append") \
        .partitionBy("file_name") \
        .parquet(data_dest)