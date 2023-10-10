from pyspark.sql.functions import input_file_name, expr, element_at
from common.util.database import update_file_status, get_connection
from common.util.constants import file_status
from common.schema.administration.organization import organization

# /administration/organization
def validate_organization(spark, data_dir, files):
    df = spark.read.schema(organization).json([f"{data_dir}/{item.strip()}" for item in files.split(",")],
                                              multiLine=True)
    connection = get_connection()
    df = df \
        .withColumn("file_name", input_file_name()) \
        .withColumn("_validation_id", expr("size(identifier) > 0 OR length(name) > 0")) \
        .withColumn("_validation_telecom", expr("size(filter(contact, x -> size(filter(x.telecom, t -> t.use == 'home')) > 0)) <= 0")) \
        .withColumn("_validation_address", expr("size(filter(contact, x -> x.address.use == 'home')) <= 0"))
    df.createOrReplaceTempView("organization_view")
    validated = spark.sql("""
        SELECT file_name abs_file_name, (_all_validation_id + _all_validation_telecom + _all_validation_address) <= 0 _validated,
            CASE 
                WHEN _all_validation_id > 0 THEN 'org-1: The organization SHALL at least have a name or an identifier, and possibly more than one'
                WHEN _all_validation_telecom > 0 THEN 'The telecom of an organization can never be of use <home>'
                WHEN _all_validation_address > 0 THEN 'The address of an organization can never be of use <home>'
                ELSE 'Validated successfully'
            END description
        FROM (
            SELECT file_name, SUM(CASE WHEN _validation_id THEN 0 ELSE 1 END) _all_validation_id, 
                SUM(CASE WHEN _validation_telecom THEN 0 ELSE 1 END) _all_validation_telecom,
                SUM(CASE WHEN _validation_address THEN 0 ELSE 1 END) _all_validation_address
            FROM organization_view
            GROUP BY file_name
        ) tbl
    """)
    validated = validated.withColumn("file_name", element_at(expr("SPLIT(abs_file_name, '/')"), -1))
    all_files = [item.asDict(recursive=True) for item in validated.collect()]
    all_files = [{
        'file_name': item['file_name'],
        'status': file_status['VALIDATION_SUCCESS'] if item['_validated'] else file_status['VALIDATION_FAILED'],
        'description': item['description']
    } for item in all_files]
    update_file_status(connection, all_files)