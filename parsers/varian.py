from datetime import datetime
import nmrglue as ng
import os

from utils import get_email, get_gnumber
from utils import to_kelvin, to_2_digits_float_string
from utils import get_2nd_nucleus_based_on_experiment_type, isotope_number_first


def parse_params(experiment_folder):
    proc_file_name = os.path.abspath(os.path.join(experiment_folder, "procpar"))

    if not os.path.exists(proc_file_name):
        return None

    try:
        parsed_parameters = {
            'Email': get_email(experiment_folder),
            'Gnumber': get_gnumber(experiment_folder),
            "Manufacturer": 'Varian',
            "Analysis": 'NMR'
        }

        procparams = ng.fileio.varian.read_procpar(proc_file_name)

        def _from_procparams(field_name):
            return procparams[field_name]['values'][0]

        date_exp = datetime.strptime(_from_procparams('time_complete'), '%Y%m%dT%H%M%S')
        parsed_parameters.update({
            "Date": date_exp.date(),
            "Time": date_exp.time()})

        parsed_parameters.update({
            "Machine": _from_procparams('console'),
            'Number of scans': _from_procparams('ct'),
            'Solvent': _from_procparams('solvent').lower(),
            'Pulse Sequence': _from_procparams('seqfil'),
            'Temperature': round(to_kelvin(float(_from_procparams('temp'))))
        })

        exp_type = _from_procparams('apptype')[-2:].upper()
        f_1 = to_2_digits_float_string(_from_procparams('sfrq'))
        f_2 = to_2_digits_float_string(_from_procparams('dfrq')) if exp_type == '2D' else 'OFF'

        n_1 = _from_procparams('tn').upper()
        n_2 = get_2nd_nucleus_based_on_experiment_type(exp_type, n_1, _from_procparams('dn').upper())

        parsed_parameters.update({
            'Experiment Type': exp_type,
            'Frequency_1': f_1,
            'Frequency_2': f_2,
            'Nucleus_1': isotope_number_first(n_1),
            'Nucleus_2': isotope_number_first(n_2)
        })

        journal_id = _from_procparams('notebook')
        if journal_id == '':
            journal_id = 'NA'
        parsed_parameters['Journal ID'] = journal_id

        return parsed_parameters
    except Exception as e:
        print(f'Exception parsing varian experiment {e}')
        return None
