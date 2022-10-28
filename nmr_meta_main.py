import os
import csv


import nmr_parser
from nmr_meta_cl_parser import Nmr_meta_cl_parser


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


if __name__ == "__main__":
    p = Nmr_meta_cl_parser()
    p.parse()

    # Expermiment discovery
    experiment_folders = get_all_experiment_folders(p.opt.nmr_data_local_folder)
    print(len(experiment_folders))

    # Parsing

    csv_rows = []
    keys = ['Experiment']
    for experiment in experiment_folders:
        metadata = nmr_parser.parse(experiment)
        metadata['Experiment'] = str(experiment)
        csv_rows.append(metadata)
        
        keys.extend(key for key in metadata if key not in keys)
        
    # csv data
    with open(p.opt.nmr_csv_name, 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(csv_rows)
