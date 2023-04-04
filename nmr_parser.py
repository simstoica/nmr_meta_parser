import parsers.varian
import parsers.bruker

NMR_PARSER_VERSION = '1.1'

# TODO: discover parsers


def parse(experiment_folder):
    # try Varian   
    params = parsers.varian.Varian(experiment_folder)
    if params:
        return params.parse_params()
    
    # try Bruker
    params = parsers.bruker.Bruker(experiment_folder)
    if params:
        return params.parse_params()


def is_experiment(experiment_folder):
    return parsers.bruker.Bruker.is_experiment(experiment_folder) or \
        parsers.varian.Varian.is_experiment(experiment_folder)
