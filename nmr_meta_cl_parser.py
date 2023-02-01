# *************************
# * Author: Simona Stoica *
# * Version:              *
# * License:              *
# *************************
import argparse
import os
import pathlib


def get_default_location_for_log_files():
    return pathlib.Path(__file__).parent.resolve()


class BaseClParser():
    def __init__(self):
        self.parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    def parse(self):
        self.opt = self.parser.parse_args()
        if self.opt.irods_env_file:
            self.opt.irods_env_file = os.path.expanduser(self.opt.irods_env_file)
        if self.opt.irods_auth_file:
            self.opt.irods_auth_file = os.path.expanduser(self.opt.irods_auth_file)


class Nmr_meta_cl_parser(BaseClParser):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser.add_argument("--irods-env-file", type=str, required=False,
                                 help='Local path to the environment file.'
                                 'If no authentication file has been provided, system will select '
                                 'default ~/.irods/irods_environment.json')

        self.parser.add_argument("--irods-auth-file", type=str, required=False,
                                 help='Local path to the corresponding authentication file.'
                                 'If no authentication file has been provided, system will select '
                                 'default ~/.irods/.irodsA')

        self.parser.add_argument("--nmr-data-local-folder", type=str, required=True, default=os.getcwd(),
                                 help='Local path to the folder with the organized nmr data')

        self.parser.add_argument("--nmr-data-rdms-folder", type=str, required=False, default='',
                                 help='Path on the rdms with the organized nmr data')

        self.parser.add_argument("--log-level", type=str, required=False, default='info',
                                 choices=['info', 'debug', 'warning'],
                                 help='Level of information to be given in the logs')

        self.parser.add_argument("--nmr-csv-name", type=str, required=False, default='',
                                 help='File name of the summary CSV with metadta')

        self.parser.add_argument("--max-depth", type=int, required=False, default=4,
                                 help='Max depth level of the experiment folder with respect'
                                 ' to the requested folder.')

        self.parser.add_argument("--analyse-localy", type=str, required=False, default='n',
                                 help='Use to investigate the metadata on the local folder.'
                                 'If set to y, the system will only analyse the metadata locally without looking at '
                                 'any irods environment')

        self.parser.add_argument("--log-files-location", type=str, required=False, default=get_default_location_for_log_files(),
                                 help="Location on disk where the log files will be stored. If no value is specifed, "
                                 "the log files will be written in the main script folder."
                                 "Warning: the location must exist and will not be created")
