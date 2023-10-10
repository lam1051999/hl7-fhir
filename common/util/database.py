import psycopg2
from common.util.constants import file_status
from common.util.helper import list_objects_to_insert_data_json
from psycopg2 import extras

def get_connection():
    return psycopg2.connect(database="postgres",
                            host="localhost",
                            user="postgres",
                            password="postgres",
                            port="5432")

def get_dict(curs):
    field_names = [d[0].lower() for d in curs.description]
    data = curs.fetchall()
    list_dict = []
    for _data in data:
        list_dict.append(
            {field_names[i]: _data[i] for i, _ in enumerate(_data)}
        )
    return list_dict

def upsert(connection, table, data, key):
    cursor = connection.cursor()
    if len(data) > 0:
        columns = list(data[0].keys())
        if key not in columns:
            raise Exception("Cannot update file status, key is not present in the input data")
        values = []
        for item in data:
            temp = []
            for col in columns:
                temp.append(item[col])
            temp.append("NOW()")
            values.append(temp)
        columns.append("updated")
        insert_values = [", ".join([f"'{inner}'" for inner in item]) for item in values]
        insert_values = [f"({item})" for item in insert_values]
        query = f"""INSERT INTO {table}({", ".join([f'"{item}"' for item in columns])})
                VALUES
                {",".join(insert_values)}
                ON CONFLICT("{key}")
                DO UPDATE SET
                    {", ".join([f'"{col}" = EXCLUDED."{col}"' for col in columns if col != key])}; 
                """
        cursor.execute(query)
        connection.commit()

def update_file_status(connection, data):
    upsert(connection, "file_monitor", data, "file_name")

def get_healthcare_process(connection):
    cursor = connection.cursor()
    query = "SELECT * FROM healthcare_process;"
    cursor.execute(query)
    rs = get_dict(cursor)
    return rs

def get_files(connection, for_action):
    if for_action == 'validation':
        status = file_status['UPLOAD_SUCCESS']
    elif for_action == 'ingestion':
        status = file_status['VALIDATION_SUCCESS']
    elif for_action == 'load':
        status = file_status['INGESTION_SUCCESS']
    else:
        status = None
    cursor = connection.cursor()
    query = f"""SELECT * FROM file_monitor WHERE "status" = '{status}';""" if status else "SELECT * FROM file_monitor;"
    cursor.execute(query)
    rs = get_dict(cursor)
    return rs

def upsert_actual_data(py_list_items, table, key, columns, json_cols, template):
    connection = get_connection()
    cursor = connection.cursor()
    insert_list = list_objects_to_insert_data_json(columns, py_list_items, json_cols)
    query = f"""INSERT INTO {table}({", ".join([f'"{item}"' for item in columns])})
                            VALUES %s
                            ON CONFLICT("{key}")
                            DO UPDATE SET
                                {", ".join([f'"{col}" = EXCLUDED."{col}"' for col in columns if col != key])}; 
                            """
    extras.execute_values(cursor, query, insert_list, template=template)

    connection.commit()
    cursor.close()
    connection.close()