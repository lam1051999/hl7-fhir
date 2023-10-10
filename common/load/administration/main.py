from common.schema.administration.organization import organization
from common.util.constants import file_status
from common.util.database import update_file_status, get_connection, upsert_actual_data
import os
import shutil

def load(process, spark, data_dir, files):
    connection = get_connection()
    all_dirs = [f"{data_dir}/file_name={item.strip()}" for item in files.split(",")]
    try:
        process(spark, data_dir, all_dirs)
        all_status = [{
            'file_name': item,
            'status': file_status['LOAD_SUCCESS'],
            'description': 'Loaded successfully'
        } for item in files.split(",")]
        update_file_status(connection, all_status)
        for d in all_dirs:
            if os.path.isdir(d):
                shutil.rmtree(d)
    except Exception as e:
        all_status = [{
            'file_name': item,
            'status': file_status['LOAD_FAILED'],
            'description': str(e)
        } for item in files.split(",")]
        update_file_status(connection, all_status)
    finally:
        connection.close()

def load_organization(spark, data_dir, all_dirs):
    def upsert_organization_qualification(list_org):
        py_list_org = [item.asDict(recursive=True) for item in list_org]
        py_list_org_q = []
        for item in py_list_org:
            if item['qualification'] and type(item['qualification']).__name__ == 'list':
                for x in item['qualification']:
                    x["id"] = x["identifier"]["value"]
                    x["organization_id"] = item["id"]
                    py_list_org_q.append(x)
        key = "id"
        columns = [
            key,
            "identifier",
            "code",
            "period",
            "organization_id"
        ]
        json_cols = ["identifier"]
        upsert_actual_data(py_list_org, "organization_qualification", key, columns, json_cols, "(%s, %s, %s::t_codeable_concept, %s::t_period, %s)")

    def upsert_organization(list_org):
        py_list_org = [item.asDict(recursive=True) for item in list_org]
        key = "id"
        columns = [
            key,
            "resourceType",
            "identifier",
            "active",
            "type",
            "name",
            "alias",
            "description",
            "contact"
        ]
        json_cols = ["identifier", "type", "contact"]
        upsert_actual_data(py_list_org, "organization", key, columns, json_cols, "(%s, %s, %s, %s, %s, %s, %s::text[], %s, %s)")
        # organization qualification
        upsert_organization_qualification(list_org)

    df = spark \
        .read \
        .option("basePath", data_dir) \
        .schema(organization) \
        .parquet(*all_dirs)
    df = df.repartition("file_name")
    df.foreachPartition(upsert_organization)
