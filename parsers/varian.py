import nmrglue as ng
import os

from utils import get_email, get_gnumber, get_requester_email


def parse_params(experiment_folder):
    proc_file_name = os.path.abspath(os.path.join(experiment_folder, "procpar"))

    if not os.path.exists(proc_file_name):
        return None

    try:
        procparams = ng.fileio.varian.read_procpar(proc_file_name)

        return {
            'Email': get_email(experiment_folder),
            'Requester': get_requester_email(experiment_folder),
            'Gnumber': get_gnumber(experiment_folder),
            "Manufacturer": 'Varian',
            "Machine": procparams['console']['values'][0],
            "Date": procparams['time_complete']['values'][0],
            "Experiment Type_seqfil": procparams['seqfil']['values'][0],
            "Experiment Type_explist": procparams['explist']['values'][0],
            "Experiment Type_explabel": procparams['explabel']['values'][0],
            'Number of scans': procparams['ct']['values'][0],
            'Solvent': procparams['solvent']['values'][0],
            'Frequency_1': procparams['sfrq']['values'][0],
            'Frequency_2': procparams['dfrq']['values'][0],
            'Nucleus_1': procparams['tn']['values'][0].upper(),
            'Nucleus_2': procparams['dn']['values'][0].upper(),
            'Pulse Sequence': procparams['seqfil']['values'][0]
        }
    except Exception as e:
        print(f'Exception parsing varian experiment {e}')
        return None
