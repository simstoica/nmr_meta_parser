from datetime import datetime
import nmrglue as ng
import os

from utils import get_content_dot_email_file, get_content_dot_gnumber_file
from utils import to_kelvin, to_2_digits_float_string
from utils import get_2nd_nucleus_based_on_experiment_type, isotope_number_first


def parse_params(experiment_folder):
    proc_file_name = os.path.abspath(os.path.join(experiment_folder, "procpar"))

    if not os.path.exists(proc_file_name):
        return None

    try:
        parsed_parameters = {
            'Author': get_content_dot_email_file(experiment_folder),
            'Group': get_content_dot_gnumber_file(experiment_folder),
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
            "Probe_head": _from_procparams('probe_'),
            'Number_of_scans': _from_procparams('ct'),
            'Solvent': _from_procparams('solvent').lower(),
            'Pulse_sequence': _from_procparams('seqfil'),
            'Temperature': round(to_kelvin(float(_from_procparams('temp')))),
            'Relaxation_delay': _from_procparams('d1')
        })

        exp_type = _from_procparams('apptype')[-2:].upper()
        f_1 = to_2_digits_float_string(_from_procparams('sfrq'))
        n_1 = _from_procparams('tn').upper()
        n_2 = get_2nd_nucleus_based_on_experiment_type(exp_type, n_1, _from_procparams('dn').upper())

        try:
            _sw = float(_from_procparams('sw'))
            _sfrq = float(_from_procparams('sfrq'))
            spectral_width_1 = to_2_digits_float_string(_sw/_sfrq)
        except Exception:
            spectral_width_1 = 'NA'

        if exp_type == '2D':
            f_2 = to_2_digits_float_string(_from_procparams('dfrq'))
            try:
                _sw1 = float(_from_procparams('sw1'))
                _dfrq = float(_from_procparams('dfrq'))
                spectral_width_2 = to_2_digits_float_string(_sw1/_dfrq)
            except Exception:
                spectral_width_2 = 'NA'
        else:
            f_2 = 'OFF'
            spectral_width_2 = 'NA'

        parsed_parameters.update({
            'Experiment_type': exp_type,
            'Frequency_1': f_1,
            'Frequency_2': f_2,
            'Nucleus_1': isotope_number_first(n_1),
            'Nucleus_2': isotope_number_first(n_2),
            'Spectral_width_1': spectral_width_1,
            'Spectral_width_2': spectral_width_2
        })

        journal_id = _from_procparams('notebook')
        if journal_id == '':
            journal_id = 'NA'
        parsed_parameters['Journal_ID'] = journal_id

        return parsed_parameters
    except Exception as e:
        print(f'Exception parsing varian experiment {e}')
        return None
