import contextlib
import csv
import datetime
import logging
import os

import irods.path
import irods.session

import nmr_parser


SYSTEM_NMR_META = 'sysmdt_nmr_meta_extractor'
SYSTEM_NMR_META_VERSION = 'sysmdt_nmr_meta_version'


class NMR_meta_binder():

    def __init__(self, path_to_local_folder, path_to_rdms_folder, path_to_csv_file, irods_connector):
        self.path_to_local_folder = os.path.expanduser(path_to_local_folder)
        self.path_to_rdms_folder = path_to_rdms_folder
        self.irods_connector = irods_connector
        self.path_to_csv_file = path_to_csv_file
        self.all_metadata = []
        self.keys = []
        

    def execute(self):
        associated_groups = get_subdirectories(self.path_to_local_folder)
        for associated_group in associated_groups:
            logging.info(f'Scanning `{associated_group}')
            personal_folders = get_subdirectories(associated_group)

            for folder in personal_folders:
                logging.info(f'Scanning `{folder}')
                experiments_list = get_subdirectories(folder)
                for experiment in experiments_list:
                    self.bind_metadata(experiment)
                    
        self.print_csv_if_needed()

    def bind_metadata(self, experiment_folder):
        logging.info(f'Analyzing `{experiment_folder}`')
        experiment_folder_on_irods = self._get_path_on_irods_server(experiment_folder)
        logging.info(f'\t Corresponding iRODS folder: `{experiment_folder_on_irods}`')

        if not self.irods_connector.session.collections.exists(experiment_folder_on_irods):
            logging.warning(f'\t\t iRODS collection does not exist `{experiment_folder_on_irods}`')
            return

        irods_collection_of_experiment = self.irods_connector.session.collections.get(experiment_folder_on_irods)
        if irods_collection_of_experiment.metadata.get_all(SYSTEM_NMR_META):
            logging.warning(f'\t\tiRODS collection `{experiment_folder_on_irods}` already has nmr metadata')
            return

        metadata = nmr_parser.parse(experiment_folder)
        if not metadata:
            logging.warning(f'\t\tCannot extract metadata for experiment `{experiment_folder}`')
            return

        prepared_metadata = self._prepare_metadata(metadata)
        logging.debug(f'\t\tPrepared metadata {prepared_metadata}')
        if not self.irods_connector.addMultipleMetadata([irods_collection_of_experiment], prepared_metadata):
            logging.error(f'Could not attach metadata to `{experiment_folder_on_irods}`')
        
        self._attach_to_csv_overview(experiment_folder, prepared_metadata)
        logging.info(f'\t\tAttached metadata to collection `{experiment_folder_on_irods}`')

    def _prepare_metadata(self, metadata):
        prepared_meta = [
            [SYSTEM_NMR_META, f'{datetime.datetime.now()}', ''],
            [SYSTEM_NMR_META_VERSION, nmr_parser.NMR_PARSER_VERSION, '']
        ]

        for (key, value, unit) in metadata:
            if key == 'Parameter_file':
                value = self._get_path_on_irods_server(value)
            if not value:
                value = 'NA'
            prepared_meta.append([f'{key}', f'{value}', f'{unit}'])
        return prepared_meta

    def _get_path_on_irods_server(self, experiment_folder):
        relative_path_to_experiment = os.path.relpath(os.path.expanduser(experiment_folder), self.path_to_local_folder)

        return irods.path.iRODSPath(self.path_to_rdms_folder, relative_path_to_experiment)
    
    
    def _attach_to_csv_overview(self, experiment_folder, metadata):
        if not self.path_to_csv_file:
            return

        metadata.insert(0, ['Experiment', str(experiment_folder), ''])
        self.all_metadata.append(metadata)

        current_keys = [a for a,_,_ in metadata]
        for a in current_keys:
            if a in self.keys and current_keys.count(a)==self.keys.count(a):
                continue
            
            for _ in range(current_keys.count(a)-self.keys.count(a)):
                self.keys.append(a)                
   
    def print_csv_if_needed(self):
        if not self.path_to_csv_file:
            return

        with open(self.path_to_csv_file, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.keys)


            for metadata_list in self.all_metadata:
                writer.writerow(self._map_current_keys_to_header(metadata_list))

    def _map_current_keys_to_header(self, metadata_list):
        metadata_row = [''] * len(self.keys)    

        current_keys = [a for a,_,_ in metadata_list]
        values = [v for _,v,_ in metadata_list]

        for a in current_keys:
            n1 = current_keys.count(a)
            n2 = self.keys.count(a)
            start_index_keys = 0
            start_index_current_keys = 0
            while n2 > 0 and n1 > 0:
                with contextlib.suppress(KeyError):
                    index_in_keys = self.keys.index(a, start_index_keys)
                    current_index = current_keys.index(a, start_index_current_keys)

                    metadata_row[index_in_keys] = values[current_index]

                    start_index_current_keys = current_index + 1
                    start_index_keys = index_in_keys + 1
                    n1 -= 1
                    n2 -= 1
                    
        return metadata_row
        


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
