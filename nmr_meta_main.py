import os
import csv


import nmr_parser
from nmr_meta_cl_parser import Nmr_meta_cl_parser
from nmr_meta_binder import NMR_meta_binder
from utils.IrodsConnector import IrodsConnector


def get_subdirectories(path):
    return (f.path for f in os.scandir(path) if f.is_dir())


def get_all_experiment_folders(path):
    experiments_list = []
    associated_groups = get_subdirectories(path)
    for associated_group in associated_groups:
        personal_folders = get_subdirectories(associated_group)

        for folder in personal_folders:
            experiments_list.extend(iter(get_subdirectories(folder)))

    return experiments_list


# /rugZone/home/user/data
# ./data
if __name__ == "__main__":
    p = Nmr_meta_cl_parser()
    p.parse()

    conn = IrodsConnector(irods_env_file=p.opt.irods_env_file, irods_auth_file=p.opt.irods_auth_file)
    NMR_meta_binder(p.opt.nmr_data_local_folder, p.opt.nmr_data_rdms_folder, conn).execute()
    
    
    
    
    # # Expermiment discovery
    # experiment_folders = get_all_experiment_folders(p.opt.nmr_data_local_folder)
    # print(len(experiment_folders))

    # # Parsing
    # csv_rows = []
    # keys = ['Experiment']
    # for experiment in experiment_folders:
    #     metadata = nmr_parser.parse(experiment)
    #     if not metadata:
    #         continue

    #     metadata.insert(0, ['Experiment', str(experiment), ''])
    #     csv_rows.append({k: v for (k, v, _) in metadata})

    #     keys.extend(key for key, _, _ in metadata if key not in keys)

    # # csv data
    # with open(p.opt.nmr_csv_name, 'w', encoding='UTF8', newline='') as f:
    #     writer = csv.DictWriter(f, fieldnames=keys)
    #     writer.writeheader()
    #     writer.writerows(csv_rows)
