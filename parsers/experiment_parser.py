class Experiment_parser:
    is_valid = False

    def __bool__(self):
        return self.is_valid

    def parse_params(self):
        try:
            return self.parse_header_information() + \
                self.parse_date() + \
                self.parse_experiment_information() + \
                self.nuclea_information()
        except Exception as e:
            print(f'Exception parsing experiment `{self._experiment_folder}` error:{e}')
            return []
