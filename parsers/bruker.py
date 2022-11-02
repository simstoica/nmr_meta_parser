import contextlib
from datetime import datetime
import nmrglue as ng

from parse_utils import get_content_dot_email_file, get_content_dot_gnumber_file, to_n_digits_float_string
from parse_utils import get_2nd_nucleus_based_on_experiment_type, isotope_number_first


class Bruker:
    acqus = None
    is_valid = False

    def __init__(self, experiment_folder):
        self._experiment_folder = experiment_folder
        with contextlib.suppress(Exception):
            self.acqus = ng.fileio.bruker.read_acqus_file(experiment_folder)

            if 'acqus' in self.acqus:
                self.is_valid = True
                self.parsed_parameters = {}

    def __bool__(self):
        return self.is_valid

    def parse_params(self):
        try:
            return self.parse_header_information() + \
                self.parse_date() + \
                self.parse_experiment_information() + \
                self.nuclea_information()
        except Exception as e:
            print(f'Exception parsing brucker experiment `{self._experiment_folder}` error:{e}')
            return []

    def parse_header_information(self):
        return [
            ['Author', get_content_dot_email_file(self._experiment_folder), ''],
            ['Group', get_content_dot_gnumber_file(self._experiment_folder), ''],
            ["Manufacturer", 'Bruker', ''],
            ["Analysis", 'NMR', '']
        ]

    def parse_date(self):
        date_exp = datetime.fromtimestamp(self.acqus['acqus']['DATE'])
        return [
            ["Date", date_exp.date(), ''],
            ["Time", date_exp.time(), '']
        ]

    def parse_experiment_information(self):
        return [
            ["Machine", self.acqus['acqus']['INSTRUM'], 'microseconds [\u03BCs]'],
            ['Probe_head', self.acqus['acqus']['PROBHD'], ''],
            ['Number_of_scans', self.acqus['acqus']['NS'], ''],
            ['Solvent', self.acqus['acqus']['SOLVENT'].lower(), ''],
            ['Pulse_sequence', self.acqus['acqus']['PULPROG'], ''],
            ['Pulse_width', to_n_digits_float_string(self.acqus['acqus']['P'][1], n=1), ''],
            ['Temperature', int(self.acqus['acqus']['TE']), 'Kelvin [K]'],
            ['Relaxation_delay', self.acqus['acqus']['D'][1], 'seconds [s]']
        ]

    def nuclea_information(self):
        exp_type = '2D' if 'acqu2s' in self.acqus else '1D'
        f_1 = to_n_digits_float_string(self.acqus['acqus']['BF1'])
        n_1 = self.acqus['acqus']['NUC1']
        n_2 = get_2nd_nucleus_based_on_experiment_type(exp_type, n_1, self.acqus['acqus']['NUC2'])
        spectral_width_1 = to_n_digits_float_string(self.acqus['acqus']['SW'])
        center_1 = to_n_digits_float_string(float(self.acqus['acqus']['O1'])/float(self.acqus['acqus']['BF1']), n=1)

        if exp_type == '2D':
            f_2 = to_n_digits_float_string(self.acqus['acqus']['BF2'])
            spectral_width_2 = to_n_digits_float_string(self.acqus['acqu2s']['SW'])
            center_2 = to_n_digits_float_string(
                float(self.acqus['acqu2s']['O1'])/float(self.acqus['acqu2s']['BF1']), n=1)
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
