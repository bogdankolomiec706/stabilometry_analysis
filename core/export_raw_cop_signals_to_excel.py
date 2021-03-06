import os
from scipy.io import loadmat
import pandas as pd
from collections import OrderedDict

from core.record_model import Record

def get_file_pathes_in_dir(path: str, extension: str):
    file_names = []
    for file_name in os.listdir(path):
        if file_name.endswith(".{}".format(extension)):
            file_names.append("{}/{}".format(path, file_name))
    return file_names

def extract_name_from_path(path):
    file_name_with_extension = path.split('/')[-1]
    return file_name_with_extension.split('.')[0]

def read_records_from_file(file_path):
    mat_data = loadmat(file_path).get('s')[0]
    file_name = extract_name_from_path(file_path)
    records = []
    for mat_data_element in mat_data:
        record = Record(mat_data_element, file_name)
        records.append(record)
    return records


if __name__ == "__main__":
    mat_file_pathes = get_file_pathes_in_dir('C:/Users/BohdanK/Dropbox/StabiloData/healthy', extension='mat')#  rowing, water_jumps, healthy

    for file_path in mat_file_pathes:
        patient_records = read_records_from_file(file_path)
        patient_export_list = []
        for record in patient_records:
            patient_export_list.append({record.record_name})
            patient_export_list.append({'xop_x'})
            patient_export_list.append(record.cop.x)
            patient_export_list.append({'xop_y'})
            patient_export_list.append(record.cop.y)
        df = pd.DataFrame.from_records(patient_export_list)
        df.to_excel(f'Data/healthy/healthy_{extract_name_from_path(file_path)}.xlsx', index=False)

