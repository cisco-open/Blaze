import os.path as path

# ASKI/data
FILES_DIR    = path.realpath(path.join(path.dirname(path.realpath(__file__)), '..', '..', 'user'))

# /ASKI/aski/models
MODELS_DIR   = path.realpath(path.join(path.dirname(path.realpath(__file__)), '..', 'models/'))

# /ASKI/aski/datasets
DATASETS_DIR = path.realpath(path.join(path.dirname(path.realpath(__file__)), '..', 'datasets/'))

PORT_REST_API = 3000
PREF_REST_API = "http://127.0.0.1:"