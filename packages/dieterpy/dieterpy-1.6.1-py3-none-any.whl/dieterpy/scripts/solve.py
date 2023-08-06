# DIETERpy is electricity market model developed by the research group
# Transformation of the Energy Economy at DIW Berlin (German Institute of Economic Research)
# copyright 2021, Carlos Gaete-Morales, Martin Kittel, Alexander Roth,
# Wolf-Peter Schill, Alexander Zerrahn
"""

"""
import os
import time
import gc
import yaml
import json
import itertools
import secrets
import pandas as pd

from shutil import copyfile
from gams import (
    GamsWorkspace,
    GamsOptions,
    DebugLevel,
    UpdateAction,
    VarType,
    GamsException,
    GamsModifier,
    GamsModelInstanceOpt,
)

from .gdx_handler import gdx_get_symb_info, gdx_get_set_coords, gdx_get_summary
from .util import OutputStream
from .output_data import get_solver_status
from ..config import settings


def scen_solve(scen_run, base, run, block):
    """
    Function that imports all information, solves the DIETER model, and
    exports the results.

    Parameters
    ----------
    workdir : string
        Working dictionary for the GAMS api.
    cp_file : GAMS model instance
        Contains defined model including the intended constraint w/o solve
        command.
    scen_run : dict
        Dictionary that holds information on parameters and variables for this
        specific block run.
    str_country : string, optional
        String that holds the countries selected in the main iteration file.
        Used for the GDX-file name. The default is None.
    str_lines : string, optional
        String that holds the lines selected according to the selected countries
        in the main iteration file. Used for the GDX-file name.
        The default is None.
    str_constraints : string, optional
        String that holds the configs of the constraints selected in the main
        iteration file. Used for the GDX-file name.
        The default is None.
    str_data : string, optional
        String that holds the scenario key for data iteration
        selected in the main iteration file. Used for the GDX-file name.
        The default is None.

    Returns
    -------
    None.

    """
    convar_dc = base['convar_dc']
    if 'model_name' in convar_dc:
        MODEL = convar_dc['model_name']
        MODEL_sense = convar_dc['model_sense']
        MODEL_prob = convar_dc['model_problem']
        MODEL_obj = convar_dc['model_objective']
        MODEL_solver = convar_dc['model_solver']
    else:
        MODEL = 'DIETER'
        MODEL_sense = 'min'
        MODEL_prob = 'lp'
        MODEL_obj = 'Z'
        MODEL_solver = ''

    gams_dir = convar_dc['gams_dir']
    save_all_symbols = True if convar_dc['save_all_symbols'] == 'yes' else False

    tmp = {}
    tmp["BASE_DIR_ABS"] = base["BASE_DIR_ABS"]
    tmp["RUN_DIR_ABS"] = base["RUN_DIR_ABS"]
    tmp["RESULTS_DIR_ABS"] = base["RESULTS_DIR_ABS"]

    cp_file = base["tmp"][block]["cp_file"]
    maingdx = base["tmp"][block]["main_gdx_file"]
    cp_working_dir = base["tmp"][block]["cp_working_dir"]
    print(f"{cp_working_dir}")
    job_name = base["tmp"][block]["job_name"]

    tmp_path = base["TMP_DIR_ABS"]
    rnd = secrets.token_hex(8)
    tmp_path_unique = os.path.join(tmp_path, rnd)
    tmp["TMP_PATH"] = tmp_path_unique
    tmp["run_orig"] = run
    tmp["id"] = (
        "Run_"
        + str(base["tmp"][block]["runs"]["run_nr"][run]).zfill(4)
        + "_"
        + base["unique"]
        + base["tmp"][block]["str_block"]
        + "_r"
        + str(run).zfill(4)
    )
    tmp["block"] = block
    tmp["id_dir"] = os.path.join(tmp["RESULTS_DIR_ABS"], tmp["id"])
    tmp["stdout_file"] = os.path.join(tmp["id_dir"], tmp["id"] + "_gams_stdout.txt")
    tmp["tmp_gdx"] = ""
    tmp["job_lst"] = os.path.join(tmp["id_dir"], tmp["id"] + "_job.lst")
    tmp["checkpoint_lst"] = os.path.join(tmp["id_dir"], tmp["id"] + "_CP.lst")
    tmp["checkpoint_gdx"] = ""
    tmp["main_gdx"] = os.path.join(tmp["id_dir"], tmp["id"] + ".gdx")
    tmp["diff_gdx"] = ""
    tmp["config_file"] = os.path.join(tmp["id_dir"], tmp["id"] + "_config.yml")
    tmp["config_json"] = os.path.join(tmp["id_dir"], tmp["id"] + ".json")
    os.makedirs(tmp_path_unique, exist_ok=True)

    ws = GamsWorkspace(
        system_directory=gams_dir,
        debug=DebugLevel.KeepFiles, 
        working_directory=tmp_path_unique
    )

    print("working_directory:", ws.working_directory)

    cp = ws.add_checkpoint(cp_file)
    # Start new code: locate parameters and variables following order in the iteration_table.csv (It works only without GUSS)
    kkk = []
    vvv = []
    for k, v in scen_run.items():
        kkk.append(k)
        vvv.append(v)
        
    nk = []
    nv = []
    for column in settings.COLUMNS:
        if column in kkk:
            nk.append(column)
            nv.append(vvv[kkk.index(column)])

    parameters_str = [k + " = " + str(v) + "; " for k, v in zip(nk,nv)]


    cp_symbols_dicts = gdx_get_summary(gams_dir=gams_dir, filename=maingdx)
    cp_sets_list = [symb['name'] for symb in cp_symbols_dicts if symb['type'] == 'set' if symb['name'] != '*']
    cp_symbols_list = [symb['name'] for symb in cp_symbols_dicts]

    reporting_symbols_path = os.path.join(base["SETTINGS_DIR_ABS"], "reporting_symbols.csv")
    if not save_all_symbols:
        if os.path.exists(reporting_symbols_path):
            reporting_flag = True
            symbol_df = pd.read_csv(reporting_symbols_path)
            symbols_list  = [symb.split('.')[0] for symb in symbol_df.stack().dropna().tolist()]
            symbols_list_middle = [symb for symb in symbols_list if symb in cp_symbols_list]
            symbols_list_definite = sorted(set(symbols_list_middle + cp_sets_list))
            symbols_string = ','.join(symbols_list_definite)
            symbols_script = f"\n execute_unload '{tmp['main_gdx']}', {symbols_string};"
            print(f"These symbols will be dumped to the gdx file:")
            print(f"{symbols_list_middle}")
            print('')
        else:
            print("'save_all_symbols' set as 'no' in project variables but no 'reporting_symbols.csv' found in settings folder.")
            print("Thus, all symbols will be dumped to the GDX files")
            reporting_flag = False
            symbols_script = ''
    else:
        reporting_flag = False
        symbols_script = ''


    # End new code
    
    job = ws.add_job_from_string(
        "".join(parameters_str)
        + f"\n solve {MODEL} using {MODEL_prob} {MODEL_sense} {MODEL_obj};\n ms={MODEL}.modelstat;\n ss={MODEL}.solvestat;"
        + symbols_script
        ,
        cp,
    )
    opt = GamsOptions(ws)
    opt.optdir = tmp["RUN_DIR_ABS"]
    opt.solvelink = 0
    if not MODEL_solver:
        solver = "cplex"
    else:
        solver = MODEL_solver


    opt.all_model_types = solver
    opt.optfile = 1
    copyfile(
        os.path.join(tmp["RUN_DIR_ABS"], f"{solver}.opt"),
        os.path.join(ws.working_directory, f"{solver}.opt"),
    )

    # for job.out_db:



    os.makedirs(tmp["id_dir"], exist_ok=True)
    start_t = time.time()
    with OutputStream(tee=True, logfile=tmp["stdout_file"]) as output_stream:
        job.run(opt, output=output_stream)

    solver_msg = get_solver_status(tmp["stdout_file"])
    tmp["solver_msg"] = solver_msg

    symbs_dict = base["tmp"][block]["runs"]["par_var"][run]
    countries = base["tmp"][block]["used_countries"]
    # lines = base['tmp'][block]['used_lines']
    constraints = base["tmp"][block]["used_constraints"]
    data_scen = base["tmp"][block]["used_data"]

    tmp["modelstatus"] = job.out_db["ms"].find_record().value
    tmp["solverstatus"] = job.out_db["ss"].find_record().value
    tmp["system_costs"] = job.out_db["Z"].find_record().level
    # tmp['summary'] = countries + '_' + lines + '_' + constraints + '_' + data_scen + '_' + \
    tmp["summary"] = (
        countries
        + "_"
        + constraints
        + "_"
        + data_scen
        + "_"
        + "_".join([k + "_" + str(v) for k, v in symbs_dict.items()])
    )
    tmp["summary_file"] = os.path.join(
        tmp["RESULTS_DIR_ABS"],
        tmp["id"]
        + "_"
        + str(tmp["modelstatus"])
        + "_"
        + str(round(tmp["system_costs"] / 1000000, 1))
        + "_"
        + tmp["summary"]
        + ".txt",
    )
    tmp["config"] = {
        k: v
        for k, v in base["tmp"][block]["runs"].items()
        if k not in ["par_var", "run_nr"]
    }
    # if 'country_set' in list(tmp['config'].keys()):
    #     tmp['config']['lines'] = lines
    tmp["config"].update({k: v for k, v in symbs_dict.items()})
    tmp["config"].update({"solver_msg": solver_msg, "long_id": tmp["id"],"run":base["tmp"][block]["runs"]["run_nr"][run]})
    tmp["guss_tool"] = base["guss_tool"]
    tmp["guss_config"] = ""
    tmp["SETTINGS_DIR_ABS"] = base["SETTINGS_DIR_ABS"]
    tmp["reporting_symbols_file"] = reporting_symbols_path
    tmp["csv_dir"] = os.path.join(tmp["id_dir"], "csv")

    with open(tmp["config_file"], "w") as yml:
        yaml.dump(tmp, yml)  # yaml.dump(tmp['config'], yml)

    with open(tmp["config_json"], "w") as jsonfile:
        jsondict = {}
        jsondict['name'] = tmp['id']
        jsondict['metadata'] = tmp['config']
        json.dump(jsondict, jsonfile, indent = 4)

    copyfile(os.path.join(cp_working_dir, job_name+".lst"), tmp["checkpoint_lst"])
    copyfile(os.path.join(ws.working_directory, job.name + ".lst"), tmp["job_lst"])

    if not reporting_flag:
        job.out_db.export(tmp["main_gdx"])
    gc.collect()

    end_t = time.time()
    print("-------------------------------------------------------------")
    print("Run: %s" % run)
    print("-------------------------------------------------------------")
    print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    print("Run id:", tmp["id"])
    print("Run config:", tmp["config"])
    print("Model status:", tmp["modelstatus"])
    print("Solver status:", tmp["solverstatus"])
    print("Total system costs:", tmp["system_costs"])
    print("")
    print("Elapsed time:", end_t - start_t, "sec")
    print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    print("")
    return [tmp]


def clearModifiers(dcmodifier, maingdx, gams_dir=None):

    for k, v in dcmodifier.items():
        if "." in k:
            raw_symb = k.split(".")[0]
        else:
            raw_symb = k
        _, info = gdx_get_symb_info(gams_dir=gams_dir, filename=maingdx, symbol=raw_symb)
        if info["type"] == "parameter":
            idx_modifier = 0
        elif info["type"] == "variable":
            idx_modifier = 2
        elif info["type"] == "equation":
            raise Exception("Equations not implemented yet")
        else:
            raise Exception(f"""{k} has info[type] not recognized""")
        # clear previous run data.
        v[idx_modifier].clear()
    return dcmodifier


def setSymbolsValues(dcmodifier, dc, maingdx, gams_dir=None):
    #  dc has symbols from our block dictionary of a specific run
    for symb, dcc in dc.items():
        if "." in symb:
            raw_symb = symb.split(".")[0]
        else:
            raw_symb = symb
        # info of the symbol recalled from precompiled GDX file
        _, info = gdx_get_symb_info(gams_dir=gams_dir, filename=maingdx, symbol=raw_symb)
        if info["type"] == "parameter":
            idx_modifier = 0
        elif info["type"] == "variable":
            idx_modifier = 2
        elif info["type"] == "equation":
            raise Exception("To modify equations is not implemented yet")
        else:
            raise Exception(f'{symb} has info["type"] not recognized')

        # porviding symbols values for the current run.
        for dom, v in dcc.items():
            if dom == (".",):  # dimensionless symbol
                dcmodifier[symb][idx_modifier].add_record().value = v
            else:
                # this section checks if the coords provided belong to a set name 'N_STO_P('n','sto')' or are set elements 'N_STO_P('FR','sto1')'
                # or combination of both 'N_STO_P('FR','sto')'
                # if it is a set element 'FR' is added directly to the matrix and is recognised by '0'
                # if it is a set name 'n' then is colected all elements of the set and added to the matrix
                # finally, the matrix looks like this [['FR','DE','IT'],['sto1','sto2']] for two-dims parameter apply itertools.product() resulting [('FR','sto1'),('FR','sto2')...]
                # all the combinations will be recorded with the same value v.
                activation = []
                for i in range(
                    info["nrdims"]
                ):  # info['dims'] -> info['nrdims'] e.g. ['n','sto'] ->  2
                    # print(dom, info['dims'][i])
                    if info["dims"][i] == dom[i]:  # dom looks like ('FR','sto')
                        activation.append(dom[i])
                    else:
                        activation.append(
                            "0"
                        )  # resulting activation list e.g. ['0','sto']
                matrix = []
                for j, setelem in enumerate(activation):
                    if setelem != "0":
                        matrix.append(
                            gdx_get_set_coords(
                                gams_dir=gams_dir, filename=maingdx, setname=setelem
                            )
                        )  # e.g. ['sto1','sto2',...]
                    else:
                        matrix.append([dom[j]])  # e.g. ['FR']
                allcombination = [
                    i for i in itertools.product(*matrix)
                ]  # e.g. [('FR','sto1'), ('FR','sto2'),...]
                for coord in allcombination:
                    dcmodifier[symb][idx_modifier].add_record(
                        coord
                    ).value = v  # v is always the same for all combinations. e.g. 'N_STO_P('FR','sto') = 100' then v = 100
    return dcmodifier


def guss_parallel(result, queue, queue_lock, print_lock, symbs, base, block):

    convar_dc = base['convar_dc']
    if 'model_name' in convar_dc:
        MODEL = convar_dc['model_name']
        MODEL_sense = convar_dc['model_sense']
        MODEL_prob = convar_dc['model_problem']
        MODEL_obj = convar_dc['model_objective']
        MODEL_solver = convar_dc['model_solver']
    else:
        MODEL = 'DIETER'
        MODEL_sense = 'min'
        MODEL_prob = 'lp'
        MODEL_obj = 'Z'
        MODEL_solver = ''

    gams_dir = convar_dc['gams_dir']

    tmp = {}
    tmp["BASE_DIR_ABS"] = base["BASE_DIR_ABS"]
    tmp["RUN_DIR_ABS"] = base["RUN_DIR_ABS"]
    tmp["RESULTS_DIR_ABS"] = base["RESULTS_DIR_ABS"]

    cp_file = base["tmp"][block]["cp_file"]
    maingdx = base["tmp"][block]["main_gdx_file"]
    cp_working_dir = base["tmp"][block]["cp_working_dir"]
    job_name = base["tmp"][block]["job_name"]

    tmp_path = base["TMP_DIR_ABS"]
    rnd = secrets.token_hex(8)
    tmp_path_unique = os.path.join(tmp_path, rnd)
    tmp["TMP_PATH"] = tmp_path_unique
    os.makedirs(tmp_path_unique, exist_ok=True)

    ws = GamsWorkspace(
        system_directory=gams_dir,
        # debug=DebugLevel.KeepFiles, 
        working_directory=tmp_path_unique
    )

    print("working_directory:", ws.working_directory)
    cp = ws.add_checkpoint(cp_file)
    opt = GamsOptions(ws)
    opt.optdir = tmp["RUN_DIR_ABS"]
    opt.solvelink = 0
    if not MODEL_solver:
        solver = "cplexd"
    else:
        solver = MODEL_solver
    opt.all_model_types = solver
    opt.optfile = 1
    copyfile(
        os.path.join(tmp["RUN_DIR_ABS"], f"{solver}.opt"),
        os.path.join(ws.working_directory, f"{solver}.opt"),
    )
    
    mi = cp.add_modelinstance()
    mi_opt = GamsModelInstanceOpt(
        solver=solver, opt_file=1, no_match_limit=999999999, debug=True
    )

    dcmodifier = {}
    for (
        sy
    ) in (
        symbs
    ):  # identify the symbols with different type and set modifier for each symbols
        if "." in sy:
            raw_symb = sy.split(".")[0]
            update_action = sy.split(".")[1].lower()
        else:
            raw_symb = sy
        _, info = gdx_get_symb_info(gams_dir=gams_dir, filename=maingdx, symbol=raw_symb)
        dim = info["nrdims"]
        txt = info["desc"]
        if info["type"] == "parameter":
            # print('raw:', raw_symb, 'sy:', sy)
            symbol_instance = mi.sync_db.add_parameter(sy, dim, txt)
            dcmodifier[sy] = [symbol_instance]
        elif info["type"] == "variable":
            # check if that variable has already been added.
            try:
                symbol_instance = mi.sync_db.get_variable(raw_symb)
            except GamsException as e:
                # print(f"{e}")
                symbol_instance = mi.sync_db.add_variable(
                    raw_symb, dim, VarType.Positive
                )
            # add to mi.sync_db
            if update_action == "lo":
                dcmodifier[sy] = [
                    symbol_instance,
                    UpdateAction.Lower,
                    mi.sync_db.add_parameter(
                        raw_symb + "_Lower", dim, txt + " MODIFIER Lower"
                    ),
                ]
            elif update_action == "up":
                dcmodifier[sy] = [
                    symbol_instance,
                    UpdateAction.Upper,
                    mi.sync_db.add_parameter(
                        raw_symb + "_Upper", dim, txt + " MODIFIER Upper"
                    ),
                ]
            elif update_action == "fx":
                dcmodifier[sy] = [
                    symbol_instance,
                    UpdateAction.Fixed,
                    mi.sync_db.add_parameter(
                        raw_symb + "_Fixed", dim, txt + " MODIFIER Fixed"
                    ),
                ]
            else:
                raise Exception(f'Update_action "{update_action}" for {sy} not valid')
        elif info["type"] == "equation":
            raise Exception("To modify equations is not implemented yet")

    mi.instantiate(
        f"{MODEL} using {MODEL_prob} {MODEL_sense} {MODEL_obj}",
        modifiers=[GamsModifier(*m) for m in dcmodifier.values()],
        options=opt,
    )
    while True:
        queue_lock.acquire()
        if queue.empty():
            queue_lock.release()
            return None
        idx, dc = queue.get()
        queue_lock.release()

        dcmodifier = clearModifiers(dcmodifier, maingdx, gams_dir=gams_dir)
        dcmodifier = setSymbolsValues(dcmodifier, dc, maingdx, gams_dir=gams_dir)

        tmp["run_orig"] = idx
        tmp["id"] = (
            "Run_"
            + str(base["tmp"][block]["runs"]["run_nr"][idx]).zfill(4)
            + "_"
            + base["unique"]
            + base["tmp"][block]["str_block"]
            + "_r"
            + str(idx).zfill(4)
        )
        # tmp['id'] = base['unique'] + base['tmp'][block]['str_block'] + '_r' + str(idx).zfill(3)
        tmp["block"] = block
        tmp["id_dir"] = os.path.join(tmp["RESULTS_DIR_ABS"], tmp["id"])
        tmp["stdout_file"] = os.path.join(tmp["id_dir"], tmp["id"] + "_gams_stdout.txt")
        tmp["tmp_gdx"] = os.path.join(tmp["id_dir"], tmp["id"] + "_tmp.gdx")
        tmp["job_lst"] = os.path.join(tmp["id_dir"], tmp["id"] + "_job.lst")
        tmp["checkpoint_lst"] = os.path.join(tmp["id_dir"], tmp["id"] + "_CP.lst")
        tmp["checkpoint_gdx"] = os.path.join(tmp["id_dir"], tmp["id"] + "_CP.gdx")
        tmp["main_gdx"] = ""
        tmp["diff_gdx"] = os.path.join(tmp["id_dir"], tmp["id"] + "_diff.gdx")
        tmp["config_file"] = os.path.join(tmp["id_dir"], tmp["id"] + "_config.yml")
        os.makedirs(tmp["id_dir"], exist_ok=True)
        start_t = time.time()
        with OutputStream(tee=False, logfile=tmp["stdout_file"]) as output_stream:
            mi.solve(output=output_stream, mi_opt=mi_opt)

        solver_msg = get_solver_status(tmp["stdout_file"])
        tmp["solver_msg"] = solver_msg

        symbs_dict = base["tmp"][block]["runs"]["par_var"][idx]
        countries = base["tmp"][block]["used_countries"]
        # lines = base['tmp'][block]['used_lines']
        constraints = base["tmp"][block]["used_constraints"]
        data_scen = base["tmp"][block]["used_data"]

        tmp["modelstatus"] = mi.model_status
        tmp["solverstatus"] = mi.solver_status
        tmp["system_costs"] = mi.sync_db.get_variable("Z")[()].level
        # tmp['summary'] = countries + '_' + lines + '_' + constraints + '_' + data_scen + '_' + \
        tmp["summary"] = (
            countries
            + "_"
            + constraints
            + "_"
            + data_scen
            + "_"
            + "_".join([k + "_" + str(v) for k, v in symbs_dict.items()])
        )
        tmp["summary_file"] = os.path.join(
            tmp["RESULTS_DIR_ABS"],
            tmp["id"]
            + "_"
            + str(tmp["modelstatus"])
            + "_"
            + str(round(tmp["system_costs"] / 1000000, 1))
            + "_"
            + tmp["summary"]
            + ".txt",
        )
        tmp["config"] = {
            k: v
            for k, v in base["tmp"][block]["runs"].items()
            if k not in ["par_var", "run_nr"]
        }
        # if 'country_set' in list(tmp['config'].keys()):
        #     tmp['config']['lines'] = lines
        tmp["config"].update({k: v for k, v in symbs_dict.items()})
        tmp["config"].update({"solver_msg": solver_msg, "long_id": tmp["id"], "run":base["tmp"][block]["runs"]["run_nr"][idx]})
        tmp["guss_tool"] = base["guss_tool"]
        tmp["guss_config"] = dc
        tmp["SETTINGS_DIR_ABS"] = base["SETTINGS_DIR_ABS"]
        tmp["reporting_symbols_file"] = os.path.join(
            base["SETTINGS_DIR_ABS"], "reporting_symbols.csv"
        )
        tmp["csv_dir"] = os.path.join(tmp["id_dir"], "csv")

        with open(tmp["config_file"], "w") as yml:
            yaml.dump(tmp, yml)  # yaml.dump(tmp['config'], yml)

        # with open(tmp['summary_file'], 'w') as txt:
        #     txt.write(tmp['summary'])

        copyfile(maingdx, tmp["checkpoint_gdx"])

        copyfile(os.path.join(cp_working_dir, job_name + ".lst"), tmp["checkpoint_lst"])
        # copyfile(os.path.join(ws.working_directory, job_name + ".lst"), tmp["job_lst"])

        mi.sync_db.export(tmp["tmp_gdx"])
        result.append(tmp)
        gc.collect()

        end_t = time.time()
        print_lock.acquire()
        print("-------------------------------------------------------------")
        print("Run: %s" % idx)
        print("-------------------------------------------------------------")
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("Run id:", tmp["id"])
        print("Run config:", tmp["config"])
        print("Model status:", tmp["modelstatus"])
        print("Solver status:", tmp["solverstatus"])
        print("Total system costs:", tmp["system_costs"])
        print("")
        print("Elapsed time:", end_t - start_t, "sec")
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("")
        print_lock.release()


def guss_solve(queue, symbs, base, block):

    convar_dc = base['convar_dc']
    if 'model_name' in convar_dc:
        MODEL = convar_dc['model_name']
        MODEL_sense = convar_dc['model_sense']
        MODEL_prob = convar_dc['model_problem']
        MODEL_obj = convar_dc['model_objective']
        MODEL_solver = convar_dc['model_solver']
    else:
        MODEL = 'DIETER'
        MODEL_sense = 'min'
        MODEL_prob = 'lp'
        MODEL_obj = 'Z'
        MODEL_solver = ''

    gams_dir = convar_dc['gams_dir']

    RUN_DIR_ABS = base["RUN_DIR_ABS"]

    cp_file = base["tmp"][block]["cp_file"]
    maingdx = base["tmp"][block]["main_gdx_file"]
    cp_working_dir = base["tmp"][block]["cp_working_dir"]
    job_name = base["tmp"][block]["job_name"]

    tmp_path = base["TMP_DIR_ABS"]
    rnd = secrets.token_hex(8)
    tmp_path_unique = os.path.join(tmp_path, rnd)
    os.makedirs(tmp_path_unique, exist_ok=True)

    ws = GamsWorkspace(
        system_directory=gams_dir,
        # debug=DebugLevel.KeepFiles, 
        working_directory=tmp_path_unique
    )
    print("working_directory:", ws.working_directory)
    cp = ws.add_checkpoint(cp_file)
    opt = GamsOptions(ws)
    opt.optdir = RUN_DIR_ABS
    opt.solvelink = 0
    if not MODEL_solver:
        solver = "cplex"
    else:
        solver = MODEL_solver

    opt.all_model_types = solver
    opt.optfile = 1
    copyfile(
        os.path.join(RUN_DIR_ABS, f"{solver}.opt"),
        os.path.join(ws.working_directory, f"{solver}.opt"),
    )
    mi = cp.add_modelinstance()
    mi_opt = GamsModelInstanceOpt(
        solver=solver, opt_file=1, no_match_limit=999999999, debug=True
    )

    dcmodifier = {}
    for (
        sy
    ) in (
        symbs
    ):  # identify the symbols with different type and set modifier for each symbols
        if "." in sy:
            raw_symb = sy.split(".")[0]
            update_action = sy.split(".")[1].lower()
        else:
            raw_symb = sy
        _, info = gdx_get_symb_info(gams_dir=gams_dir, filename=maingdx, symbol=raw_symb)
        dim = info["nrdims"]
        txt = info["desc"]
        if info["type"] == "parameter":
            # print('raw:', raw_symb, 'sy:', sy)
            symbol_instance = mi.sync_db.add_parameter(sy, dim, txt)
            dcmodifier[sy] = [symbol_instance]
        elif info["type"] == "variable":
            # check if that variable has already been added.
            try:
                symbol_instance = mi.sync_db.get_variable(raw_symb)
            except GamsException as e:
                # print(f"{e}")
                symbol_instance = mi.sync_db.add_variable(
                    raw_symb, dim, VarType.Positive
                )
            # add to mi.sync_db
            if update_action == "lo":
                dcmodifier[sy] = [
                    symbol_instance,
                    UpdateAction.Lower,
                    mi.sync_db.add_parameter(
                        raw_symb + "_Lower", dim, txt + " MODIFIER Lower"
                    ),
                ]
            elif update_action == "up":
                dcmodifier[sy] = [
                    symbol_instance,
                    UpdateAction.Upper,
                    mi.sync_db.add_parameter(
                        raw_symb + "_Upper", dim, txt + " MODIFIER Upper"
                    ),
                ]
            elif update_action == "fx":
                dcmodifier[sy] = [
                    symbol_instance,
                    UpdateAction.Fixed,
                    mi.sync_db.add_parameter(
                        raw_symb + "_Fixed", dim, txt + " MODIFIER Fixed"
                    ),
                ]
            else:
                raise Exception(f'Update_action "{update_action}" for {sy} not valid')
        elif info["type"] == "equation":
            raise Exception("To modify equations is not implemented yet")

    mi.instantiate(
        f"{MODEL} using {MODEL_prob} {MODEL_sense} {MODEL_obj}",
        modifiers=[GamsModifier(*m) for m in dcmodifier.values()],
        options=opt,
    )
    results = []
    for idx, dc in queue.items():

        dcmodifier = clearModifiers(dcmodifier, maingdx,gams_dir=gams_dir)
        dcmodifier = setSymbolsValues(dcmodifier, dc, maingdx,gams_dir=gams_dir)

        tmp = {}
        tmp["TMP_PATH"] = tmp_path_unique
        tmp["BASE_DIR_ABS"] = base["BASE_DIR_ABS"]
        tmp["RUN_DIR_ABS"] = base["RUN_DIR_ABS"]
        tmp["RESULTS_DIR_ABS"] = base["RESULTS_DIR_ABS"]
        tmp["run_orig"] = idx
        tmp["id"] = (
            "Run_"
            + str(base["tmp"][block]["runs"]["run_nr"][idx]).zfill(4)
            + "_"
            + base["unique"]
            + base["tmp"][block]["str_block"]
            + "_r"
            + str(idx).zfill(4)
        )
        # tmp['id'] = base['unique'] + base['tmp'][block]['str_block'] + '_r' + str(idx).zfill(3)
        tmp["block"] = block
        tmp["id_dir"] = os.path.join(tmp["RESULTS_DIR_ABS"], tmp["id"])
        tmp["stdout_file"] = os.path.join(tmp["id_dir"], tmp["id"] + "_gams_stdout.txt")
        tmp["tmp_gdx"] = os.path.join(tmp["id_dir"], tmp["id"] + "_tmp.gdx")
        tmp["job_lst"] = os.path.join(tmp["id_dir"], tmp["id"] + "_job.lst")
        tmp["checkpoint_lst"] = os.path.join(tmp["id_dir"], tmp["id"] + "_CP.lst")
        tmp["checkpoint_gdx"] = os.path.join(tmp["id_dir"], tmp["id"] + "_CP.gdx")
        tmp["main_gdx"] = ""
        tmp["diff_gdx"] = os.path.join(tmp["id_dir"], tmp["id"] + "_diff.gdx")
        tmp["config_file"] = os.path.join(tmp["id_dir"], tmp["id"] + "_config.yml")
        os.makedirs(tmp["id_dir"], exist_ok=True)
        start_t = time.time()
        with OutputStream(tee=False, logfile=tmp["stdout_file"]) as output_stream:
            mi.solve(output=output_stream, mi_opt=mi_opt)

        solver_msg = get_solver_status(tmp["stdout_file"])
        tmp["solver_msg"] = solver_msg

        symbs_dict = base["tmp"][block]["runs"]["par_var"][idx]
        countries = base["tmp"][block]["used_countries"]
        # lines = base['tmp'][block]['used_lines']
        constraints = base["tmp"][block]["used_constraints"]
        data_scen = base["tmp"][block]["used_data"]

        tmp["modelstatus"] = mi.model_status
        tmp["solverstatus"] = mi.solver_status
        tmp["system_costs"] = mi.sync_db.get_variable("Z")[()].level
        # tmp['summary'] = countries + '_' + lines + '_' + constraints + '_' + data_scen + '_' + \
        tmp["summary"] = (
            countries
            + "_"
            + constraints
            + "_"
            + data_scen
            + "_"
            + "_".join([k + "_" + str(v) for k, v in symbs_dict.items()])
        )
        tmp["summary_file"] = os.path.join(
            tmp["RESULTS_DIR_ABS"],
            tmp["id"]
            + "_"
            + str(tmp["modelstatus"])
            + "_"
            + str(round(tmp["system_costs"] / 1000000, 1))
            + "_"
            + tmp["summary"]
            + ".txt",
        )
        tmp["config"] = {
            k: v
            for k, v in base["tmp"][block]["runs"].items()
            if k not in ["par_var", "run_nr"]
        }
        # if 'country_set' in list(tmp['config'].keys()):
        #     tmp['config']['lines'] = lines
        tmp["config"].update({k: v for k, v in symbs_dict.items()})
        tmp["config"].update({"solver_msg": solver_msg, "long_id": tmp["id"], "run":base["tmp"][block]["runs"]["run_nr"][idx]})
        tmp["guss_tool"] = base["guss_tool"]
        tmp["guss_config"] = dc
        tmp["SETTINGS_DIR_ABS"] = base["SETTINGS_DIR_ABS"]
        tmp["reporting_symbols_file"] = os.path.join(
            base["SETTINGS_DIR_ABS"], "reporting_symbols.csv"
        )
        tmp["csv_dir"] = os.path.join(tmp["id_dir"], "csv")

        with open(tmp["config_file"], "w") as yml:
            yaml.dump(tmp, yml)  # yaml.dump(tmp['config'], yml)

        # with open(tmp['summary_file'], 'w') as txt:
        #     txt.write(tmp['summary'])

        copyfile(maingdx, tmp["checkpoint_gdx"])

        copyfile(os.path.join(cp_working_dir, job_name + ".lst"), tmp["checkpoint_lst"])
        # copyfile(os.path.join(ws.working_directory, job_name + ".lst"), tmp["job_lst"])

        mi.sync_db.export(tmp["tmp_gdx"])
        results.append(tmp)
        gc.collect()

        end_t = time.time()
        print("-------------------------------------------------------------")
        print("Run: %s" % idx)
        print("-------------------------------------------------------------")
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("Run id:", tmp["id"])
        print("Run config:", tmp["config"])
        print("Model status:", tmp["modelstatus"])
        print("Solver status:", tmp["solverstatus"])
        print("Total system costs:", tmp["system_costs"])
        print("")
        print("Elapsed time:", end_t - start_t, "sec")
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("")
    return results
