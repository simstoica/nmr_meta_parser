from datetime import datetime
import nmrglue as ng
import os

from parse_utils import get_content_dot_email_file, get_content_dot_gnumber_file
from parse_utils import to_kelvin, to_n_digits_float_string
from parse_utils import get_2nd_nucleus_based_on_experiment_type, isotope_number_first

from parsers import experiment_parser


class Varian(experiment_parser.Experiment_parser):

    def __init__(self, experiment_folder):
        self._experiment_folder = experiment_folder
        self._proc_file_name = os.path.abspath(os.path.join(experiment_folder, "procpar"))

        if os.path.exists(self._proc_file_name):
            self._procparams = ng.fileio.varian.read_procpar(self._proc_file_name)
            self.is_valid = True

    def parse_header_information(self):
        return [
            ['Author', get_content_dot_email_file(self._experiment_folder), ''],
            ['Group', get_content_dot_gnumber_file(self._experiment_folder), ''],
            ["Manufacturer", 'Varian', ''],
            ["Analysis", 'NMR', '']
        ]

    def parse_date(self):
        date_exp = datetime.strptime(self._from_procparams('time_complete'), '%Y%m%dT%H%M%S')
        return [
            ["Date", date_exp.date(), ''],
            ["Time", date_exp.time(), '']
        ]

    def parse_experiment_information(self):
        journal_id = self._from_procparams('notebook')
        if journal_id == '':
            journal_id = 'NA'

        return [
            ["Machine", self._from_procparams('console'), ''],
            ["ID", self._from_procparams('go_id'), ''],
            ["Probe_head", self._from_procparams('probe_'), ''],
            ['Number_of_scans', self._from_procparams('ct'), ''],
            ['Solvent', self._from_procparams('solvent').lower(), ''],
            ['Pulse_sequence', self._from_procparams('seqfil'), ''],
            ['Pulse_width', to_n_digits_float_string(self._from_procparams('pw'), n=1), 'microseconds [\u03BCs]'],
            ['Temperature', to_n_digits_float_string(to_kelvin(float(self._from_procparams('temp'))), n=1), 'Kelvin [K]'],
            ['Temperature', to_n_digits_float_string(self._from_procparams('temp'), n=1), 'Celsius [\u00B0]'],
            ['Relaxation_delay', self._from_procparams('d1'), 'seconds [s]'],
            ['Acquisition_time', to_n_digits_float_string(self._from_procparams('at'), n=1), 'seconds [s]'],
            ['Journal_ID', journal_id, '']
        ]

    def nuclea_information(self):
        exp_type = self._from_procparams('apptype')[-2:].upper()
        f_1 = to_n_digits_float_string(self._from_procparams('sfrq'))
        n_1 = self._from_procparams('tn')
        n_2 = get_2nd_nucleus_based_on_experiment_type(exp_type, n_1, self._from_procparams('dn'))

        try:
            _sw = float(self._from_procparams('sw'))
            _sfrq = float(self._from_procparams('sfrq'))
            spectral_width_1 = to_n_digits_float_string(_sw/_sfrq, n=1)
            _rfl = float(self._from_procparams('rfl'))
            _rfp = float(self._from_procparams('rfp'))
            center_1 = to_n_digits_float_string(((_sw/2)-_rfl+_rfp)/_sfrq, n=1)
        except Exception:
            spectral_width_1 = 'NA'
            center_1 = 'NA'

        if exp_type == '2D':
            f_2 = to_n_digits_float_string(self._from_procparams('dfrq'))
            try:
                _sw1 = float(self._from_procparams('sw1'))
                _dfrq = float(self._from_procparams('dfrq'))
                spectral_width_2 = to_n_digits_float_string(_sw1/_dfrq, n=1)
                _rfl1 = float(self._from_procparams('rfl1'))
                _rfp1 = float(self._from_procparams('rfp1'))
                center_2 = to_n_digits_float_string(((_sw1/2)-_rfl1+_rfp1)/_dfrq, n=1)
            except Exception:
                spectral_width_2 = 'NA'
                center_2 = 'NA'
        else:
            f_2 = 'OFF'
            spectral_width_2 = 'NA'
            center_2 = 'NA'

        return [
            ['Experiment_type', exp_type, ''],
            ['Frequency_1', f_1, 'Hertz [Hz]'],
            ['Frequency_2', f_2, 'Hertz [Hz]'],
            ['Nucleus_1', isotope_number_first(n_1), ''],
            ['Nucleus_2', isotope_number_first(n_2), ''],
            ['Spectral_width_1', spectral_width_1, 'ppm'],
            ['Spectral_width_2', spectral_width_2, 'ppm'],
            ['Center_1', center_1, 'ppm'],
            ['Center_2', center_2, 'ppm']
        ]

    def parse_parameter_files(self):
        return [
            ['Parameter_file', str(os.path.join(self._experiment_folder, 'procpar')), '']
        ]

    def _from_procparams(self, field_name):
        return self._procparams[field_name]['values'][0]

    @staticmethod
    def is_experiment(experiment_folder):
        procpar_path = os.path.abspath(os.path.join(experiment_folder, "procpar"))
        return os.path.isfile(procpar_path)
