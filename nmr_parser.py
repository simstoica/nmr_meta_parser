import parsers.varian
import parsers.bruker

NMR_PARSER_VERSION = '1.0'

# TODO: discover parsers


def parse(experiment_folder):
    if params := parsers.varian.Varian(experiment_folder):
        return params.parse_params()
    if params := parsers.bruker.Bruker(experiment_folder):
        return params.parse_params()


def is_experiment(experiment_folder):
    return parsers.bruker.Bruker.is_experiment(experiment_folder) or \
        parsers.varian.Varian.is_experiment(experiment_folder)
