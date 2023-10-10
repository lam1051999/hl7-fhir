# Data ingestion pipeline for HL7 FHIR data

This demo is for Organization models (https://www.hl7.org/fhir/organization.html), using Spark, Postgres to process and store data, running in local machine.

## Setup

You will need Apache Spark 3.3.0 installed and $SPARK_HOME configured correctly.

```bash
# Start Postgres instance
docker-compose -f docker/docker-compose.yaml up -d
```
Go to `job/init.sql`, run all the SQL queries to init the metadata.

Go to `common/schema/sql/organization.sql`, run all the SQL queries to init Organization tables.

## Install libs

```bash
python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

# your venv directory
export VIRTUAL_ENV=/Volumes/Sandisk/pycharm_venv/dhp_ingestion_tool
```

## Build package

```bash
python setup.py bdist_egg
```

## File upload

```bash
PYTHONPATH="$PWD" python job/file_upload.py \
  --file=fake_data/test.JSON \
  --file_format=JSON \
  --process=administration \
  --sub_process=organization
```

## Validation

```bash
PYTHONPATH="$PWD" python job/file_sensor.py --for_action=validation

# Go to job/metadata/validation.json for input of the below command

export PYSPARK_PYTHON=$VIRTUAL_ENV/bin/python && \
export PYSPARK_DRIVER_PYTHON=$VIRTUAL_ENV/bin/python && \
spark-submit \
  --master "local[4]" \
  --driver-memory 512m \
  --executor-memory 512m \
  --py-files dist/dhp_ingestion_tool_common-0.1.0-py3.10.egg \
  job/validation.py \
  --file_format=JSON \
  --process=administration \
  --sub_process=organization \
  --files DHP_administration_organization_20231010085922.JSON
```

## Ingestion

```bash
PYTHONPATH="$PWD" python job/file_sensor.py --for_action=ingestion

# Go to job/metadata/ingestion.json for input of the below command

export PYSPARK_PYTHON=$VIRTUAL_ENV/bin/python && \
export PYSPARK_DRIVER_PYTHON=$VIRTUAL_ENV/bin/python && \
spark-submit \
  --master "local[4]" \
  --driver-memory 512m \
  --executor-memory 512m \
  --py-files dist/dhp_ingestion_tool_common-0.1.0-py3.10.egg \
  job/ingestion.py \
  --file_format=JSON \
  --process=administration \
  --sub_process=organization \
  --files DHP_administration_organization_20231010085922.JSON
```

## Load

```bash
PYTHONPATH="$PWD" python job/file_sensor.py --for_action=load

# Go to job/metadata/load.json for input of the below command

export PYSPARK_PYTHON=$VIRTUAL_ENV/bin/python && \
export PYSPARK_DRIVER_PYTHON=$VIRTUAL_ENV/bin/python && \
spark-submit \
  --master "local[4]" \
  --driver-memory 512m \
  --executor-memory 512m \
  --py-files dist/dhp_ingestion_tool_common-0.1.0-py3.10.egg \
  job/load.py \
  --process=administration \
  --sub_process=organization \
  --files DHP_administration_organization_20231010085922.JSON
```