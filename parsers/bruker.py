from datetime import datetime
import nmrglue as ng

from utils import get_email, get_requester_email, get_gnumber


def parse_params(experiment_folder):
    try:
        acqus = ng.fileio.bruker.read_acqus_file(experiment_folder)

        if 'acqus' not in acqus:
            return None

        exp_date = datetime.fromtimestamp(acqus['acqus']['DATE'])

        return {
            'Email': get_email(experiment_folder),
            'Requester': get_requester_email(experiment_folder),
            'Gnumber': get_gnumber(experiment_folder),
            "Manufacturer": 'Bruker',
            "Machine": acqus['acqus']['INSTRUM'],
            "Date": exp_date,
            "Experiment Type_seqfil": acqus['acqus']['EXP'],
            'Number of scans': acqus['acqus']['NS'],
            'Solvent': acqus['acqus']['SOLVENT'],
            'Frequency_1': acqus['acqus']['BF1'],
            'Frequency_2': acqus['acqus']['BF2'],
            'Nucleus_1': acqus['acqus']['NUC1'].upper(),
            'Nucleus_2': acqus['acqus']['NUC2'].upper(),
            'Pulse Sequence': acqus['acqus']['PULPROG']
        }

    except Exception as e:
        print(f'Exception parsing brucker experiment `{experiment_folder}` error:{e}')
        return None
