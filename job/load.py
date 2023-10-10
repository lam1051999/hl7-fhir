from pyspark.sql import SparkSession
import os
import argparse
from common.load.administration.main import load, load_organization

if __name__ == "__main__":
    PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser()
    parser.add_argument('--process', required=True)
    parser.add_argument('--sub_process', required=True)
    parser.add_argument('--files', required=True)
    args = parser.parse_args()
    process = args.process
    sub_process = args.sub_process
    files = args.files

    spark = SparkSession \
        .builder \
        .getOrCreate()

    data_dir = f"{PROJECT_DIR}/data/VALIDATED/{process}/{sub_process}"

    if process == "administration":
        if sub_process == "organization":
                load(load_organization, spark, data_dir, files)