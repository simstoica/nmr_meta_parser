import os
import datetime

import irods.path
import irods.session

import nmr_parser


SYSTEM_NMR_META = 'sysmdt_nmr_meta_extractor'
SYSTEM_NMR_META_VERSION = 'sysmdt_nmr_meta_version'


class NMR_meta_binder():

    def __init__(self, path_to_local_folder, path_to_rdms_folder, irods_connector):
        self.path_to_local_folder = os.path.expanduser(path_to_local_folder)
        self.path_to_rdms_folder = path_to_rdms_folder
        self.irods_connector = irods_connector

    def execute(self):
        associated_groups = get_subdirectories(self.path_to_local_folder)
        for associated_group in associated_groups:
            personal_folders = get_subdirectories(associated_group)

            for folder in personal_folders:
                experiments_list = get_subdirectories(folder)
                for experiment in experiments_list:
                    self.bind_metadata(experiment)

    def bind_metadata(self, experiment_folder):
        experiment_folder_on_irods = self._get_path_on_irods_server(experiment_folder)
        if not self.irods_connector.session.collections.exists(experiment_folder_on_irods):
            return

        irods_collection_of_experiment = self.irods_connector.session.collections.get(experiment_folder_on_irods)

        if irods_collection_of_experiment.metadata.get_all(SYSTEM_NMR_META):
            return

        metadata = nmr_parser.parse(experiment_folder)
        if not metadata:
            return

        prepared_metadata = self._prepare_metadata(metadata)
        self.irods_connector.addMultipleMetadata([irods_collection_of_experiment], prepared_metadata)

    def _prepare_metadata(self, metadata):
        prepared_meta = [
            [SYSTEM_NMR_META, f'{datetime.datetime.now()}', ''],
            [SYSTEM_NMR_META_VERSION, nmr_parser.NMR_PARSER_VERSION, '']
        ]

        for (key, value, unit) in metadata:
            if key == 'Parameter_file':
                value = self._get_path_on_irods_server(value)
            prepared_meta.append([f'{key}', f'{value}', f'{unit}'])
        return prepared_meta

    def _get_path_on_irods_server(self, experiment_folder):
        relative_path_to_experiment = os.path.relpath(os.path.expanduser(experiment_folder), self.path_to_local_folder)

        return irods.path.iRODSPath(self.path_to_rdms_folder, relative_path_to_experiment)


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
