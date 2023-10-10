from pyspark.sql import SparkSession
import os
import argparse
from common.validation.administration.rules import validate_organization

if __name__ == "__main__":
    PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser()
    parser.add_argument('--file_format', required=True, choices=["JSON", "XML"])
    parser.add_argument('--process', required=True)
    parser.add_argument('--sub_process', required=True)
    parser.add_argument('--files', required=True)
    args = parser.parse_args()
    file_format = args.file_format
    process = args.process
    sub_process = args.sub_process
    files = args.files

    spark = SparkSession \
        .builder \
        .getOrCreate()

    data_dir = f"{PROJECT_DIR}/data/{file_format}/{process}/{sub_process}"

    if process == "administration":
        if sub_process == "organization":
            if file_format == "JSON":
                validate_organization(spark, data_dir, files)