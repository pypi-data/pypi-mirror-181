# DIETERpy is electricity market model developed by the research group
# Transformation of the Energy Economy at DIW Berlin (German Institute of Economic Research)
# copyright 2021, Carlos Gaete-Morales, Martin Kittel, Alexander Roth,
# Wolf-Peter Schill, Alexander Zerrahn
"""
This module contains the default names of variables. It mainly contains folders' names that other modules will use to link the data.
"""
import os
import appdirs
import dieterpy

PROJECT_DIR_ABS = ""

PROJECT_NAME = ""

BASE_DIR_NAME = "project_files"

INPUT_DIR_NAME = "data_input"

SETTINGS_DIR_NAME = "settings"

ITERATION_DIR_NAME = "iterationfiles"

MODEL_DIR_NAME = "model"

RUN_DIR_NAME = "rundir"

GDX_INPUT_NAME = "gdx_input"

RESULTS_DIR_NAME = "data_output"

REPORT_DIR_NAME = "report_files"

RESULT_CONFIG = dict()

TMP = "tmp"

CWD = os.getcwd()

TEMPLATES_DIR_NAME = "templates"

TEMPLATES_INFO_FILE = "templates_info.json"

DEFAULT_DATA_DIR = appdirs.user_data_dir("dieterpy", "dieterpy")

USER_PATH = os.environ.get('DIETERPY_DATA_DIR')

MODULE_PATH = dieterpy.__path__[0]

MODULE_TEMPLATES_PATH = os.path.join(MODULE_PATH, TEMPLATES_DIR_NAME)

MODEL_CONFIG = {'DIETER':
                        {
                            'project_features': [
                                                    "base_year",
                                                    "define_h_set",
                                                    "dispatch_only",
                                                    "network_transfer",
                                                    "no_crossover",
                                                    "infeasibility",
                                                ],
                            'input_file_basename': ["data_input","time_series"],
                            'feat_node_exists': True,
                            'iterable_data_exists': True,  # This is an excel file that contains time series scenarios, h dim must be included
                            'topography_exists': True,
                        },
}

COLUMNS = []