from datetime import datetime
import nmrglue as ng
import os

from utils import get_email, get_gnumber, get_requester_email
from utils import to_kelvin, to_2_digits_float_string



def parse_params(experiment_folder):
    proc_file_name = os.path.abspath(os.path.join(experiment_folder, "procpar"))

    if not os.path.exists(proc_file_name):
        return None

    try:
        parsed_parameters = {
            'Email': get_email(experiment_folder),
            'Requester': get_requester_email(experiment_folder),
            'Gnumber': get_gnumber(experiment_folder),
            "Manufacturer": 'Varian'}
        
        
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
            'Solvent': _from_procparams('solvent'),
            'Pulse Sequence': _from_procparams('seqfil'),
            'Temperature': round(to_kelvin(float(_from_procparams('temp'))))
        })
        
        experiment_type = _from_procparams('apptype')[-2:].upper()
        f_1 = to_2_digits_float_string(_from_procparams('sfrq'))
        n_1 = _from_procparams('tn').upper()
        parsed_parameters.update({
                'Experiment Type':experiment_type,
                'Frequency_1': f_1,
                'Frequency_2' :'OFF',
                'Nucleus_1': n_1, 
                'Nucleus_2':'OFF'
            })
        if experiment_type == '2D':
            n_2 = _from_procparams('dn').upper()
            f_2 = to_2_digits_float_string(_from_procparams('dfrq'))
            parsed_parameters.update({
                'Frequency_2': f_2,
                'Nucleus_2': n_2
            })
            
        return parsed_parameters
    except Exception as e:
        print(f'Exception parsing varian experiment {e}')
        return None
