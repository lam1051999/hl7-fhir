from pyspark.sql.types import StructType, StructField, StringType, ArrayType, BooleanType
from common.schema.common import identifier, codeable_concept, period, extended_contact_detail

qualification = StructType([
    StructField("identifier", ArrayType(identifier), True),
    StructField("code", codeable_concept, True),
    StructField("period", period, True)
])

organization = StructType([
    StructField("resourceType", StringType(), True),
    StructField("id", StringType(), True),
    StructField("identifier", ArrayType(identifier), True),
    StructField("active", BooleanType(), True),
    StructField("type", ArrayType(codeable_concept), True),
    StructField("name", StringType(), True),
    StructField("alias", ArrayType(StringType()), True),
    StructField("description", StringType(), True),
    StructField("contact", ArrayType(extended_contact_detail), True),
    StructField("qualification", ArrayType(qualification), True),
])