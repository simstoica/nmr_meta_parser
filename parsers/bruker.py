from datetime import datetime
import nmrglue as ng

from utils import get_email, get_requester_email, get_gnumber, to_2_digits_float_string
from utils import get_2nd_nucleus_based_on_experiment_type

def parse_params(experiment_folder):
    try:
        acqus = ng.fileio.bruker.read_acqus_file(experiment_folder)

        if 'acqus' not in acqus:
            return None
        
        parsed_parameters = {
            'Email': get_email(experiment_folder),
            'Requester': get_requester_email(experiment_folder),
            'Gnumber': get_gnumber(experiment_folder),
            "Manufacturer": 'Bruker'
        }

        date_exp = datetime.fromtimestamp(acqus['acqus']['DATE'])
        parsed_parameters.update({
            "Date": date_exp.date(),
            "Time": date_exp.time()})
        
        parsed_parameters.update({
            "Machine": acqus['acqus']['INSTRUM'],
            'Number of scans': acqus['acqus']['NS'],
            'Solvent': acqus['acqus']['SOLVENT'],
            'Pulse Sequence': acqus['acqus']['PULPROG'],
            'Temperature': int(acqus['acqus']['TE']),
            })
        
        exp_type = '2D' if 'acqu2s' in acqus else '1D'
        f_1 = to_2_digits_float_string(acqus['acqus']['BF1'])
        f_2 = to_2_digits_float_string(acqus['acqus']['BF2']) if exp_type =='2D' else 'OFF'
        n_1 = acqus['acqus']['NUC1'].upper()
        n_2 = get_2nd_nucleus_based_on_experiment_type(exp_type, n_1, acqus['acqus']['NUC2'].upper())
        
        parsed_parameters.update({
                'Experiment Type':exp_type,
                'Frequency_1': f_1,
                'Frequency_2' :f_2,
                'Nucleus_1': n_1, 
                'Nucleus_2': n_2
            })
     
        return parsed_parameters

    except Exception as e:
        print(f'Exception parsing brucker experiment `{experiment_folder}` error:{e}')
        return None
