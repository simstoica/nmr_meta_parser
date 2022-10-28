from datetime import datetime
import nmrglue as ng

from utils import get_content_dot_email_file, get_content_dot_gnumber_file, to_n_digits_float_string
from utils import get_2nd_nucleus_based_on_experiment_type, isotope_number_first


def parse_params(experiment_folder):
    try:
        acqus = ng.fileio.bruker.read_acqus_file(experiment_folder)

        if 'acqus' not in acqus:
            return None

        parsed_parameters = {
            'Author': get_content_dot_email_file(experiment_folder),
            'Group': get_content_dot_gnumber_file(experiment_folder),
            "Manufacturer": 'Bruker',
            "Analysis": 'NMR'
        }

        date_exp = datetime.fromtimestamp(acqus['acqus']['DATE'])
        parsed_parameters.update({
            "Date": date_exp.date(),
            "Time": date_exp.time()})

        parsed_parameters.update({
            "Machine": acqus['acqus']['INSTRUM'],
            'Probe_head': acqus['acqus']['PROBHD'],
            'Number_of_scans': acqus['acqus']['NS'],
            'Solvent': acqus['acqus']['SOLVENT'].lower(),
            'Pulse_sequence': acqus['acqus']['PULPROG'],
            'Temperature': int(acqus['acqus']['TE']),
            'Relaxation_delay': acqus['acqus']['D'][1]
        })

        exp_type = '2D' if 'acqu2s' in acqus else '1D'
        f_1 = to_n_digits_float_string(acqus['acqus']['BF1'])
        n_1 = acqus['acqus']['NUC1'].upper()
        n_2 = get_2nd_nucleus_based_on_experiment_type(exp_type, n_1, acqus['acqus']['NUC2'].upper())
        spectral_width_1 = to_n_digits_float_string(acqus['acqus']['SW'])
        center_1 = to_n_digits_float_string(float(acqus['acqus']['O1'])/float(acqus['acqus']['BF1']), n=1)

        if exp_type == '2D':
            f_2 = to_n_digits_float_string(acqus['acqus']['BF2'])
            spectral_width_2 = to_n_digits_float_string(acqus['acqu2s']['SW'])
            center_2 = to_n_digits_float_string(float(acqus['acqu2s']['O1'])/float(acqus['acqu2s']['BF1']), n=1)
        else:
            f_2 = 'OFF'
            spectral_width_2 = 'NA'
            center_2 = 'NA'

        parsed_parameters.update({
            'Experiment_type': exp_type,
            'Frequency_1': f_1,
            'Frequency_2': f_2,
            'Nucleus_1': isotope_number_first(n_1),
            'Nucleus_2': isotope_number_first(n_2),
            'Spectral_width_1': spectral_width_1,
            'Spectral_width_2': spectral_width_2,
            'Center_1': center_1,
            'Center_2': center_2
        })

        return parsed_parameters

    except Exception as e:
        print(f'Exception parsing brucker experiment `{experiment_folder}` error:{e}')
        return None
