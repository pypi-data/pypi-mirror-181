# DIETERpy is electricity market model developed by the research group
# Transformation of the Energy Economy at DIW Berlin (German Institute of Economic Research)
# copyright 2021, Carlos Gaete-Morales, Martin Kittel, Alexander Roth,
# Wolf-Peter Schill, Alexander Zerrahn
"""

"""
import os
import time
import pandas as pd
import shutil
from multiprocessing import Lock, Process, Queue, Manager, cpu_count

from datetime import datetime

from .input_data import (
    getConfigVariables,
    getGlobalFeatures,
    generateInputGDX_gdx,
    generateInputGDX_feat,
    prepareGAMSAPI,
    defineGAMSOptions_dir,
    defineGAMSOptions_proj,
    defineGAMSOptions_feat,
    defineGAMSOptions_gdx,
    writeConstraintOpt,
    getIterableDataDict,
    genIterationDict,
    convert_par_var_dict,
    getGussVariables,
    setCountryIteration,
    setDataIteration,
    createModelCheckpoint,
    getConstraintsdata,
    getTopographydata,
    getGDXoutputOptions,
    get_iter_features_data,
    write_iter_features_opt,
    generateInputGDX_iterable_feat
)

from .solve import scen_solve, guss_solve, guss_parallel
from .output_data import GDXpostprocessing, solver_status_summary
from .report import CollectScenariosPerSymbol
from ..config import settings
from .. import __version__ 

try:
    import streamlit as st

    st_installed = True
except ImportError:
    st_installed = False


def main(project_file=None):
    if st_installed:
        activate_st = st._is_running_with_streamlit
    else:
        activate_st = False
    if activate_st:
        show_bar_text = st.empty()
        bar = st.progress(0)
    print("::::::::::::::::::::::::::::")
    print(f"Start dieterpy {'.'.join([str(i) for i in __version__])} prepartion.")
    print("::::::::::::::::::::::::::::")

    ##### BASIC CONFIGURATION
    BASE = {}
    start_time_global = time.time()
    start_time_global_gm = time.gmtime()
    # String time part of unique name of scenarios. Files will contain this string at the beginning
    BASE["unique"] = time.strftime("%Y%m%d%H%M%S", start_time_global_gm)

    # create location paths
    BASE[
        "BASE_DIR_ABS"
    ] = settings.BASE_DIR_ABS  # absolute path to child folder of project directory
    BASE[
        "INPUT_DIR_ABS"
    ] = (
        settings.INPUT_DIR_ABS
    )  # absolute path to folder where input_data.xlsx and timeseries.xlsx are hosted
    BASE[
        "SETTINGS_DIR_ABS"
    ] = settings.SETTINGS_DIR_ABS  # absolute path to folder where
    BASE[
        "ITERATION_DIR_ABS"
    ] = (
        settings.ITERATION_DIR_ABS
    )  # absolute path to folder where constraints_list.csv and symbols.csv are hosted
    BASE[
        "RUN_DIR_ABS"
    ] = (
        settings.RUN_DIR_ABS
    )  # absolute path to folder where gams runs "ws.working_directory"
    BASE[
        "GDX_INPUT_ABS"
    ] = (
        settings.GDX_INPUT_ABS
    )  # absolute path to folder where inputs gdx files are hosted. 'RUN_DIR_ABS'  is its parent folder
    BASE[
        "RESULTS_DIR_ABS"
    ] = (
        settings.RESULTS_DIR_ABS
    )  # absolute path to folder where model output files are hosted
    BASE[
        "MODEL_DIR_ABS"
    ] = settings.MODEL_DIR_ABS  # absolute path to folder where model.gms is hosted
    BASE[
        "TMP_DIR_ABS"
    ] = settings.TMP_DIR_ABS  # absolute path to the folder for temp files

    # import control and scenario variables from config folder
    BASE['convar_dc'] = getConfigVariables(BASE["SETTINGS_DIR_ABS"], project_file=project_file)

    if 'model_name' in BASE['convar_dc']:
        BASE['model_name'] = BASE['convar_dc']['model_name']
    else:
        BASE['model_name'] = 'DIETER'

    BASE['MODEL_CONFIG'] = settings.MODEL_CONFIG  # still thinking which for is best
    
    BASE['input_gdxfiles'] = {}
    for input_option in BASE['MODEL_CONFIG'][BASE['model_name']]['input_file_basename']:
        for variables in BASE['convar_dc']:
            if input_option in variables:
                file_base_name = BASE['convar_dc'][variables].split('.')[0]
                if BASE['convar_dc']['skip_input'] == "no":
                    BASE['input_gdxfiles'][input_option] = generateInputGDX_gdx(input_path= BASE["INPUT_DIR_ABS"], gdx_path= BASE["GDX_INPUT_ABS"], file_basename= file_base_name, gams_dir= BASE["convar_dc"]['gams_dir'])
                else:
                    BASE['input_gdxfiles'][input_option] = os.path.join(BASE["GDX_INPUT_ABS"],file_base_name + '.gdx')
                    if os.path.isfile(BASE['input_gdxfiles'][input_option]):
                        pass
                    else:
                        raise Exception(f"skip_input set 'yes' in project_variables.csv but no gdx file: {BASE['input_gdxfiles'][input_option]}")

    if BASE['MODEL_CONFIG'][BASE['model_name']]['feat_node_exists']:
        flag_node = True
        if 'iterable_features_node' in BASE['convar_dc']:
            if BASE['convar_dc']['iterable_features_node'] == 'yes':
                flag_node = False
                BASE['iterfeat_dc'] = get_iter_features_data(BASE["SETTINGS_DIR_ABS"])
            else:
                flag_node = True
        if flag_node:
            BASE['active_gf'], BASE['input_gdxfiles']['feat_node'] = generateInputGDX_feat(config_folder= BASE["SETTINGS_DIR_ABS"], gdx_path= BASE["GDX_INPUT_ABS"], gams_dir= BASE["convar_dc"]['gams_dir'])
            # get switch values for all global features
            BASE['glob_feat_dc'] = getGlobalFeatures(BASE["SETTINGS_DIR_ABS"], BASE['active_gf'])

    # Read list of constraints
    BASE['itercon_dc'] = getConstraintsdata(BASE["SETTINGS_DIR_ABS"])

    if BASE['MODEL_CONFIG'][BASE['model_name']]['topography_exists']:
        # Read in topology
        BASE['topography'] = getTopographydata(BASE["INPUT_DIR_ABS"], BASE['convar_dc'])
    else:
        BASE['topography'] = None

    if BASE['MODEL_CONFIG'][BASE['model_name']]['iterable_data_exists']:
        # Get iterable data
        BASE['data_it_dc'], BASE['input_gdxfiles']['data_it'] = getIterableDataDict(BASE["ITERATION_DIR_ABS"], BASE["GDX_INPUT_ABS"], BASE['convar_dc'])
    else:
        BASE['data_it_dc'] = None
    ##### ITERATION CONFIG
    BASE['iteration_main_dict'], BASE['list_constraints'], BASE['list_features'] = genIterationDict(BASE['convar_dc'], BASE["ITERATION_DIR_ABS"])

    # Get guss tool configuration
    BASE["guss_tool"], BASE["guss_parallel"], BASE["guss_threads"] = getGussVariables(BASE['convar_dc'])

    BASE['csv_bool'], BASE['pickle_bool'], BASE['vaex_bool'], BASE['convert_cores'] = getGDXoutputOptions(BASE['convar_dc'])

    # Get cpu cores
    cores = cpu_count()

    # this statement if for streamlit - the web tool
    if activate_st:
        show_bar_text.text(f"DIETER preparation finished")
        bar.progress(10 / 100)
    print(
        "DIETER preparation finished. It took %s minutes"
        % (round((time.time() - start_time_global) / 60, 1))
    )

    ###########################################################################
    # START LOOPING
    ###########################################################################

    print("::::::::::::::::::::::::::::")
    print("START DIETER solving")
    print("::::::::::::::::::::::::::::")

    BASE["RUNS"] = []
    BASE["tmp"] = {}
    barmax = len(BASE['iteration_main_dict'].keys())
    for block, block_iter_dc in BASE['iteration_main_dict'].items():
        print("----------------------------")
        print("Block run %s started" % block)
        print("----------------------------")
        # save temp BASE to be used later to contruct relevant BASE of each run
        BASE["tmp"][block] = {}
        BASE["tmp"][block]["str_block"] = "_b" + str(block).zfill(
            3
        )  # e.g. block=21 then after zfill(5) results 00021, five digits
        BASE["tmp"][block]["runs"] = block_iter_dc

        ############################
        # prepare GAMS API
        ############################

        ws, cp, opt = prepareGAMSAPI(BASE["RUN_DIR_ABS"], gams_dir=BASE['convar_dc']['gams_dir'])

        ############################
        # GLOBAL OPTIONS
        ############################

        opt = defineGAMSOptions_dir(opt, BASE["MODEL_DIR_ABS"])
        opt = defineGAMSOptions_proj(opt, BASE['convar_dc'], BASE['model_name'])

        ############################
        # SET ITERATION
        ############################

        opt, countries, _ = setCountryIteration(opt, block_iter_dc, BASE['topography'])

        path_cl = os.path.join(BASE["MODEL_DIR_ABS"],"countries-lines.gms")

        f = open(path_cl,"w+")
        f.write('Set n "Nodes" ' + ' / ' + countries + ' / ' + ' ;' + '\n' + 'Set l "Lines" ' + ' / ' + _ + ' / ' + ' ;')
        f.close()
        
        ############################
        # FEATURES ITERATION
        ############################
        
        if BASE['MODEL_CONFIG'][BASE['model_name']]['feat_node_exists']:
            flag_node = True
            if 'iterable_features_node' in BASE['convar_dc']:
                if BASE['convar_dc']['iterable_features_node'] == 'yes':
                    flag_node = False
                    opt = write_iter_features_opt(opt, block_iter_dc, BASE['list_features'], BASE['iterfeat_dc'])  # TODO here a function with arg: 'block_iter_dc' to extract all features pass a * and the remainig ''
                    BASE['input_gdxfiles']['feat_node'] = generateInputGDX_iterable_feat(block_iter_dc=block_iter_dc,iterfeat_dc=BASE['iterfeat_dc'],countries=countries, topology=BASE['topography'], gdx_dir= BASE["GDX_INPUT_ABS"], gams_dir= BASE["convar_dc"]['gams_dir'], working_directory=BASE["TMP_DIR_ABS"])
                else:
                    flag_node = True
            if flag_node:
                opt = defineGAMSOptions_feat(opt, BASE['glob_feat_dc'])

        ############################
        # CONSTRAINT ITERATION
        ############################

        # For every constraint, write GAMS option
        choosen_constraints = writeConstraintOpt(opt, block_iter_dc, BASE['list_constraints'], BASE['itercon_dc'])  # TODO use as an example for feat

        ###############################
        # DATA (TIME SERIES) ITERATION
        ###############################

        opt, data_scen_key = setDataIteration(opt, block_iter_dc)
        
        ###############################
        # FEEDING GDX FILES
        ###############################        
        
        opt = defineGAMSOptions_gdx(opt, BASE['input_gdxfiles']) # New feat_node can be updated here

        ###############################
        # Model Checkpoint and GDX
        ###############################

        cp_file, main_gdx_file, cp_working_dir, job_name = createModelCheckpoint(ws, opt, cp, BASE["MODEL_DIR_ABS"], BASE['data_it_dc'], data_scen_key, BASE['convar_dc'])

        BASE["tmp"][block]["cp_file"] = cp_file
        BASE["tmp"][block]["main_gdx_file"] = main_gdx_file
        # new implementation to copy lst files
        BASE["tmp"][block]["cp_working_dir"] = cp_working_dir
        BASE["tmp"][block]["job_name"] = job_name

        ############################
        # PARAMETER
        ############################

        # Create parameter dict that will be used in this block
        dict_parameters_block = block_iter_dc["par_var"]

        #######################################################################
        # RUN MODEL
        #######################################################################

        # Collect information of used options for pass-through to gdx file name

        BASE["tmp"][block]["runs"].update(choosen_constraints)
        BASE["tmp"][block]["used_constraints"] = "-".join(list(choosen_constraints.values()))
        BASE["tmp"][block]["used_countries"] = countries.replace(",", "-")
        BASE["tmp"][block]["used_data"] = data_scen_key

        # run several parameter/variable configurations per block
        if BASE["guss_tool"]:
            guss_symbol_block, symbs = convert_par_var_dict(
                symbols_dict=dict_parameters_block
            )
            if BASE["guss_parallel"]:
                with Manager() as manager:
                    block_results = manager.list()
                    queue = Queue()
                    for run, dc in guss_symbol_block.items():
                        queue.put((run, dc))
                    count = len(guss_symbol_block)
                    if BASE["guss_threads"] == 0:
                        nr_workers = min(count, cores)
                    elif BASE["guss_threads"] <= min(count, cores):
                        nr_workers = BASE["guss_threads"]
                    else:
                        print(
                            "GUSS_parallel_threads:",
                            BASE["guss_threads"],
                            "is greater than ",
                            min(count, cores),
                            ". Minimum value is selected",
                        )
                        nr_workers = min(count, cores)
                    print("nr_workers", nr_workers)
                    queue_lock = Lock()
                    print_lock = Lock()
                    processes = {}
                    for i in range(nr_workers):
                        processes[i] = Process(
                            target=guss_parallel,
                            args=(
                                block_results,
                                queue,
                                queue_lock,
                                print_lock,
                                symbs,
                                BASE,
                                block,
                            ),
                        )
                        processes[i].start()
                    for i in range(nr_workers):
                        processes[i].join()
                    scenario_collection = list(block_results)
                BASE["RUNS"] += scenario_collection
            else:
                scenario_collection = guss_solve(guss_symbol_block, symbs, BASE, block)
                BASE["RUNS"] += scenario_collection
        # no guss tool then sequential model solve
        else:
            scenario_collection = []
            for run, dc in dict_parameters_block.items():
                # Solve DIETER model
                scenario_collection += scen_solve(dc, BASE, run, block)
            BASE["RUNS"] += scenario_collection
        if activate_st:
            show_bar_text.text(f"Problem block {block+1} of {barmax} finished")
            bar.progress((10 + (70 / barmax) * (block + 1)) / 100)

        # Delete temporary country-line file
        os.remove(path_cl)

    summary_status = solver_status_summary("direct", BASE)
    print(summary_status)
    time.sleep(2)

    # if not BASE['pickle_bool']:
    #     with open(
    #         os.path.join(
    #             BASE["RESULTS_DIR_ABS"], BASE["unique"] + "_scenario_collection.yml"
    #         ),
    #         "w",
    #     ) as f:
    #         BASE['convar_dc']['gams_dir'] = 'none'
    #         yaml.dump(BASE, f)

    elapsed_time_global = time.time() - start_time_global

    print("::::::::::::::::::::::::::::::::::::")
    print("ALL RUNS FINISHED")
    print("::::::::::::::::::::::::::::::::::::")
    print("Total calculation time:")
    print("Seconds: %s" % (round((elapsed_time_global), 2)))
    print("Minutes: %s" % (round((elapsed_time_global) / 60, 1)))
    print("Hours:   %s" % (round((elapsed_time_global) / 3600, 1)))
    print("::::::::::::::::::::::::::::::::::::")

    if activate_st:
        st.write("Optimization Status")
        st.dataframe(summary_status)

    print("GDX FILES CONVERSION")
    print("::::::::::::::::::::::::::::::::::::::")
    GDXpostprocessing(
        method="direct",
        input=BASE["RUNS"],
        csv_bool=BASE['csv_bool'],
        pickle_bool=BASE['pickle_bool'],
        vaex_bool=BASE['vaex_bool'],
        cores_data=BASE['convert_cores'],
        gams_dir=BASE['convar_dc']['gams_dir'],
        base=BASE,
    )
    settings.RESULT_CONFIG = BASE

    print("::::::::::::::::::::::::::::::::::::::")
    print("")
    if activate_st:
        show_bar_text.text(f"GDX files conversion finished")
        bar.progress(85 / 100)

    if BASE['convar_dc']["report_data"] == "yes":
        print("REPORTING FILES")
        print("::::::::::::::::::::::::::::::::::::::")
        paths = [rundc["PKL_path"] for rundc in BASE["RUNS"]]
        Data = CollectScenariosPerSymbol(paths=paths, cores=BASE['convert_cores'])
        Data.collectinfo()
        Data.join_all_symbols_from_reporting()

        if activate_st:
            show_bar_text.text(f"Reporting files created")
            bar.progress(95 / 100)
    if activate_st:
        time.sleep(2)
        show_bar_text.text(f"Program finished successfully")
        bar.progress(100 / 100)

    # Delete tmp folder
    if os.path.exists(BASE["TMP_DIR_ABS"]):
        shutil.rmtree(BASE["TMP_DIR_ABS"])

    if 'move_output' in BASE['convar_dc']:
        if BASE['convar_dc']['move_output'] == "yes":
        
            # Move folders to "output"

            # Define folder name based on current time stamp
            home            = os.getcwd()
            moment          = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            path_new_folder = os.path.join(home,'output',moment)

            # Create folder
            from pathlib import Path
            Path(path_new_folder).mkdir(parents=True, exist_ok=True)

            # Move
            if os.path.isdir('project_files/data_output'):
                shutil.move('project_files/data_output',path_new_folder)
            else:
                pass
            
            if os.path.isdir('project_files/report_files'):
                shutil.move('project_files/report_files',path_new_folder)
            else:
                pass
            
            print("")
            print("Files moved to /output")
            print("")
            
        else:
            pass
    else:
        print("")
        print("No 'move_output' feature identified in settings/project_variables.csv")
        print("Files not moved")
        print("")

    shutil.rmtree(BASE["RUN_DIR_ABS"])
    shutil.rmtree(BASE["GDX_INPUT_ABS"])

    print("::::::::::::::::::::::::::::::::::::::")
    print(":::::::::::::::FINISHED:::::::::::::::")
    print("::::::::::::::::::::::::::::::::::::::")
    
    return None


if __name__ == "__main__":
    main()
