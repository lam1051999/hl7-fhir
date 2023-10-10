from collections import namedtuple
from psycopg2.extras import Json

seqs = (tuple, list, set, frozenset)

def list_objects_to_insert_data(columns, list_objects):
    insert_list = []
    for item in list_objects:
        temp = []
        for col in columns:
            temp.append(dict_to_namedtuple(item[col], col))
        insert_list.append(tuple(temp))
    return insert_list

def list_objects_to_insert_data_json(columns, list_objects, json_cols):
    insert_list = []
    for item in list_objects:
        temp = []
        for col in columns:
            temp.append(Json(item[col]) if col in json_cols else dict_to_namedtuple(item[col], col))
        insert_list.append(tuple(temp))
    return insert_list

def dict_to_namedtuple(d, name='NamedTuple'):
    # Handle the case when the input is a dictionary
    if isinstance(d, dict):
        fields = []
        for key, value in d.items():
            # Recursively convert sub-dictionaries and dictionaries in lists
            if isinstance(value, (dict, *seqs)):
                value = dict_to_namedtuple(value, key)
            fields.append((key, value))
        return namedtuple(name, [field[0] for field in fields])(**{field[0]: field[1] for field in fields})
    # Handle the case when the input is a list of dictionaries
    elif isinstance(d, seqs):
        return [dict_to_namedtuple(item, name) if isinstance(item, dict) else item for item in d]
    # Handle the case when the input is a literal value
    else:
        return d
