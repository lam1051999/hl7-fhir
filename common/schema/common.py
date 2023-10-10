from pyspark.sql.types import StructType, StructField, StringType, ArrayType, BooleanType

coding = StructType([
    StructField("system", StringType(), True),
    StructField("version", StringType(), True),
    StructField("code", StringType(), True),
    StructField("display", StringType(), True),
    StructField("userSelected", BooleanType(), True)
])

codeable_concept = StructType([
    StructField("coding", ArrayType(coding), True),
    StructField("text", StringType(), True)
])

period = StructType([
    StructField("start", StringType(), True),
    StructField("end", StringType(), True),
])

identifier = StructType([
    StructField("use", StringType(), True),
    StructField("type", codeable_concept, True),
    StructField("system", StringType(), True),
    StructField("value", StringType(), True),
    StructField("period", period, True)
])

human_name = StructType([
    StructField("use", StringType(), True),
    StructField("text", StringType(), True),
    StructField("family", StringType(), True),
    StructField("given", ArrayType(StringType()), True),
    StructField("prefix", ArrayType(StringType()), True),
    StructField("suffix", ArrayType(StringType()), True),
    StructField("period", period, True)
])

telecom = StructType([
    StructField("system", StringType(), True),
    StructField("value", StringType(), True),
    StructField("use", StringType(), True),
    StructField("rank", ArrayType(StringType()), True),
    StructField("period", period, True)
])

address = StructType([
    StructField("use", StringType(), True),
    StructField("type", StringType(), True),
    StructField("text", StringType(), True),
    StructField("line", ArrayType(StringType()), True),
    StructField("city", StringType(), True),
    StructField("district", StringType(), True),
    StructField("state", StringType(), True),
    StructField("postalCode", StringType(), True),
    StructField("country", StringType(), True),
    StructField("period", period, True)
])

extended_contact_detail = StructType([
    StructField("purpose", codeable_concept, True),
    StructField("name", ArrayType(human_name), True),
    StructField("telecom", ArrayType(telecom), True),
    StructField("address", address, True),
    StructField("period", period, True)
])