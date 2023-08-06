import csv
import os
import time
from gams import GamsWorkspace, GamsOptions, DebugLevel
from .gdx_handler import gdx_get_set_coords


def gams_parameter_script(name: str = 'power', index: dict = {1:'n',2:'tech'}, useHeader: bool = True) -> str:
    """
    This script is a raw gams code. It calls csv2gdx gams application, available for linux and windows.

    Arguments:
        name {str} -- Name of the symbol.
        index {dict} -- Dictionary of the index.
        useHeader {bool} -- If True, the first row of the CSV file is used as header.

    Returns:
        str -- gams script.

    Examples:
        csv  >> n,tech,value
                DE,pv,1
                FR,wind,2
                US,coal,3
    """
    string_of_sets = ''
    for k,v in index.items():
        string_of_sets += f'Set {v};\n'
    
    srting_of_index = f'''"({','.join([str(i) for i in index.keys()])})"'''
    index_of_value_col = str(max(index.keys()) + 1)

    if useHeader:
        option = 'y'
    else:
        option = 'n'

    string_of_load_sets = ''
    for k,v in index.items():
        string_of_load_sets += f'$load {v} = Dim{str(k)}\n'

    str_indexes = f'''{','.join(index.values())}'''
    gams_symbol_str = f'{name}({str_indexes})'

    return (f"""
{string_of_sets}
$call csv2gdx "%csv_path%" output = "%gdxfile%" id={name} index={srting_of_index} values={index_of_value_col} useHeader={option}
$ifE errorLevel<>0 $abort Problems reading file
$gdxIn %gdxfile%
{string_of_load_sets}

Parameter {gams_symbol_str};
$load {name}
$gdxIn
execute_unload '%gdxfile%';
""", gams_symbol_str)

def gams_csv2gdx_parameters(symbol_name: str = None, gams_dir: str = None, working_directory: str = None, csv_path: str = None, useHeader: bool = True, gdx_dir: str = None) -> tuple([str, str, dict, str]):
    """ Creates a GDX file from CSV. The file converted is named after the symbol name.

    Arguments:
        symbol_name {str} -- Name of the symbol.
        gams_dir {str} -- Path to the GAMS installation directory.
        working_directory {str} -- Path to the working directory.
        csv_path {str} -- Path to the CSV file.
        useHeader {bool} -- If True, the first row of the CSV file is used as header.
        gdx_dir {str} -- Path to the GDX directory.

    Returns:
        tuple -- (symbol name, gams_symbol_str, index, gdx_file_path)

    """
    if gdx_dir is None:
        gdxfilename = os.path.join(os.getcwd(), f'{symbol_name}.gdx')
    else:
        gdxfilename = os.path.join(gdx_dir, f'{symbol_name}.gdx')
    
    with open(csv_path) as csvFile:
        reader = csv.reader(csvFile)
        header_names_list = next(reader)

    index = {}
    for i, header in enumerate(header_names_list,1):
        if i < len(header_names_list):
            index[i] = header
    
    ws = GamsWorkspace(system_directory=gams_dir,working_directory=working_directory,debug=DebugLevel.KeepFiles)
    script, gams_symbol_str = gams_parameter_script(name=symbol_name, index=index, useHeader=useHeader)
    jobs = ws.add_job_from_string(script)
    opt = GamsOptions(ws)
    opt.defines["csv_path"] = f'"{csv_path}"'
    opt.defines["gdxfile"] = f'"{gdxfilename}"'
    jobs.run(gams_options=opt)
    return (symbol_name, gams_symbol_str, index, gdxfilename)


def gams_join_gdx_script(gdx_info_list: list = None, gams_dir=None) -> str:
    """ Creates a GAMS script to join GDX files."""

    index_union = set()
    parameters = []
    gdx_path = []
    names = []
    sets_elements = {}

    for symbol_name, gams_symbol_str, index, gdx_file_path in gdx_info_list:
        index_union = index_union.union(set(index.values()))
        parameters.append(gams_symbol_str)
        gdx_path.append(gdx_file_path)
        names.append(symbol_name)
        for k,v in index.items():
            if v not in sets_elements.keys():
                sets_elements[v] = []
            sets_elements[v].append(gdx_get_set_coords(gams_dir=gams_dir, filename=gdx_file_path, setname=v))
    
    elements_union = {}
    for k,v in sets_elements.items():
        elements_union[k] = set()
        for i in v:
            elements_union[k] = elements_union[k].union(i)
    
    for k,v in elements_union.items():
        elements_union[k] = sorted(list(v))

    string_of_sets = ''
    for k,v in elements_union.items():
        string_of_sets += f'Set {k} / {",".join(v)} /;\n'

    string_parameters = ''
    for parameter in parameters:
        string_parameters += f'Parameter {parameter};\n'

    string_load_gdxs = ''
    for gdx_file_path, name in zip(gdx_path,names):
        string_load_gdxs += f'$gdxIn {gdx_file_path}\n$load {name}\n'
    
    string_unload_output_gdx = f"$gdxIn\nexecute_unload '%gdxfile%';"

    script = f"""

{string_of_sets}

{string_parameters}

{string_load_gdxs}

{string_unload_output_gdx}

"""
    return script


def join_gdx_files(gdx_info_list: list = None, output_gdx_file_path: str = None, gams_dir: str = None, working_directory: str = None) -> str:
    """ Joins GDX files.

    Arguments:
        gdx_info_list {list} -- List of tuples (symbol name, gams_symbol_str, index, gdx_file_path)
        output_gdx_file_path {str} -- Path to the output GDX file.
        gams_dir {str} -- Path to the GAMS installation directory.
        working_directory {str} -- Path to the working directory.

    Returns:
        str -- Path to the output GDX file.

    """
    ws = GamsWorkspace(system_directory=gams_dir,working_directory=working_directory,debug=DebugLevel.KeepFiles)
    script = gams_join_gdx_script(gdx_info_list)
    jobs = ws.add_job_from_string(script)
    opt = GamsOptions(ws)
    opt.defines["gdxfile"] = f'"{output_gdx_file_path}"'
    jobs.run(gams_options=opt)
    return output_gdx_file_path

def gams_feat_node(
    gams_dir: str = None, csv_path: str = None, gdxoutputfolder: str = None
) -> str:
    """ Creates a GDX file from CSV. The file converted is 

    Args:
        gams_dir (str, optional): directory where gams.exe is located. Defaults to None.
        csv_path (str, optional): absolute path of the csv file. Defaults to None. Hint: The name of the file must fit the symbol name.
        gdxoutputfolder (str, optional): absolute path of the directory, without a "/" at the end. The name of the output file will be the same as the symbol with .gdx extension. Defaults to None.

    Returns:
        str: path of the new GDX file
    """

    def gams_script():
        """
        This script is a raw gams code. It calls csv2gdx gams application, available for linux and windows.
        """
        return """
Set
features
n;

$call csv2gdx "%csv_path%" output = "%gdxfile%" id=feat_node index=1 values=%range% useHeader=y
$ifE errorLevel<>0 $abort Problems reading csv file
$gdxIn %gdxfile%
$load features = dim1
$load n = dim2

Parameter feat_node(features,n);
$load feat_node
$gdxIn
execute_unload '%gdxfile%';
"""

    start = time.time()
    # reading first row of csv file to get columns number
    with open(csv_path) as csvFile:
        reader = csv.reader(csvFile)
        header_names_list = next(reader)
    header_len = len(header_names_list)
    strrng = ",".join(
        str(i) for i in range(2, header_len + 1)
    )  # passing to gams a range of columns omiting first column. First value is 1 in gams
    #  verify linux or windows
    if os.name == "posix":
        rng = strrng
    elif os.name == "nt":
        rng = f"({strrng})"
    os.makedirs(gdxoutputfolder, exist_ok=True)  # create folder if it does not exist.
    symbname = os.path.basename(csv_path).split(".")[0]
    gdxfilename = os.path.join(gdxoutputfolder, symbname + ".gdx")
    ws = GamsWorkspace(system_directory=gams_dir,debug=DebugLevel.KeepFiles)
    jobs = ws.add_job_from_string(gams_script())
    opt = GamsOptions(ws)
    opt.defines["csv_path"] = f'"{csv_path}"'
    opt.defines["gdxfile"] = f'"{gdxfilename}"'
    opt.defines["range"] = f'"{rng}"'
    jobs.run(gams_options=opt)
    # print(f'{csv_path} -> {gdxfilename}: Elapsed time {round(time.time() - start, 3)} sec.')
    return gdxfilename

