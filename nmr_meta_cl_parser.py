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


class Nmr_meta_cl_parser(BaseParser):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser.add_argument("--irods-env-file", type=str, required=False,
                                 help='Local path to the environment file')

        self.parser.add_argument("--irods-pwd-file", type=str, required=False,
                                 help='Local path to the encoded password file')

        self.parser.add_argument("--nmr-data-local-folder", type=str, required=False, default=os.getcwd(),
                                 help='Local path to the folder with the organized nmr data')

        self.parser.add_argument("--nmr-data-rdms-folder", type=str, required=False,
                                 help='Path on the rdms with the organized nmr data')
