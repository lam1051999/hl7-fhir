from common.util.database import get_connection, get_files
import os
import argparse
import json

if __name__ == "__main__":
    PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser()
    parser.add_argument('--for_action', required=True)
    args = parser.parse_args()
    for_action = args.for_action

    connection = get_connection()
    files = get_files(connection, for_action)

    if len(files) > 0:
        data_dirs = {}
        for item in files:
            _file_name = item['file_name']
            _format = _file_name.split(".")[-1]
            _process = _file_name.split("_")[1]
            _subprocess = _file_name.split("_")[2]
            _path = f"{_format}/{_process}/{_subprocess}"
            if _path not in data_dirs:
                data_dirs[_path] = set()
            data_dirs[_path].add(_file_name)
        for key in data_dirs:
            data_dirs[key] = list(data_dirs[key])
        target_dir = f"{PROJECT_DIR}/metadata"
        os.makedirs(target_dir, exist_ok = True)
        with open(f"{target_dir}/{for_action}.json", "w") as fi:
            fi.write(json.dumps(data_dirs, indent=4))
    else:
        print("No files for processing")

    connection.close()