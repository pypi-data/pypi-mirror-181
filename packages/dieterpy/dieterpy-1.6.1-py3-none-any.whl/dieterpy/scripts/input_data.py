# DIETERpy is electricity market model developed by the research group
# Transformation of the Energy Economy at DIW Berlin (German Institute of Economic Research)
# copyright 2021, Carlos Gaete-Morales, Martin Kittel, Alexander Roth,
# Wolf-Peter Schill, Alexander Zerrahn
"""
This module contains the functions that help to process the input data
"""
from exceltogdx import exceltogdx
import pandas as pd
import os
import time
import re
import secrets

from typing import List
from gams import GamsWorkspace, GamsOptions, DebugLevel, GamsCheckpoint

from .gdx_handler import gdx_get_set_coords
from .gams_tools import gams_feat_node, gams_csv2gdx_parameters
from .util import col2num
from ..config import settings

# TODO: Add inputs parameters as arguments of runopt.main(). This will be an alternative way to config files
def getConfigVariables(config_folder: str, project_file=None) -> dict:
    """Imports configuration of the project variables and scenario variables from CSV file

    Args:
        config_folder (str): folder path of project_variables.csv location

    Returns:
        dict: Dictionary containing configuration variables
    """
    if project_file is None:
        project_file = "project_variables.csv"

    cv_df = pd.read_csv(os.path.join(config_folder, project_file))
    project_variables = {}
    for i, row in cv_df.iterrows():
        project_variables[row["feature"]] = (
            row["value"] if not pd.isnull(row["value"]) else ""
        )
    if 'model_file' not in project_variables:
        print("It is defined model_file = model.gms as 'model_file' feature not present in project_variables.csv. Make sure the file is in 'model' folder or put the correct file name in project_variables.csv")
        project_variables['model_file'] = "model.gms"
    if 'gams_dir' not in project_variables:
        project_variables['gams_dir'] = os.getenv('GAMS_DIR') or os.getenv('GAMSDIR') or None
        print(f"GAMS system location found: {project_variables['gams_dir']}")
    if 'save_all_symbols' not in project_variables:
        project_variables['save_all_symbols'] = 'yes'

    return project_variables


def getGlobalFeatures(config_folder: str, active_global_features: List[str]) -> dict:
    """
    This function prepares features that will be handed over to GAMS model as Global parameters. Creates dict with appropriate switch values for all global options.
    On-switch: '*'
    Off-switch: "''"

    Args:
        config_folder (str): Path referring to folder location that contains features_node_selection.csv.
        active_global_features (List[str]): It contains all features names that need to be activated in the GAMS model.

    Returns:
        dict: Contains switch information for global features.
    """
    # get all global features
    glob_feat_list = pd.read_csv(os.path.join(config_folder, "features_node_selection.csv"))["feature"].to_list()

    # assign feature switch values
    glob_feat_dc = {gf: "*" if gf in active_global_features else "''" for gf in glob_feat_list}
    return glob_feat_dc

def generateInputGDX_gdx(input_path: str, gdx_path: str, file_basename: str, gams_dir=None) -> tuple:
    """Generates input gdx files if skip_import is 'no' in project_variables.csv.

    Args:
        input_path (str): path referring to folder location that contains input xlsx files.
        gdx_path (str): path referring to folder location that contains input gdx files to be generated.
        file_basename (str): base name then input is with .xlsx and ouput with .gdx file extensions.


    Returns:
        tuple: paths of new GDX input files.
    """
    data_input_xlsx_abspath = os.path.join(input_path, file_basename + ".xlsx")
    data_input_gdx_abspath = os.path.join(gdx_path, file_basename + ".gdx")

    if gams_dir is not None:
        if os.path.isdir(gams_dir):
            pass
        else:
            raise Exception(f"gams_dir: '{gams_dir}' is incorrect. Verify the correct gams location \n" + \
            "                     in your computer. Replace it in project_variables.csv")
    
    
    try:
        exceltogdx(excel_file= data_input_xlsx_abspath, gdx_file= data_input_gdx_abspath,gams_dir= gams_dir)
    except RuntimeError:
        raise Exception('HINT: This error is due to GAMS program is not detected. \n' + \
        '                 Make sure GAMS_DIR is an environment variable in the PATH, or \n' + \
        '                 add "gams_dir" key to project_variables.csv with it location as value.')
        
    return data_input_gdx_abspath

def generateInputGDX_feat(config_folder: str, gdx_path: str, gams_dir=None) -> tuple:
    """Generates feat_node gdx files.

    Args:
        config_folder (str): path referring to folder location that contains project_variables.csv.
        gdx_path (str): path referring to folder location that contains input gdx files to be generated.

    Returns:
        tuple: first position a list of active model features. Second position a path of new GDX file.
    """
    # import of features_node_selection.csv <-- always required
    file_abspath = os.path.join(config_folder, "features_node_selection.csv")
    file_abspath_temp = os.path.join(settings.TMP_DIR_ABS,"tmp_features_node_selection.csv")
    os.makedirs(settings.TMP_DIR_ABS, exist_ok=True)

    # create temporay csv file w/o comment column
    original = pd.read_csv(file_abspath, index_col="feature")

    feature_configuration = original.drop("comment", axis=1)
    feature_configuration.to_csv(file_abspath_temp)

    # read csv and create gdx
    feat_node_gdx_abspath = gams_feat_node(gams_dir=gams_dir, csv_path=file_abspath_temp, gdxoutputfolder=gdx_path)

    # get active global features
    active_gf = gdx_get_set_coords(filename=feat_node_gdx_abspath, setname="features")

    return (active_gf, feat_node_gdx_abspath)

def prepareGAMSAPI(working_directory: str, gams_dir: str) -> tuple:
    """Generates GAMS instances of workspace, checkpoint, and options.

    Args:
        working_directory (str): path of GAMS working directory. GAMS will host all working files for the optimization.

    Returns:
        tuple: 3-element tuple containing

        - **ws** (*GAMS workspace object*): Base class of the gams namespace, used for initiating GAMS objects (e.g. GamsDatabase and GamsJob) by an "add" method of GamsWorkspace. Unless a GAMS system directory is specified during construction of GamsWorkspace, GamsWorkspace determines the location of the GAMS installation automatically. Aorking directory (the anchor into the file system) can be provided when constructing the GamsWorkspace instance. It is used for all file-based operations.
        - **cp** (*GAMS execution Checkpoint*): A GamsCheckpoint class captures the state of a GamsJob after the GamsJob.run method has been carried out. Another GamsJob can continue (or restart) from a GamsCheckpoint.
        - **opt** (*GAMS options object*): Stores and manages GAMS options for a GamsJob and GamsModelInstance.
    """

    # define directories and create GAMS workspace
    ws = GamsWorkspace(
        system_directory=gams_dir, working_directory=working_directory, debug=DebugLevel.KeepFiles
    )
    version = GamsWorkspace.api_version
    print("GAMS version: ", version)
    print("MainDir ---->: ", ws.working_directory)
    cp = ws.add_checkpoint()
    opt = GamsOptions(ws)
    return (ws, cp, opt)

def defineGAMSOptions_dir(opt: GamsOptions, model_dir: str) -> GamsOptions:
    """
    Defines global and control options and hands them over to the GAMS options object.
    Args:
        opt (GamsOptions): stores and manages GAMS options for a GamsJob and GamsModelInstance.
        model_dir (str): pass to GAMS the loaction of the model folder.
    Returns:
        GamsOptions: updated GAMS options.
    """
    opt.defines["py_modeldir"] = f'"{model_dir+os.sep}"'
    return opt

def defineGAMSOptions_proj(opt: GamsOptions, project_vars: dict, model_name: str = 'DIETER') -> GamsOptions:
    """
    Defines global and control options and hands them over to the GAMS options object.
    Args:
        opt (GamsOptions): stores and manages GAMS options for a GamsJob and GamsModelInstance.
        project_vars (dict): project variables collected from project_variables.csv.
        model_name (str): model name.
    Returns:
        GamsOptions: updated GAMS options.
    """
    custom_hour_exists = False
    global_options = settings.MODEL_CONFIG[model_name]['project_features']
    for k in project_vars.keys():
        if k in global_options:
            if (project_vars[k] == "yes") or (project_vars[k] == "no"):
                if k == "dispatch_only":
                    opt.defines[str("py_dispatch_only")] = (
                        "*" if project_vars[k] == "yes" else "''"
                    )
                    opt.defines[str("py_investment")] = (
                        "''" if project_vars[k] == "yes" else "*"
                    )
                else:
                    opt.defines[str("py_" + k)] = (
                        "*" if project_vars[k] == "yes" else "''"
                    )
            elif k == "define_h_set":
                if model_name == 'DIETER':
                    custom_hour_exists = True
                if project_vars[k]:
                    # provides gams string for h set from h1 to define_h_set, eg. h1*h8760
                    gams_h_set_string = f'"{project_vars[k]}"'
                    opt.defines[str("py_end_hour")] = "'*'"
                    opt.defines[str("py_h_set")] = gams_h_set_string
                else:
                    # if define_h_set is left in blank in 'project_variables.csv'
                    opt.defines[str("py_end_hour")] = "''"
                    opt.defines[str("py_h_set")] = "''"
            elif k == 'base_year':
                if model_name == 'DIETER':
                    print('')
                    print('WARNING: DEPRECATION from DIETER > 1.5.0 and dieterpy 1.6.0')
                    print('         "base_year" in project_variables.csv has been removed.')
                    print('         "year" was also removed from all parameters in timeseries_input.xlsx')
                    print('')
                    opt.defines[str("py_" + k)] = "'{}'".format(str(project_vars[k]))
            else:
                opt.defines[str("py_" + k)] = "'{}'".format(str(project_vars[k]))
        elif k in ['end_hour']:  # deprecation message
            if model_name == 'DIETER':
                custom_hour_exists = True
                print('')
                print('WARNING: DEPRECATION from DIETER > 1.5.0 and dieterpy 1.6.0')
                print('         "end_hour" in project_variables.csv has been replaced by "define_h_set"')
                print('         Please, replace in project_variables.csv end_hour by define_h_set.')
                print('         The new value is the GAMS notation to define sets e.g. h1*h8760 or t0001*t8760 depending on your timeseries inputs.')
                print('         The process will continue but h set will not be overwritten. Using h as defined in timeseries_input.xlsx')
                print('')
                # If define_h_set is left in blank in 'project_variables.csv'
                opt.defines[str("py_end_hour")] = "''"
                opt.defines[str("py_h_set")] = "''"
        else:
            continue
    if model_name == 'DIETER':
        if not custom_hour_exists:
            print("project_variables.csv does not contain either 'end_hour' nor 'define_h_set' feature.")
            opt.defines[str("py_end_hour")] = "''"
            opt.defines[str("py_h_set")] = "''"
    return opt

def defineGAMSOptions_feat(opt: GamsOptions, glob_feat_dc: dict) -> GamsOptions:
    """
    Defines global and control options and hands them over to the GAMS options object.

    Args:
        opt (GamsOptions): stores and manages GAMS options for a GamsJob and GamsModelInstance.
        glob_feat_dc (dict): contains GAMS model features and their activation case '*' or ''.

    Returns:
        GamsOptions: updated GAMS options.
    """
    # define global features to (de)activate model modules
    for k, v in glob_feat_dc.items():
        opt.defines[str("py_" + k)] = v

    # define features set acc. to list of all global features
    feature_string = ",".join(list(glob_feat_dc.keys()))
    opt.defines[str("py_feature_set")] = '"' + feature_string + '"'
    return opt

def defineGAMSOptions_gdx(opt: GamsOptions, gdx_abspaths_dc: dict) -> GamsOptions:
    """
    Defines global and control options and hands them over to the GAMS options object.

    Args:
        opt (GamsOptions): stores and manages GAMS options for a GamsJob and GamsModelInstance.
        gdx_abspaths_dc (dict): contains all GDX input paths

    Returns:
        GamsOptions: updated GAMS options.
    """
    # add absolute path of gdx files
    print("func: defineGAMSOptions_gdx passes 'py_name_gdx'")
    for name, abspath in gdx_abspaths_dc.items():
        py_name = "py_" + name + "_gdx"
        opt.defines[py_name] = f'"{abspath}"'
        print(f"    name -> {name}: {py_name}")
    return opt


def writeCountryOpt(opt: GamsOptions, countries: str, topos: pd.DataFrame) -> tuple:
    """Writes the sets 'n' (nodes) and 'l' (lines) in the GAMS options. Selects automatically the correct lines for the selected nodes.

    Args:
        opt (GamsOptions): updated GAMS options.
        countries (str): countries to be written in the opt object.
        topos (pd.DataFrame): spatial structure of the model. Defines which nodes are connected with which lines.

    Returns:
        tuple: 2-element tuple containing

        - **countries** (*str*): countries to be written in the opt object.
        - **list_lines_export** (*str*): list of lines that will be used in that model run.
    """

    # Format countries to import to GAMS
    countries_gams = f'"{countries}"'
    # Format countries for line selection
    countries_formated = countries.split(",")

    # Write countries to GAMS
    opt.defines["py_iter_countries_set"] = countries_gams

    # Determine the right lines that have to be activated in the model
    list_lines = topos[topos[topos.columns.intersection(countries_formated)].notnull().sum(axis=1) == 2].index.tolist()

    # Reformat list to enter into GAMS
    list_lines_gams = ",".join(list_lines)
    list_lines_gams = '"{0}"'.format(list_lines_gams)
    # if no-connection setting from project variables
    if opt.defines["py_network_transfer"] == "''":

        if len(list_lines) == 0:
            opt.defines["py_network_transfer"] = '""'
            # Load one line to avoid other loading errors
            list_lines_gams = '"DE_FR"'
            list_lines = ["DE_FR"]
        else:
            opt.defines["py_network_transfer"] = '""'
            print(
                'Warning: "py_network_transfer" is deactivated from "project variables"'
            )

    # if only one country or no lines to be in the model:
    # activate no-connection setting
    elif len(countries_formated) == 1 or len(list_lines) == 0:
        print(
            f'Warning: "py_network_transfer" will be deactivated because only one country is selected {countries} or no lines exist in the grid topology'
        )
        # Deactivate NTC
        opt.defines["py_network_transfer"] = '""'
        # Load one line to avoid other loading errors
        list_lines_gams = '"DE_FR"'
        list_lines = ["DE_FR"]
    else:
        # Line selection based on topology
        # NTC is aready allowed from project variables
        opt.defines["py_network_transfer"] = "*"

    # Write lines to GAMS option
    opt.defines["py_iter_lines_set"] = list_lines_gams
    opt.defines["py_iter_countries_switch_on"] = "*"
    opt.defines["py_iter_countries_switch_off"] = '""'

    list_lines_export = ",".join(list_lines)

    return countries, list_lines_export

def writeConstraintOpt(
    opt: GamsOptions,
    block_iter_dc: dict,
    list_constraints: List[str],
    itercon_dc: pd.DataFrame,
) -> dict:
    """Writes the selected constraints in the GAMS opt object for all scenarios that belong to a determined block. 

    Args:
        opt (GamsOptions): updated GAMS options.
        block_iter_dc (dict): contains all symbols that will have different values through out the scenarios runs. A block contains a group of scenarios within same constraints or network topography.
        list_constraints (List[str]): List of constraints that exist in the block of scenarios.
        itercon_dc (pd.DataFrame): Panda that stores the different optional constraint see constraints_list.csv.

    Raises:
        Exception: if the constraint obtained from block does not coincide with the ones in itercon_dc (constraints_list.csv).

    Returns:
        dict: dictionary whose keys are the types of constraints while values are a corresponding constraint name to hand over GAMS model. See constraints_list.csv to identify the type of constraints and contraint manes.
    """
    selected_constraints = {}
    for constraint in itercon_dc.columns:
        if (
            constraint not in list_constraints
        ):  # If list_constraints is missing all or some constraints, it means that these constraints were not present in iteration_table.csv
            # The first option of the contraint is selected as a default option from constraints_list.csv
            i = 0
            for con in itercon_dc[constraint]:
                if pd.isna(con):
                    continue
                if i == 0:
                    opt.defines[str("py_" + con)] = "*"
                    selected_constraints[constraint] = con
                    print(
                        "%s: No constraint selected. %s is selected by default"
                        % (constraint, con)
                    )
                else:
                    opt.defines[str("py_" + con)] = '""'
                i += 1

    # Loop through all contraints
    for constraint in list_constraints:
        if block_iter_dc[constraint] == "NA":
            i = 0
            for con in itercon_dc[constraint]:
                if pd.isna(con):
                    continue
                if i == 0:
                    opt.defines[str("py_" + con)] = "*"
                    selected_constraints[constraint] = con
                    print(
                        "%s: No constraint selected. %s is selected by default"
                        % (constraint, con)
                    )
                else:
                    opt.defines[str("py_" + con)] = '""'
                i += 1
        # If one constraint selected
        else:
            # Select constraint
            constraint_config = block_iter_dc[constraint]
            if constraint_config in itercon_dc[constraint].tolist():
                # handover iteration contraint options to GAMS
                for con in itercon_dc[constraint]:
                    if pd.isna(con):
                        continue
                    else:
                        opt.defines[str("py_" + con)] = (
                            "*" if con == constraint_config else '""'
                        )
                selected_constraints[constraint] = constraint_config
                print("%s: %s" % (constraint, constraint_config))
            else:
                string_options = ",".join(itercon_dc[constraint].tolist())
                raise Exception(
                    f"{constraint_config} is not in {string_options}. Check for any typo in iteration_table.csv and compare with constraints_list.csv"
                )
    return selected_constraints


def getIterableDataDict(input_path: str, output_path: str, project_vars: dict) -> tuple:
    """Generates a dictionary that holds the information for (data) time series iteration. e.g.: scenarios that alternate time series of solar capacity factors.

    Args:
        input_path (str): String that defines the input path for the excel file.
        output_path (str): String that defines the output path for the gdx file.
        project_vars (dict): project variables collected from project_variables.csv.

    Returns:
        tuple: 2-element tuple containing

        - **iter_data_dict** (*str*): Dictioary that holds the time series iteration information.
        - **output_gdx_abspath** (*str*): string absolute path of the output gdx file.
    """

    iteration_data_file_abspath = os.path.join(
        input_path, project_vars["iteration_data_file"]
    )
    output_gdx_abspath = os.path.join(output_path, "iter_data.gdx")
    # Convert iteration data excel to GDX
    if project_vars["skip_iteration_data_file"] == "no":
        print("----------------------------")
        print("Start excel-to-GDX-conversion for iterable time series.")
        print("----------------------------")
        exceltogdx(excel_file= iteration_data_file_abspath, gdx_file= output_gdx_abspath, gams_dir=project_vars["gams_dir"])
    else:
        pass
    # Convert iteration data to Panda
    data_in = pd.read_excel(
        iteration_data_file_abspath,
        sheet_name="scenario",
        index_col=0,
        header=0,
        skiprows=1,
    )
    iter_data_set_scenario = set(data_in.loc["scenario", :].to_list())

    # Create dict of dict for scenarios, parameters, identifiers
    iter_data_dict = {}
    for entry in iter_data_set_scenario:
        # Create first scenario entry
        iter_data_dict[entry] = {}
        # Create tempory list with parameters & identifiers
        temp_para_list = data_in.loc["parameter"][data_in.loc["scenario", :] == entry].to_list()
        temp_id_list = data_in.loc["identifier"][data_in.loc["scenario", :] == entry].to_list()
        # Fill scenario keys
        for i in range(0, len(temp_id_list)):
            iter_data_dict[entry][temp_id_list[i]] = temp_para_list[i]
        # delete temp
        # del (temp_para_list, temp_id_list, entry, i)
    return iter_data_dict, output_gdx_abspath


def genStringOptData(iter_data_dict: dict, key: str) -> str:
    """Generates a string that is compatible and used in the GAMS model to overwrite parameters for time series iteration.

    Args:
        iter_data_dict (dict): dictioary that holds the time series iteration information.
        key (str): identifier that selects the correct time series iteration "scenario".

    Returns:
        str: String to write in the GAMS opt object. It will enable GAMS model to select the intended time series from iter_data GAMS table.
    """

    script = "{0}".format(
        "".join(
            [
                str(v)
                + " = "
                + "iter_data("
                + "h,"
                + "'"
                + str(k)
                + "'"
                + ","
                + "'"
                + str(key)
                + "'"
                + "); "
                for k, v in iter_data_dict[key].items()
            ]
        )
    )
    return script

def genIterationDict(project_vars: dict, path: str) -> tuple:
    """Function that creates the main iteration dict. First, a pandas DataFrame is imported from iteration_table.csv and then converted to a dictionary.

    Args:
        project_vars (dict): project variables collected from project_variables.csv.
        path (str): Input path to the folder where the main iteration csv files is hosted.

    Raises:
        Exception: scenarios_iteration must be either "yes" or "no". Check project_variables.csv

    Returns:
        tuple: 2-element tuple containing

        - **iteration_main_dict** (*dict*): Main iteration dictionary that hold all relevant information for the different scenario runs. The keys of the dictionary are the block numbers, and every block contains a dictionary with information for each contained scenario.
        - **list_constraints** (*str*): a list of constraints obtained from iteration_table.csv
    """
    # TODO: This function is too big, we should divide it into two or three parts
    if project_vars["scenarios_iteration"] == "no":
        iteration_main = pd.DataFrame({"run": [0]})
    elif project_vars["scenarios_iteration"] == "yes":
        ##### MAIN FILE
        # Read main iteration file
        if 'iteration_table_file' not in project_vars:
            iter_file = 'iteration_table.csv'
        else:
            iter_file = project_vars["iteration_table_file"]
        iteration_main = pd.read_csv(os.path.join(path, iter_file)).astype(object)
        # remove from strings leading and trailing whitespaces in columns and cells
        iteration_main = iteration_main.rename(
            columns={k: k.strip() for k in iteration_main.columns}
        )
        iteration_main = iteration_main.applymap(
            lambda x: x.strip() if isinstance(x, str) else x
        )
        # Fill empty cells with "NA"
        iteration_main = iteration_main.fillna("NA")
    else:
        raise Exception(
            'scenarios_iteration must be either "yes" or "no". Check project_variables.csv'
        )

    ##### WORK on column names and lists

    # Get all columns names
    iteration_main_columns = iteration_main.columns.to_list()
    settings.COLUMNS = iteration_main_columns
    settings.update_changes()

    # Read all constraints (currently only minRES)
    list_constraints = [col for col in iteration_main.columns if "constraint_" in col]
    # Read all feat
    list_features = [col for col in iteration_main.columns if "feature_" in col]

    # Make a list of all non-parameter elements
    block_elements = ["country_set", "time_series_scen"]
    user_defined_categories = [col for col in iteration_main.columns if "custom_" in col]
    list_no_parameters_original = user_defined_categories + block_elements + ["run"]

    list_no_parameters = []
    for col in iteration_main_columns:
        if col in list_no_parameters_original:
            list_no_parameters.append(col)

    list_no_parameters.extend(list_constraints+list_features)

    # Identify parameter
    list_parameters = list(set(iteration_main_columns) - set(list_no_parameters))

    ##### DEFINE "BLOCK" RUNS

    # Remove 'run' from list of elements
    list_no_parameters_no_run = list_no_parameters[:]
    for not_block_elem in user_defined_categories:
        if not_block_elem in list_no_parameters_no_run:
            list_no_parameters_no_run.remove(not_block_elem)

    # sort dataframe to eventually reduce the number of blocks
    if list_no_parameters_no_run:
        iteration_main = iteration_main.sort_values(
            list_no_parameters_no_run
        ).reset_index(drop=True)

    print(iteration_main)

    # Define a 'running dict'
    # e.g. {0: ('DE,FR', 'NA', 'rescon_1b'), 1: ('NA', 'NA', 'rescon_1b')}
    run_dict = {
        i: tuple(v)
        for i, v in enumerate(iteration_main[list_no_parameters_no_run].values)
    }

    # Define a 'running block list'
    run_block_list = list()

    for i in run_dict:
        if i == 0:
            block = 0
            run_block_list.append(block)
        if i > 0:
            if run_dict[i] != run_dict[i - 1]:
                block = block + 1
            else:
                pass
            run_block_list.append(block)

    # Create set

    run_block_set = set(run_block_list)
    run_block_set_list = list(run_block_set)

    # Add 'running block list' to 'iteration_main'

    iteration_main["block"] = run_block_list

    # Creat main iteration dictionary

    iteration_main_dict = {}
    list_no_parameters_no_runs_plus_usdefcats = list_no_parameters_no_run + user_defined_categories

    for block in run_block_set_list:
        iteration_main_dict[block] = {}
        # Fill non-GUSS elements
        for element in list_no_parameters_no_runs_plus_usdefcats:
            # Define entry
            entry = list(
                set(iteration_main[element][iteration_main["block"] == block])
            )[0]
            # Write in dict
            iteration_main_dict[block][element] = entry

        # Fill GUSS elements
        # Create parameter dict
        iteration_main_dict[block]["par_var"] = {}
        iteration_main_dict[block]["run_nr"] = {}
        
        i = 0
        for ix, row in iteration_main[iteration_main["block"] == block].iterrows():
            iteration_main_dict[block]["par_var"][i] = {}
            iteration_main_dict[block]["run_nr"][i] = row["run"]
            for parameter in list_parameters:
                entry_list = iteration_main[parameter][
                    iteration_main["block"] == block
                ].tolist()
                entry = entry_list[i]
                if entry == "NA":
                    pass
                else:
                    iteration_main_dict[block]["par_var"][i][parameter] = entry
            i += 1
    return iteration_main_dict, list_constraints, list_features


def convert_par_var_dict(symbols_dict: dict = None) -> tuple:
    """It convetrs the symbols to the format required to run GUSS tool.

    Args:
        symbols_dict (dict, optional): correspond to a iteration_main_dict[block]["par_var"]. Defaults to None.

    Examples:
        dictionary of current symbols notation to guss dict nomenclature.
        e.g. example of a parameter and a variable: {'ev_quant': {'body': 'ev_quant', 'dims': ('.',)}, "N_TECH.lo('DE','pv')": {'body': 'N_TECH.lo', 'dims': ('DE', 'pv')}

    Returns:
        tuple: 2-element tuple containing

        - **symb_guss_dict** (*dict*): the dictionary contains symbols' name as in the GAMS model. e.g. {0: {'ev_quant': {('.',): 500.0},'N_TECH.lo': {('DE', 'pv'): 5000.0}
        - **symbols_guss_block_set_list** (*list*): list of all symbols to be modified throughout all scenarios. e.g. ['ev_quant', 'N_TECH']
    """
    # collect all the symbols through the runs of the block
    collect_keys = []
    for k, v in symbols_dict.items():
        for kk in v.keys():
            collect_keys.append(kk)
    symbols_block_set_list = list(set(collect_keys))
    # dictionary of current symbols notation to guss dict nomenclature.
    # e.g. {'ev_quant': {'body': 'ev_quant', 'dims': ('.',)},
    #        "N_TECH.lo('DE','pv')": {'body': 'N_TECH.lo', 'dims': ('DE', 'pv')}
    symb_translate_dict = {}
    for long_symb in symbols_block_set_list:
        symb_parts = {}
        if "." in long_symb:
            symb_parts["body"] = long_symb.split("(")[0]
            elements = []
            for elem in long_symb.split("(")[1][:-1].split(","):
                for sign in [
                    "'",
                    "‘",
                    "’",
                    '"',
                ]:  # removing unwanted signs from strings e.g. "‘DE’" to 'DE'
                    elem = elem.replace(sign, "")
                elements.append(elem)
            symb_parts["dims"] = tuple(elements)
        else:
            if "(" in long_symb:
                symb_parts["body"] = long_symb.split("(")[0]
                elements = []
                for elem in long_symb.split("(")[1][:-1].split(","):
                    for sign in ["'", "‘", "’", '"']:
                        elem = elem.replace(sign, "")
                    elements.append(elem)
                symb_parts["dims"] = tuple(elements)

            else:
                symb_parts["body"] = long_symb
                symb_parts["dims"] = (".",)
        symb_translate_dict[long_symb] = symb_parts
    # create guss dict. e.g. {0: {'ev_quant': {('.',): 500.0},'N_TECH.lo': {('DE', 'pv'): 5000.0}
    symb_guss_dict = {}
    for k, v in symbols_dict.items():
        symb_guss_dict[k] = {}
        for symbs, val in v.items():
            symb_guss_dict[k][symb_translate_dict[symbs]["body"]] = {}
        for symbs, val in v.items():
            symb_guss_dict[k][symb_translate_dict[symbs]["body"]].update(
                {symb_translate_dict[symbs]["dims"]: val}
            )
    # obtain list of raw symbols. e.g. ['ev_quant', 'N_TECH']
    symbols_guss_block_list = []
    for k, v in symb_translate_dict.items():
        symbols_guss_block_list.append(v["body"])
    symbols_guss_block_set_list = list(set(symbols_guss_block_list))
    return symb_guss_dict, symbols_guss_block_set_list


def getGussVariables(project_vars: dict) -> tuple:
    """Collects from project_variables.csv the parameters related to the activation of GUSS tool.

    Args:
        project_vars (dict): project variables collected from project_variables.csv.

    Raises:
        Exception: GUSS should be "yes" or "no" in project_variables.csv
        Exception: GUSS_parallel should be "yes" or "no" in project_variables.csv
        Exception: GUSS_parallel_threads must be an integer in project_variables.csv

    Returns:
        tuple: 3-element tuple containing

        - **guss** (*bool*): activation of GUSS tool.
        - **guss_parallel** (*bool*): run GUSS tool in parallel.
        - **guss_parallel_threads** (*int*): number CPUs used to run GUSS tool in parallel.
    """
    if project_vars["GUSS"].lower() in ["yes", "no"]:
        guss = True if project_vars["GUSS"].lower() == "yes" else False
    else:
        raise Exception('GUSS should be "yes" or "no"')

    if project_vars["GUSS_parallel"].lower() in ["yes", "no"]:
        guss_parallel = (
            True if project_vars["GUSS_parallel"].lower() == "yes" else False
        )
    else:
        raise Exception('GUSS_parallel should be "yes" or "no"')
    if isinstance(project_vars["GUSS_parallel_threads"], int):
        guss_parallel_threads = project_vars["GUSS_parallel_threads"]
    elif project_vars["GUSS_parallel_threads"].isdigit():
        guss_parallel_threads = int(project_vars["GUSS_parallel_threads"])
    else:
        raise Exception("GUSS_parallel_threads must be an integer")
    return guss, guss_parallel, guss_parallel_threads


def setCountryIteration(opt: GamsOptions, block_iter_dc: dict, topography: pd.DataFrame) -> tuple:
    """It updates the activation of countries and transmission lines in GamsOptions.

    Args:
        opt (GamsOptions): updated GAMS options.
        block_iter_dc (dict): dictionary of each block with scenario parameters.
        topography (pd.DataFrame): spatial structure of the model. Defines which nodes are connected with which lines.

    Returns:
        tuple: 3-element tuple containing
        
        - **opt** (*GamsOptions*): updated GAMS options.
        - **countries** (*str*): countries to be written in the opt object.
        - **lines** (*str*): list of lines that will be used in that model run.
    """
    if "country_set" not in list(block_iter_dc.keys()):
        opt.defines["py_iter_countries_switch_on"] = '""'
        opt.defines["py_iter_countries_switch_off"] = "*"
        print("Default country set used")
        countries = "NA"
        lines = "NA"
    # No country set defined -> take default
    elif block_iter_dc["country_set"] == "NA":
        opt.defines["py_iter_countries_switch_on"] = '""'
        opt.defines["py_iter_countries_switch_off"] = "*"
        print("Default country set used")
        countries = "NA"
        lines = "NA"
    # Country set defined
    else:
        # Write country set
        countries, lines = writeCountryOpt(opt, block_iter_dc["country_set"], topography)
        print("Countries used: %s" % countries)
        print("Lines used:     %s" % str(lines))
    return opt, countries, lines

def setDataIteration(opt: GamsOptions, block_iter_dc: dict) -> tuple:
    """collect the key of time_series_scen in iteration_table.csv

    Args:
        opt (GamsOptions): updated GAMS options.
        block_iter_dc (dict): dictionary of each block with scenario parameters.

    Returns:
        tuple: 2-element tuple containing
        
        - **opt** (*GamsOptions*): updated GAMS options.
        - **data_scen_key** (*str*): identifier of time-series iteration data for a particular scenario.
    """
    # if time_series_scen is not in iteration_table.csv
    if "time_series_scen" not in list(block_iter_dc.keys()):
        # Default switch data off
        opt.defines["py_iter_data_switch"] = '""'
        data_scen_key = "NA"
        print("No time series iteration.")
    # if no data scen defined
    elif block_iter_dc["time_series_scen"] == "NA":
        # Default switch data off
        opt.defines["py_iter_data_switch"] = '""'
        data_scen_key = "NA"
        print("No time series iteration.")
    # if data scen defined
    else:
        # Switch on data iteration
        opt.defines["py_iter_data_switch"] = "*"
        data_scen_key = block_iter_dc["time_series_scen"]
        print("Time series scenario: %s" % data_scen_key)
    return opt, data_scen_key


def createModelCheckpoint(
    ws: GamsWorkspace,
    opt: GamsOptions,
    cp: GamsCheckpoint,
    model_dir_abspath: str,
    iter_data_dict: dict = None,
    data_scen_key: str = "NA",
    project_vars: dict = None,
) -> tuple:
    """Creates the initial checkpoint containing a model instance without solve command.

    Args:
        ws (GamsWorkspace): Base class of the gams namespace, used for initiating GAMS objects (e.g. GamsDatabase and GamsJob) by an "add" method of GamsWorkspace. Unless a GAMS system directory is specified during construction of GamsWorkspace, GamsWorkspace determines the location of the GAMS installation automatically. Aorking directory (the anchor into the file system) can be provided when constructing the GamsWorkspace instance. It is used for all file-based operations.
        opt (GamsOptions): Stores and manages GAMS options for a GamsJob and GamsModelInstance.
        cp (GamsCheckpoint): A GamsCheckpoint class captures the state of a GamsJob after the GamsJob.run method has been carried out. Another GamsJob can continue (or restart) from a GamsCheckpoint.
        model_dir_abspath (str): path of the folder where model.gms is hosted.
        iter_data_dict (dict, optional): dictioary that holds the time series iteration information. Defaults to None.
        data_scen_key (str, optional): identifier of time-series iteration data for a particular scenario. Defaults to "NA".
        project_vars (dict, optional): this dict should contain the key model file, if not the default file name will be used "model.gms".

    Returns:
        tuple: 2-element tuple containing

        - **cp_file** (*str*): GamsCheckpoint file path that contains defined model including the intended constraint w/o solve command.
        - **main_gdx_file** (*str*): contains the path of the resulting gdx file after the creation of the checkpoint.
    """
    start_time = time.time()
    print("Creating first checkpoint with precompiled model without solve statement.")

    file_name = project_vars['model_file']
    jobs = ws.add_job_from_file(os.path.join(model_dir_abspath, file_name))
    jobs.run(gams_options=opt, checkpoint=cp)
    if not data_scen_key == "NA":
        # Add data string
        jobs = ws.add_job_from_string(
            genStringOptData(iter_data_dict, data_scen_key), cp
        )
        # Run model
        jobs.run(checkpoint=cp)
    else:
        pass
    cp_working_dir = ws.working_directory
    # Define checkpoint-file
    cp_file = os.path.join(ws.working_directory, cp.name + ".g00")
    # copy precompiled gdx file useful for reporting and guss results
    main_gdx_file = os.path.join(ws.working_directory, jobs.out_db.name + ".gdx")
    job_name = jobs.name
    return cp_file, main_gdx_file, cp_working_dir, job_name


def getConstraintsdata(path: str) -> pd.DataFrame:
    """Get pandas dataframe of constraints_list.csv

    Args:
        path (str): path of the folder that contains constraints_list.csv.

    Returns:
        pd.DataFrame: pandas dataframe of constraints_list.csv
    """
    dataframe = pd.read_csv(os.path.join(path, "constraints_list.csv"))
    return dataframe


def getTopographydata(path: str, project_vars: dict) -> pd.DataFrame:
    """Get pandas dataframe of 'spatial' sheet name of static_input.xlsx

    Args:
        path (str): Input path to the folder where the 'static_input.xlsx' is hosted.
        project_vars (dict): project variables collected from project_variables.csv.

    Returns:
        pd.DataFrame: pandas dataframe of 'spatial' sheet name of static_input.xlsx
    """
    if 'incidence_matrix_name' in project_vars.keys():
        incidence_matrix_name = project_vars['incidence_matrix_name']
    else:
        incidence_matrix_name = 'inc' # default name in DIETER
    
    df_inc = pd.read_excel(os.path.join(path, project_vars["data_input_file"]), sheet_name="py",header=0)
    if incidence_matrix_name not in df_inc.symbol.unique():
        raise Exception(f"\n          Incidence_matrix_name '{incidence_matrix_name}' not found in 'symbol' column of 'py' sheet in {project_vars['data_input_file']} \n" + \
            "          DIETER uses 'inc'. If your model has different parameter name, include it in project_variables.csv with 'incidence_matrix_name' as key")
    
    sheet = df_inc.query(f"symbol == '{incidence_matrix_name}'")['sheet_name'].tolist()[0]
    startcell = df_inc.query(f"symbol == '{incidence_matrix_name}'")['startcell'].tolist()[0]
    rowstr = re.findall("\d+", startcell)[0]
    row = int(rowstr) - 1
    colletter = startcell.rsplit(rowstr)[0]
    index_col = col2num(colletter) - 1
    df = pd.read_excel(
                        os.path.join(path, project_vars["data_input_file"]),
                        sheet_name= sheet,
                        index_col=index_col,
                        header=0,
                        skiprows=row,
                        )
    return df.drop(axis=1,columns=df.columns[list(range(index_col))].tolist())


def getGDXoutputOptions(project_vars: dict) -> tuple:
    """Extract from project_variables.csv the formats on which the resulting GDX file will be converted. Options are CSV, PICKLE, and VAEX.

    Args:
        project_vars (dict): project variables collected from project_variables.csv.

    Raises:
        Exception: features values must be "yes" or "no"

    Returns:
        tuple: 4-element tuple containing

        - **csv_bool** (*bool*): boolean
        - **pickle_bool** (*bool*): boolean
        - **vaex_bool** (*bool*): boolean
        - **convert_cores** (*int*): number of cores used to convert the symbols from GDX file to output formats.

    """
    features = [
        "gdx_convert_parallel_threads",
        "gdx_convert_to_csv",
        "gdx_convert_to_pickle",
        "gdx_convert_to_vaex",
    ]
    selection = {}
    for feat in features:
        if feat == "gdx_convert_parallel_threads":
            selection[feat] = int(project_vars[feat])
        else:
            if project_vars[feat] == "yes":
                selection[feat] = True
            elif project_vars[feat] == "no":
                selection[feat] = False
            else:
                raise Exception(f'{feat} must be "yes" or "no"')
    convert_cores = selection["gdx_convert_parallel_threads"]
    csv_bool = selection["gdx_convert_to_csv"]
    pickle_bool = selection["gdx_convert_to_pickle"]
    vaex_bool = selection["gdx_convert_to_vaex"]
    return csv_bool, pickle_bool, vaex_bool, convert_cores


def write_iter_features_opt(
                opt: GamsOptions,
                block_iter_dc: dict,
                list_features: List[str],
                complete_list_of_features: list,
                ) -> dict:
    
    for raw_feature in complete_list_of_features:
        seudo_feature = 'feature_' + raw_feature
        passing_feat = 'py_' + raw_feature
        if seudo_feature in list_features:
            if block_iter_dc[seudo_feature] == "NA":
                opt.defines[passing_feat] = '""'
            else:
                opt.defines[passing_feat] = "*"
        else:
            opt.defines[passing_feat] = '""'
            
    feature_string = ",".join(complete_list_of_features)
    opt.defines[str("py_feature_set")] = '"' + feature_string + '"'
    return opt


def get_iter_features_data(path: str) -> list:
    complete_list_of_features = pd.read_csv(os.path.join(path, "features_list.csv"))['feature'].tolist()
    return complete_list_of_features


def generateInputGDX_iterable_feat(
                                   block_iter_dc: dict = None,
                                   iterfeat_dc: list = None,
                                   countries: str = None,
                                   topology: pd.DataFrame = None,
                                   gdx_dir: str = None,
                                   gams_dir: str = None,
                                   working_directory: str = None,
                                   ):
    
    tmp_path = working_directory
    rnd = secrets.token_hex(8)
    tmp_path_unique = os.path.join(tmp_path, rnd)
    os.makedirs(tmp_path_unique,exist_ok=True)
    
    csv_path = os.path.join(tmp_path_unique,'feat_node.csv')
    
    if countries == "NA":
        nodes_list = topology.columns.tolist()
    else:
        nodes_list = countries.split(',')
    
    data = {}
    i = 0
    for raw_feat in iterfeat_dc:
        seudo_feat = 'feature_' + raw_feat
        for n in nodes_list:
            if seudo_feat in block_iter_dc:
                if block_iter_dc[seudo_feat] == 'NA':
                    data[i] = [raw_feat,n,0]
                else:
                    nodes_selected = block_iter_dc[seudo_feat] # check if this is a list
                    if n in nodes_selected or 'all' in nodes_selected:
                        data[i] = [raw_feat,n,1]
                    else:
                        data[i] = [raw_feat,n,0]
            else:
                data[i] = [raw_feat,n,0]
            i += 1
        
    df = pd.DataFrame.from_dict(data, orient='index', columns=['features', 'n', 'value'])
    df.to_csv(csv_path,index=False)
    _, _, _, feat_gdx = gams_csv2gdx_parameters(symbol_name='feat_node',gams_dir=gams_dir,working_directory=tmp_path_unique,csv_path=csv_path,gdx_dir=gdx_dir)
    return feat_gdx