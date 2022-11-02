import parsers.varian
import parsers.bruker


# TODO: discover parsers
def parse(experiment_folder):
    if params := parsers.varian.Varian(experiment_folder):
        return params.parse_params()
    if params := parsers.bruker.Bruker(experiment_folder):
        return params.parse_params()
