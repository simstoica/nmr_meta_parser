import logging

from nmr_meta_cl_parser import Nmr_meta_cl_parser
from nmr_meta_binder import NMR_meta_binder
from utils.IrodsConnector import IrodsConnector
from utils.DummyIrodsConnector import DummyIrodsConnector
import utils


def get_logging_level(level):
    if level == 'debug':
        return logging.DEBUG
    elif level == 'warning':
        return logging.WARNING
    else:
        return logging.INFO


def get_connector(parameters):
    if parameters.analyse_localy == 'y':
        return DummyIrodsConnector()

    return IrodsConnector(irods_env_file=parameters.irods_env_file, irods_auth_file=parameters.irods_auth_file)


if __name__ == "__main__":
    p = Nmr_meta_cl_parser()
    p.parse()

    utils.utils.setup_logger('.', 'NMR_meta_logger', get_logging_level(p.opt.log_level))

    conn = get_connector(p.opt)

    if not conn.collection_exists(p.opt.nmr_data_rdms_folder):
        logging.warning(f'Irods collection {p.opt.nmr_data_rdms_folder} does not exist!')
    else:
        NMR_meta_binder(
            p.opt.nmr_data_local_folder,
            p.opt.nmr_data_rdms_folder,
            p.opt.nmr_csv_name,
            p.opt.max_depth,
            conn
        ).execute()
