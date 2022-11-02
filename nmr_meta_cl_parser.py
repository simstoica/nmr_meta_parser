# *************************
# * Author: Simona Stoica *
# * Version:              *
# * License:              *
# *************************
import argparse
import os


class BaseParser():
    def __init__(self):
        self.parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    def parse(self):
        self.opt = self.parser.parse_args()
        if self.opt.irods_env_file:
            self.opt.irods_env_file = os.path.expanduser(self.opt.irods_env_file)
        if self.opt.irods_auth_file:
            self.opt.irods_auth_file = os.path.expanduser(self.opt.irods_auth_file)


class Nmr_meta_cl_parser(BaseParser):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser.add_argument("--irods-env-file", type=str, required=False,
                                 help='Local path to the environment file.'
                                 'If no authentication file has been provided, system will select default ~/.irods/irods_environment.json')

        self.parser.add_argument("--irods-auth-file", type=str, required=False,
                                 help='Local path to the corresponding authentication file.'
                                 'If no authentication file has been provided, system will select default ~/.irods/.irodsA')

        self.parser.add_argument("--nmr-data-local-folder", type=str, required=False, default=os.getcwd(),
                                 help='Local path to the folder with the organized nmr data')

        self.parser.add_argument("--nmr-csv-name", type=str, required=False, default='nmr_metadata.csv',
                                 help='File name of the summary CSV with metadta')

        self.parser.add_argument("--nmr-data-rdms-folder", type=str, required=False,
                                 help='Path on the rdms with the organized nmr data')
