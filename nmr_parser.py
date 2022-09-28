import parsers.varian
import parsers.bruker


# TODO: discover parsers
def parse(experiment_folder):
    if params := parsers.varian.parse_params(experiment_folder):
        return params
    if params := parsers.bruker.parse_params(experiment_folder):
        return params
