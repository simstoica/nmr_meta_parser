from pathlib import Path


def find_file_in_parent_folders(experiment_folder, file_name):
    for current_folder in Path(experiment_folder).resolve().parents:
        file_name_with_path = current_folder.joinpath(file_name)
        if file_name_with_path.exists():
            return file_name_with_path

    return None


def get_file_contents_in_parent_folder(experiment_folder, file_name):
    try:
        file_with_path = find_file_in_parent_folders(experiment_folder, file_name)
        assert (file_with_path)

        with open(file_with_path) as f:
            return f.read().strip()

    except Exception:
        return ''


def get_email(experiment_folder):
    return get_file_contents_in_parent_folder(experiment_folder, '.email')


def get_requester_email(experiment_folder):
    return get_file_contents_in_parent_folder(experiment_folder, '.requestermail')


def get_gnumber(experiment_folder):
    return get_file_contents_in_parent_folder(experiment_folder, '.gnumber')


def to_celsius(temperature_in_K):
    return temperature_in_K - 273.15


def to_kelvin(temperature_in_C):
    return temperature_in_C + 273.15
