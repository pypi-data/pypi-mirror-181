import os

from yangson import DataModel


def get_model(path, name: str, mod_path=None, description: str = None):
    default_path = os.path.dirname(os.path.realpath(__file__)) + '/yang'
    if mod_path:
        mod_path = list(mod_path)
        mod_path.append(default_path)
    else:
        mod_path = [path,default_path]

    data_model = DataModel.from_file(path+name, mod_path, description)
    return data_model.schema
