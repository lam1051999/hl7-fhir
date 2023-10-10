import argparse
import os
import shutil
from common.util.database import get_connection, get_healthcare_process, update_file_status
from common.util.constants import file_status
import datetime

if __name__ == "__main__":
    PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True)
    parser.add_argument('--file_format', required=True, choices=["JSON", "XML"])
    parser.add_argument('--process', required=True)
    parser.add_argument('--sub_process', required=True)
    args = parser.parse_args()
    file = args.file
    file_format = args.file_format
    process = args.process
    sub_process = args.sub_process

    if not os.path.isfile(file):
        raise Exception("Input data is not a file")

    original_file_name = os.path.basename(file)

    connection = get_connection()
    healthcare_process = get_healthcare_process(connection)
    list_process = [item['process'] for item in healthcare_process]
    list_subprocess = [item['subprocess'] for item in healthcare_process if item['process'] == process]

    if process not in list_process:
        raise Exception(f"Input error for process, must be one of {list_process}")

    if sub_process not in list_subprocess:
        raise Exception(f"Input error for sub_process, must be one of {list_subprocess} for process '{process}'")

    current_timestamp = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S")
    data_dir = f"{PROJECT_DIR}/data/{file_format}/{process}/{sub_process}"
    file_name = f"DHP_{process}_{sub_process}_{current_timestamp}.{file_format}"
    os.makedirs(data_dir, exist_ok=True)
    try:
        destination = shutil.copyfile(file, f"{data_dir}/{file_name}")
        update_file_status(connection, [{
            'file_name': file_name,
            'original_file_name': original_file_name,
            'status': file_status['UPLOAD_SUCCESS'],
            'description': f'Uploaded successfully'
        }])
    except Exception as e:
        update_file_status(connection, [{
            'file_name': file_name,
            'original_file_name': original_file_name,
            'status': file_status['UPLOAD_FAILED'],
            'description': str(e)
        }])
    finally:
        connection.close()