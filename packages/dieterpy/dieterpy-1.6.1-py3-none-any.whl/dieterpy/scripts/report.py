# DIETERpy is electricity market model developed by the research group
# Transformation of the Energy Economy at DIW Berlin (German Institute of Economic Research)
# copyright 2021, Carlos Gaete-Morales, Martin Kittel, Alexander Roth,
# Wolf-Peter Schill, Alexander Zerrahn
"""

"""
import sys
import re
import glob
import os
import copy
import time
import operator
import gzip
import mgzip
import pickle
import numpy as np
import pandas as pd
import ntpath
import itertools
from typing import Union

from multiprocessing import Lock, Process, Queue, Manager, cpu_count
from ..config import settings

from loguru import logger

logger.remove(0)
fmt = "{time} - {name} - {level} - {message}"
logger.add("dieterpy.log", level="DEBUG", format="{time} - {name}:{function}:{line} - {level} - {message}")
logger.add(sys.stdout, level="SUCCESS", format="{message}")



def parallel_func(dc, queue=None, queue_lock=None, function=None, kargs={}):
    while True:
        queue_lock.acquire()
        if queue.empty():
            queue_lock.release()
            return None
        key, item = queue.get()
        queue_lock.release()
        obj = function(item, **kargs)
        dc[key] = obj
    return None


def parallelize(function=None, inputdict=None, nr_workers=1, **kargs):
    """
    input is a dictionary that contains numbered keys and as value any object
    the queue contains tuples of keys and objects, the function must be consistent when getting data from queue
    """
    with Manager() as manager:
        dc = manager.dict()
        queue = Queue()
        for key, item in inputdict.items():
            queue.put((key, item))
        queue_lock = Lock()
        processes = {}
        for i in range(nr_workers):
            if kargs:
                processes[i] = Process(
                    target=parallel_func, args=(dc, queue, queue_lock, function, kargs,)
                )
            else:
                processes[i] = Process(
                    target=parallel_func, args=(dc, queue, queue_lock, function,)
                )
            processes[i].start()
        for i in range(nr_workers):
            processes[i].join()
        outputdict = dict(dc)
    return outputdict


def open_file(path):
    # use parallel proc to open file
    # with mgzip.open(path, thread=cpu_count()) as pk:
    with gzip.open(path) as pk:
        dc = pickle.load(pk)
    return dc


class CollectScenariosPerSymbol:
    def __init__(self, paths=None, rng=None, cores = 0):
        self.paths = paths
        self.rng = rng
        self.cores = cores
        self.fixed = ["scenario", "loop", "scen_desc", "path", "reporting_symbols"]
        if rng is None and paths is None:
            self.pkls = glob.glob(os.path.join(settings.RESULTS_DIR_ABS,"*/*.pkl.gz"))
        elif paths is None:
            self.pkls = glob.glob(os.path.join(settings.RESULTS_DIR_ABS,"*/*.pkl.gz"))[rng[0] : rng[1]]
        elif rng is None:
            self.pkls = paths
        else:
            raise Exception("paths and rng can not be provided simultaneously")
        self.config = []
        inpdc = {}
        for i, v in enumerate(self.pkls):
            inpdc[i] = v
        if self.cores == 0:
            nr_workers = min(len(inpdc), cpu_count())
        else:
            nr_workers = min(len(inpdc), self.cores)

        outpdc = parallelize(function=self.from_pkl_remove_df, inputdict=inpdc, nr_workers = nr_workers)
        for ix in sorted(list(outpdc.keys())):
            self.config.append(outpdc[ix])

        self.convertiontable = {
            "v": "Val",
            "m": "Marginal",
            "up": "Upper",
            "lo": "Lower",
        }

    def __repr__(self):
        return f'''CollectScenariosPerSymbol(paths={self.paths}, rng={self.rng}, cores={self.cores})'''

    def from_pkl_remove_df(self, path):

        ## use parallel proc to open file
        # with mgzip.open(path, thread=cpu_count()) as pk:

        with gzip.open(path) as pk:
            dc = pickle.load(pk)
        dc_keys = list(dc.keys())
        for key in dc_keys:
            if key not in self.fixed:
                dc[key].pop("data")
                dc["path"] = path
        return dc

    def scen_load(self, path, symbol):

        # with mgzip.open(path, thread=cpu_count()) as pk:
        with gzip.open(path) as pk:
            dc = pickle.load(pk)
            symbdc = dc[symbol]
        return symbdc

    def collectinfo(self, symbols=[]):
        data = copy.deepcopy(self.config)
        if symbols:
            symblist = self.fixed + symbols
            for idx, scen in enumerate(self.config):
                for ky in scen.keys():
                    if ky not in symblist:
                        data[idx].pop(ky)

        self.data = data
        self.symbols = [sy for sy in self.showsymbols(self.data) if sy not in self.fixed]
        self.shortscennames = self.scenario_name_shortener(self.data)
        self.loopitems = self.get_loopitems(self.data)
        self.pathsbook = dict()
        logger.success("Collecting scenarios data finished")
        logger.success("Now choose a method of a CollectScenariosPerSymbol instance by doing \ne.g.  instance.join_scens_by_symbol(symbol, result_col, loopinclude, warningshow), or\n     instance.join_all_symbols(result_col, loopinclude, warningshow)")

    @staticmethod
    def ts(df):
        df["h"] = df.h.str.extract(r"(\d+)", expand=False).astype("int16")
        return df

    @staticmethod
    def showsymbols(data):
        ks = list()
        for sc in data:
            ks += list(sc.keys())
        return sorted(list(set(ks)))

    @staticmethod
    def scenario_name_shortener(data):
        flag = False
        pattern = re.compile(r"(\d+)", re.IGNORECASE)
        names = list()
        numbs = list()
        shortnames = dict()
        for scen in data:
            name = scen["scenario"]
            names.append(name)
            if pattern.search(name) != None:
                numbs.append(pattern.search(name)[0])
            else:
                flag = True
        names = sorted(names)
        if not flag:
            names_set = list(set(names))
            if len(names) == len(names_set):
                if len(names) == len(set(numbs)):
                    for name in names:
                        shortname = "S" + pattern.search(name)[0]
                        shortnames[name] = shortname
                        shortnames[shortname] = name
                else:
                    flag = True
            else:
                flag = True
        if flag:
            logger.info(f"New short names for scenarios. To know the corresponding scenario names type obj.shortscennames")
            for n, name in enumerate(names):
                shortname = "S" + str(n).zfill(4)
                shortnames[name] = shortname
                shortnames[shortname] = name
        return shortnames

    @staticmethod
    def get_loopitems(data):
        loopkeys = list()
        for scen in data:
            loopkeys += list(scen["loop"].keys())
        loopset = list(set(loopkeys))
        loopitems = dict()
        for loop in loopset:
            vals = list()
            for scen in data:
                if loop in scen["loop"].keys():
                    val = type(scen["loop"][loop]).__name__
                    if "int" in val:
                        if "int" == val:  # if numpy.int64 then val should be int64
                            int_py = scen["loop"][loop]
                        else:
                            int_py = scen["loop"][loop].item()  # any numpy int to native int
                        bit = int_py.bit_length()
                        if bit < 16:
                            val = val + "16"
                        elif bit < 32:
                            val = val + "32"
                        else:
                            val = val + "64"
                    elif "float" in val:
                        val = val + "16"
                    elif val == "str":
                        val = "category"
                    elif val == "NoneType":
                        pass
                    else:
                        raise Exception(
                            f"the iteration values in scenario {scen['scenario']} for the symbol '{loop}' is {scen['loop']}, not recognized as int,float or str"
                        )
                    vals.append(val)
            typ = sorted(list(set(vals)))[-1]  # the higest bit for all values
            loopitems[loop] = typ
        return loopitems

    @staticmethod
    def get_modifiers(scen, loopitems):
        loops = dict()
        for key, value in loopitems.items():
            if key in scen["loop"].keys():
                loops[key] = scen["loop"][key]
            else:
                if value == "category":
                    loops[key] = "NaN"
                elif "int" in value:
                    loops[key] = np.nan
                elif "float" in value:
                    loops[key] = np.nan
                else:
                    raise Exception("loop must contain int, float or string")
        return loops

    @staticmethod
    def add_scencols(
        scen, symbol, symbscen, shortscennames, loopitems, val_col, loopinclude
    ):
        df = symbscen["data"]
        scenname = scen["scenario"]
        shortn = shortscennames[scenname]
        dims = scen[symbol]["dims"]
        # write into df
        df["symbol"] = symbol
        df["id"] = shortn

        if loopinclude:
            loops = self.get_modifiers(scen, loopitems)
            for k in loopitems.keys():
                df[k] = loops[k]
            return df[["id", *list(loopitems.keys()), "symbol", *dims, val_col]].copy()
        else:
            return df[["id", "symbol", *dims, val_col]].copy()

    def concatenation(self, symbol, flag, loopinclude, result_col, symblist):
        savefile = False

        symbdict = self.data[flag][symbol]

        if loopinclude:
            if len(symblist) > 1:
                savefile = True
                symbdict[result_col] = (
                    pd.concat(symblist)
                    .astype({k: typ for k, typ in self.loopitems.items()})
                    .astype(
                        {
                            k: "int16" if k == "h" else "category"
                            for k in symbdict["dims"]
                        }
                    )
                    .astype({k: "category" for k in ["id", "symbol"]})
                )
            elif len(symblist) == 1:
                savefile = True
                symbdict[result_col] = (
                    symblist[0]
                    .astype({k: typ for k, typ in self.loopitems.items()})
                    .astype(
                        {
                            k: "int16" if k == "h" else "category"
                            for k in symbdict["dims"]
                        }
                    )
                    .astype({k: "category" for k in ["id", "symbol"]})
                )
            else:
                logger.info(f"   {symbol} does not have data in any scenarios provided [{self}]")
        else:
            if len(symblist) > 1:
                savefile = True
                symbdict[result_col] = (
                    pd.concat(symblist)
                    .astype(
                        {
                            k: "int16" if k == "h" else "category"
                            for k in symbdict["dims"]
                        }
                    )
                    .astype({k: "category" for k in ["id", "symbol"]})
                )
            elif len(symblist) == 1:
                savefile = True
                symbdict[result_col] = (
                    symblist[0]
                    .astype(
                        {
                            k: "int16" if k == "h" else "category"
                            for k in symbdict["dims"]
                        }
                    )
                    .astype({k: "category" for k in ["id", "symbol"]})
                )
            else:
                logger.info(f"   {symbol} does not have data in any scenarios provided [{self}]")

        # queue.put((symbdict, savefile))
        return (symbdict, savefile)

    def symbol_dataframe_ready(self, scen, scenload_file_func, add_scencols_func, ts_func, shortscennames, loopitems, loopinclude, val_col, symbol):
        symb_scendict = scenload_file_func(scen["path"], symbol)
        dframe = add_scencols_func(
            scen,
            symbol,
            symb_scendict,
            shortscennames,
            loopitems,
            val_col,
            loopinclude,
        )
        if "h" in scen[symbol]["dims"]:
            dframe = ts_func(dframe)
        return dframe

    def join_scens_by_symbol(
        self, symbol, result_col="v", loopinclude=False, warningshow=True,
    ):
        """
        result_col: marginal or val
        self.data
        symbol
        """
        tmi = time.time()
        logger.success(f"{symbol}.{result_col} --> Starting...")
        logger.success(f"   Loading pkl files of scenario data")
        if result_col in self.convertiontable.keys():
            val_col = self.convertiontable[result_col]
        else:
            raise Exception(
                f"result_col is {result_col}, it must be one of the following: {list(self.convertiontable.keys())}"
            )
        sceninfo_dict = dict()
        for indx, scen in enumerate(self.data):
            if symbol in scen.keys():
                sceninfo_dict[indx] = scen
        outputdict = {}
        for idx, scenario in sceninfo_dict.items():

            symbdf = self.symbol_dataframe_ready(scen = scenario,
                                    scenload_file_func = self.scen_load,
                                    add_scencols_func = self.add_scencols,
                                    ts_func = self.ts,
                                    shortscennames = self.shortscennames,
                                    loopitems = self.loopitems,
                                    loopinclude = loopinclude,
                                    val_col = val_col,
                                    symbol = symbol)
            outputdict[idx] = symbdf

        symblist = [v for v in outputdict.values()]

        flag = -1
        modifiers = dict()
        for ix, scen in enumerate(self.data):
            if symbol in scen.keys():
                modifiers[self.shortscennames[scen["scenario"]]] = self.get_modifiers(
                    scen, self.loopitems
                )
                flag = ix
            else:
                logger.info(f'   Symbol "{symbol}" is not in {scen["scenario"]} [{self}]')
        tmm = time.time()
        logger.success(f"   Starting concatenation of dataframes. (Loading time {round(tmm-tmi)} s)")

        if flag > -1:
            symbdict, savefile = self.concatenation(symbol, flag, loopinclude, result_col, symblist)
            symbdict["scen"] = self.shortscennames
            symbdict["loop"] = list(self.loopitems.keys())
            symbdict["modifiers"] = modifiers

        else:
            savefile = False
            logger.info(f'Symbol "{symbol}" does not exist in any scenario [{self}]')

        if savefile:
            dest_dir = settings.REPORT_DIR_ABS
            dest_path = os.path.join(dest_dir, symbol + "." + result_col + ".pkl.gz")

            if symbol not in self.pathsbook.keys():
                self.pathsbook[symbol] = {}
            self.pathsbook[symbol][result_col] = dest_path
            tmc = time.time()
            logger.success(f"   Saving file... (Concat time {round(tmc-tmm)} s)")
            self.to_pickle(dest_path, symbdict)
            logger.success(f"   Final file size {round(os.path.getsize(dest_path)/10**6, 2)} mb. Saving time {round(time.time() - tmc)} s")
        logger.success("")

        if warningshow:
            logger.success(
                'In a new python script or notebook you can access the data with this snippet: \n   from dieterpy import SymbolsHandler, Symbol \n   SH = SymbolsHandler("folder") \n   Z = Symbol(name="Z", value_type="v", symbol_handler=SH) \n   Z.df  # <- Pandas DataFrame'
            )
        return None

    def join_all_symbols(self, result_col, loopinclude=False, warningshow=True):
        for symb in self.symbols:
            self.join_scens_by_symbol(symb, result_col, loopinclude, False)
        if warningshow:
            logger.success('In a new python script or notebook you can access the data with this snippet: \n   from dieterpy import SymbolsHandler, Symbol \n   SH = SymbolsHandler("folder") \n   Z = Symbol(name="Z", value_type="v", symbol_handler=SH) \n   Z.df  # <- Pandas DataFrame')
            
    def join_all_symbols_from_reporting(self, loopinclude=False, warningshow=True):

        symbol_df = pd.read_csv(os.path.join(settings.SETTINGS_DIR_ABS, "reporting_symbols.csv")) # open reporting_symbols.csv with pandas and refer it to the list updated_symbols
        updated_symbols  = symbol_df.stack().dropna().tolist()

        for symb in self.symbols:
            for reported in updated_symbols:
                symbol_raw = reported.split('.')[0]
                if symb == symbol_raw:
                    if '.' in reported:
                        result_col_candidate = reported.split('.')[1]
                        if result_col_candidate.lower() in self.convertiontable.keys():
                            result_col = result_col_candidate.lower()
                        else:
                            result_col = 'v'
                            logger.info(f"   Warning: result_col is not valid: {result_col_candidate}. Valid options are: {list(self.convertiontable.keys())}, using 'v' instead [{self}]")
                    else:
                        result_col = 'v'  # when symbol in reporting does not have a '.' in it we assume it is a 'v'
                    self.join_scens_by_symbol(symb, result_col, loopinclude, False)
        # add compatibility with version 0.3.3 (con1a_bal.m)
        if 'con1a_bal.m' not in updated_symbols:
            if 'con1a_bal' in updated_symbols:
                self.join_scens_by_symbol('con1a_bal', 'm', loopinclude, False)
        # end compatibility code
        if warningshow:
            logger.success('In a new python script or notebook you can access the data with this snippet: \n   from dieterpy import SymbolsHandler, Symbol \n   SH = SymbolsHandler("folder") \n   Z = Symbol(name="Z", value_type="v", symbol_handler=SH) \n   Z.df  # <- Pandas DataFrame')

    def to_pickle(self, path, obj):
        pickleobj = pickle.dumps(obj, protocol=min(3, pickle.HIGHEST_PROTOCOL))
        if path.endswith(".pkl.gz"):
            folder = os.path.dirname(path)
            os.makedirs(folder, exist_ok=True)

            # use parallel proc to open file
            # define block size per cpu
            cpu_nr = max(cpu_count() - 1, 1)
            filesize = len(pickleobj)
            size_per_cpu = int(filesize/cpu_nr)
            if size_per_cpu > 3*10**6: # 3mb
                size_selected = 3*10**6
            elif size_per_cpu < 1*10**5: # 100kb
                size_selected = 1*10**5
            else:
                size_selected = size_per_cpu
            logger.success(f'   Uncompressed file {round(filesize/10**6, 2)} mb. Chunk {round(size_selected/10**3, 1)} kb.')

            # with gzip.open(path, "wb") as datei:
            with mgzip.open(path, "wb", thread=0, blocksize=size_selected) as datei:
                datei.write(pickleobj)
            logger.success(f"   File saved: {path}")
        else:
            logger.success(f'   File {path} not saved. It does not have ".pkl.gz" extension')


class SymbolsHandler:
    def __init__(self, method, inpt=None):
        self.method = method
        self.inpt = inpt
        self.custom_loop = ['run','custom_name']
        self.filelocacions = {}
        if method == "object":
            self.from_object(inpt)
        elif method == "folder":
            self.from_folder(inpt)
        else:
            raise Exception('A method mus be provided from either "object" or "folder"')
        self.symbol_list = []
        self.get_symbolnames()
        self.loop_list = []
        self.get_loopitems()

    def from_object(self, object):
        self.filelocacions = object.pathsbook

    def from_folder(self, folder_path=None):
        if folder_path is None:
            self.folder_path = settings.REPORT_DIR_ABS
        else:
            self.folder_path = folder_path

        files = glob.glob(os.path.join(self.folder_path, "*.pkl.gz"))
        for file in files:
            self.add_symbolfile(file)

    def get_symbolnames(self):
        for name in self.filelocacions.keys():
            self.symbol_list.append(name)

    def get_loopitems(self):
        looplist = []
        for name in self.symbol_list:
            for k, v in self.filelocacions[name].items():
                looplist = looplist + self.get_data(name, k)["loop"]
                break  # if this name has more than one valuetype 'v', 'm', 'up', 'lo' then takes only one, since it is about the same symbol.
        self.loop_list = list(set(looplist))

    def add_symbolfile(self, path):
        symbol, valuetype = ntpath.basename(path).rstrip(".pkl.gz").split(".")
        if symbol not in self.filelocacions.keys():
            self.filelocacions[symbol] = {}
        self.filelocacions[symbol][valuetype] = path

    def get_data(self, name, valuetype):
        return open_file(self.filelocacions[name][valuetype])
    

    def custom_items(self,action: str='add', item: str = 'run'):
        ''' Not finished
            action can be "add" or "rm" 
            item a string. it can be any option self.loop_list
            This updates a list that is used in Symbol class to display custom columns when typing Symbol.dfm
        '''
        if action == 'add':
            if item in self.custom_loop:
                logger.info(f"Item already in custom list [{self}]")
            else:
                self.custom_loop.append(item)
        elif action == 'rm':
            if item in self.custom_loop:
                self.custom_loop.remove(item)
            else:
                logger.info(f"Item does not exist in custom list [{self}]")
        else:
            logger.info(f"Make sure you choose 'add' or 'rm' [{self}]")
        self.custom_loop = list(set(self.custom_loop))
        logger.success(f"custom_loop = [{*self.custom_loop,}]")

    def __repr__(self):
        return f'''SymbolsHandler(method='{self.method}', inpt='{self.inpt}')'''


# utils
def argmax(l):
    def f(i):
        return l[i]
    return max(range(len(l)), key=f)


def argmin(l):
    def f(i):
        return l[i]
    return min(range(len(l)), key=f)


class Symbol(object):
    def __init__(
        self,
        name,
        value_type,
        unit=None,
        header_name=None,
        dims=None,
        symbol_type=None,
        index=["id"],
        symbol_handler=None,
    ):
        self.__dict__["_repo"] = {}
        self.exists_sh = True
        self.name = name
        self.value_type = value_type
        self.symbol_type = symbol_type
        self.dims = dims
        self.index = index + ["symbol"]  # must be a list
        self.preferred_index = index  # must be a list
        self.data = None  # represents df
        self.modifiers = None
        self.symbol_handler = symbol_handler
        self.extend_header = ""
        self.info = None

        self.check_handler()
        self.check_inputs()
        self._repo["conversion_table"] = {
            "v": "Val",
            "m": "Marginal",
            "up": "Upper",
            "lo": "Lower",
        }
        self.check_value_type()
        self.get_modifiers()

    def fill_data(self):
        temp = self.get("symbol_handler").get_data(self.get("name"), self.get("value_type"))
        self.symbol_type = temp["type"]
        self.dims = temp["dims"]
        self.index = ["id", "symbol"] + temp["loop"]
        self.info = temp["symb_desc"]
        del temp

    def check_handler(self):
        if isinstance(self.get("symbol_handler"), SymbolsHandler):
            self.exists_sh = True
            if self.get("name") in self.get("symbol_handler").symbol_list:
                self.fill_data()
            else:
                self.exists_sh = True
                raise Exception(f'''Name: '{self.get("name")}' not in symbol_handler.symbol_list''')
        else:
            self.exists_sh = False

    def check_inputs(self):
        if not self.get("exists_sh"):
            if (
                self.get("symbol_type") is None
                or self.get("dims") is None
                or self.get("index") is None
            ):
                raise Exception("To create a 'Symbol' instance without 'symbol_handler' argument, the following arguments must be provided: 'symbol_type' 'dims' 'index'.")

    def check_value_type(self):
        if self.get("value_type") in self._repo["conversion_table"]:
            pass
        else:
            raise Exception("value_type argument must be either 'v', 'm', 'lo', or 'up'")

    def check_index(self):
        if isinstance(self.get("preferred_index"), list):
            for index in self.get("preferred_index"):
                if not index in self.get("index"):
                    raise Exception(f"'{index}' in preferred_index does not exists in the symbols data (columns of dataframe)")
        else:
            raise Exception("preferred_index must be a list")

    def update_index(self, preferred_index):
        self.preferred_index = preferred_index

    # TODO: Add new index items, for example actual res_share per scenario
    def get_df(self):
        if self.get("exists_sh"):
            df = self.get("symbol_handler").get_data(self.get("name"), self.get("value_type"))[self.get("value_type")]
            df = df.drop(df.columns.difference(
                                                self.get("preferred_index")
                                                + ["symbol"]
                                                + self.get("dims")
                                                + [self._repo["conversion_table"][self.get("value_type")]]
                                            ),
                        axis=1,
                        )
            df = df.rename(columns={self._repo["conversion_table"][self.get("value_type")]: "value"})
            return df.reset_index(drop=True)
        else:
            if self.get("data") is None:
                raise Exception("No dataframe has been provided")
            return self.get("data")

    def set_df(self, df):
        if not self.get("exists_sh"):
            self.data = df

    def get_modifiers(self):
        if self.get("exists_sh"):
            loops = self.get("symbol_handler").get_data(self.get("name"), self.get("value_type"))["modifiers"]
            dc = {}
            for k, v in loops.items():
                dc[k] = {}
                for key, value in v.items():
                    dc[k][key] = value
            self.modifiers = pd.DataFrame(dc).transpose().to_dict()

    @property
    def df(self):
        return self.get_df().copy()

    def get(self, name):
        if name == "df":
            return self.get_df().copy()
        else:
            return self._repo[name]

    @property
    def dfm(self):
        dfm = self.get_df().copy()
        for k, v in self.get("modifiers").items():
            dfm[k] = dfm["id"].map(v)
        return dfm

    @property
    def dfc(self):
        dfc = self.get_df().copy()
        for k, v in self.get("modifiers").items():
            if 'custom_' in k:
                dfc[k] = dfc["id"].map(v)
        return dfc

    @property
    def dfm_nan(self):
        dfm = self.get_df().copy()
        for k, v in self.get("modifiers").items():
            dfm[k] = dfm["id"].map(v)
        numeric_columns = dfm.select_dtypes(include=['number']).columns.tolist()
        numeric_columns.remove('value')
        dfm[numeric_columns] = dfm[numeric_columns].fillna(-1)
        return dfm

    def dfmdr(self, dim="h", nan = False, aggfunc='sum'):
        '''
        Deprecated: will be removed.
        dfmdr stands for dataframe with modifiers and dimension reduction
        dim are the list of dimension to be Reduced with sum(), default "h"
        nan convert numeric columns, nan to -1 when value is True
        '''
        new_dims = list(set(self.get("dims")).symmetric_difference(set([dim])))
        dfmdr = (
                self.df.set_index(self.get("preferred_index") + self.get("dims"))
                .drop("symbol", axis=1)
                .sort_index()
                )
        if dim in self.get("dims"):
            dfmdr = dfmdr.groupby(self.get("preferred_index") + new_dims).agg({'value':aggfunc}).reset_index()
        else:
            dfmdr = dfmdr.reset_index()
            
        for k, v in self.get("modifiers").items():
            dfmdr[k] = dfmdr["id"].map(v)
        dfmdr.insert(1, "symbol", self.get("name"))
        if nan:
            numeric_columns = dfmdr.select_dtypes(include=['number']).columns
            dfmdr[numeric_columns] = dfmdr[numeric_columns].fillna(-1)
        return dfmdr

    def __setattr__(self, name, value):
        if name == "df":
            self.set_df(value)
        elif name == "preferred_index":
            self._repo[name] = value
            self.check_index()
        elif name == "name":
            if not self.get("exists_sh"):
                self._repo[name] = value
                if self.get("data") is not None:
                    df = self.get("data").copy()
                    df.drop('symbol', axis=1, inplace=True)
                    df["symbol"] = value
                    self.df = df
            else:
                self._repo[name] = value
        else:
            self._repo[name] = value

    def reorganize(self, dim, common_dims):
        try:
            return self.df.drop("symbol", axis=1).set_index(self.get("preferred_index")+self.get("dims")).unstack(common_dims).fillna(0).sort_index()
        except ValueError as err:
            logger.info(f"Failure while executing: {err}.")
            logger.info("If this transformation involved the merge of two dataframes, make sure Index does not contain duplicate entries.")
            logger.info("This issue is solved by calling pivot tables instead of unstack in Pandas Dataframes, where duplicates are added up.")
            logger.info(f'''Conflictive symbol: "{self.get('name')}"''')
            logger.info(f"[{self.name}]")
            return pd.concat({'value':
                                self.df.drop("symbol", axis=1)
                                .pivot_table(
                                            index=self.get("preferred_index")+[dim],
                                            columns=common_dims,
                                            values='value',
                                            aggfunc=sum,
                                            )
                                .fillna(0)
                                .sort_index()
                            },
                            names=[''], axis=1,
                            )

    def __add__(self, other):
        flag = False
        if isinstance(other, (int, float)):
            # Operation
            new_df = (self.df.set_index(self.get("preferred_index") + self.get("dims")).drop("symbol", axis=1) + other)
            new_name =  "(" + self.get("name") + ")" + "+" + str(other)
            new_dims = self.get("dims")
            return self.new_symbol(self, new_df, new_name, new_dims, other)

        elif set(self.get("dims")) == set(other.get("dims")):
            new_name = self.get("name") + "+" + other.get("name")
            # Operation
            new_df = (self.df.set_index(self.get("preferred_index") + self.get("dims")).drop("symbol", axis=1).sort_index()
                        + other.df.set_index(other.get("preferred_index") + other.get("dims")).drop("symbol", axis=1).sort_index())
            if self.hasNaN(new_df):
                logger.info(f'Null cells replaced by zero after "+" operation [{self.name}]')
                new_df['value'] = 0
                new_dfA = (new_df + self.df.set_index(self.get("preferred_index") + self.get("dims")).drop("symbol", axis=1).sort_index()).fillna({'value':0})
                new_dfB = (new_df + other.df.set_index(other.get("preferred_index") + other.get("dims")).drop("symbol", axis=1).sort_index()).fillna({'value':0})
                new_df = new_dfA + new_dfB

            new_dims = self.get("dims")
            return self.new_symbol(self, new_df, new_name, new_dims, other)

        else:
            flag = True
        if flag:
            raise Exception(f'dims are not equal. {self.get("name")} Dims: {self.get("dims")}, {other.get("name")} Dims: {other.get("dims")}')

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            # Operation
            new_df = (self.df.set_index(self.get("preferred_index") + self.get("dims")).drop("symbol", axis=1) * other)

            new_name = "(" + self.get("name") + ")" + "*" + str(other)
            new_dims = self.get("dims")
            return self.new_symbol(self, new_df, new_name, new_dims, other)

        elif isinstance(other, object):
            diffdims = list(set(self.get("dims")).symmetric_difference(set(other.get("dims"))))
            lendiff = len(diffdims)
            if set(self.get("dims")) == set(other.get("dims")):
                new_name = "(" + self.get("name") + ")" + "*" + other.get("name")
                # Operation
                new_df = (self.df.set_index(self.get("preferred_index") + self.get("dims")).drop("symbol", axis=1).sort_index()
                          * other.df.set_index(other.get("preferred_index") + other.get("dims")).drop("symbol", axis=1).sort_index())
                if self.hasNaN(new_df):
                    logger.info(f'Null cells replaced by zero after "*" operation [{self.name}]')
                    new_df.fillna({'value':0}, inplace=True)

                new_dims = self.get("dims")
                return self.new_symbol(self, new_df, new_name, new_dims, other)

            elif lendiff == 1:
                dim = diffdims[0]
                save = {}
                save[dim in self.get("dims")] = self
                save[dim in other.get("dims")] = other
                common_dims = list(set(save[True].get("dims")).intersection(save[False].get("dims")))
                new_name = "(" + save[False].get("name") + ")" + "*" + save[True].get("name")
                # Operation
                true_df_ = save[True].reorganize(dim, common_dims)
                false_df_ = save[False].df.set_index(save[False].get("preferred_index") + save[False].get("dims")).drop("symbol", axis=1).unstack(common_dims).fillna(0).sort_index()
                new_df = true_df_.mul(false_df_, fill_value=np.nan) # Added fill_value=np.nan for compatibility. pandas>1.3.5 requires it, otherwise recursion error when missing index elements in one df (currently: version 1.5.1)
                new_df = new_df.stack(common_dims)
                logger.info(f'Piece-wise multiplication as "{dim}" dim is only in one symbol [{self.name}]')
                if self.hasNaN(new_df):
                    logger.info(f'Null cells replaced by zero. Operation: {new_name} [{self.name}]')
                    new_df.fillna({'value':0}, inplace=True)

                new_dims = save[True].get("dims")
                return self.new_symbol(save[True], new_df, new_name, new_dims, other)

            elif lendiff > 1:
                common_dims = list(set(self.get("dims")).intersection(other.get("dims")))
                if len(common_dims) > 0:
                    new_name = "(" + self.get("name") + ")" + "*" + other.get("name")
                    # Operation
                    new_df = (self.df.set_index(self.get("preferred_index") + self.get("dims")).drop("symbol", axis=1).sort_index()
                              * other.df.set_index(other.get("preferred_index") + other.get("dims")).drop("symbol", axis=1).sort_index())
                    if self.hasNaN(new_df):
                        logger.info(f'Null cells replaced by zero after "*" operation [{self.name}]')
                        new_df.fillna({'value':0}, inplace=True)

                    new_dims = list(set(self.get("dims") + other.get("dims")))
                    logger.info(f'The difference in dimensions is greater than one. Common {common_dims}, Different: {diffdims} [{self.name}]')
                    return self.new_symbol(self, new_df, new_name, new_dims, other)

                else:
                    raise Exception(f"The difference in dimensions is greater than one: '{diffdims}' and has no common dimensions")
        else:
            raise Exception("The second term is not known, must be a int, float or a Symbol object")

    def __sub__(self, other):
        new_object = self + (other*(-1))
        return new_object

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            # Operation
            new_df = (self.df.set_index(self.get("preferred_index") + self.get("dims")).drop("symbol", axis=1)
                      / other)
            new_name = "(" + self.get("name") + ")" + "/" + str(other)
            new_dims = self.get("dims")
            return self.new_symbol(self, new_df, new_name, new_dims, other)

        elif isinstance(other, object):
            diffdims = list(set(self.get("dims")).symmetric_difference(set(other.get("dims"))))
            lendiff = len(diffdims)
            if set(self.get("dims")) == set(other.get("dims")):
                new_name = "(" + self.get("name") + ")" + "/" + other.get("name")
                # Operation
                new_df = (self.df.set_index(self.get("preferred_index") + self.get("dims")).drop("symbol", axis=1).sort_index()
                            / other.df.set_index(other.get("preferred_index") + other.get("dims")).drop("symbol", axis=1).sort_index())
                if self.hasNaN(new_df):
                    logger.info(f'Null cells replaced by zero after "/" operation [{self.name}]')
                    new_df.fillna({'value':0}, inplace=True)

                new_dims = self.get("dims")
                return self.new_symbol(self, new_df, new_name, new_dims, other)

            elif lendiff == 1:
                dim = diffdims[0]
                save = {}
                save[dim in self.get("dims")] = self
                save[dim in other.get("dims")] = other
                common_dims = list(set(save[True].get("dims")).intersection(save[False].get("dims")))
                new_name = "(" + self.get("name") + ")" + "/" + other.get("name")
                # Operation
                new_df = (self.df.set_index(self.get("preferred_index") + self.get("dims")).drop("symbol", axis=1).unstack(common_dims).fillna(0).sort_index()
                        / other.df.set_index(other.get("preferred_index") + other.get("dims")).drop("symbol", axis=1).unstack(common_dims).fillna(0).sort_index())
                new_df = new_df.stack(common_dims)
                logger.info(f'Piece-wise division as "{dim}" dim is only in one symbol [{self.name}]')
                if self.hasNaN(new_df):
                    logger.info(f'Null cells replaced by zero after "/" operation [{self.name}]')
                    new_df.fillna({'value':0}, inplace=True)

                new_dims = save[True].get("dims")
                return self.new_symbol(save[True], new_df, new_name, new_dims, other)

            elif lendiff > 1:
                raise Exception(f"The difference in dimensions is greater than one: '{diffdims}'")
        else:
            raise Exception("The second term is not known, must be a int, float or a Symbol object")

    def __rtruediv__(self,other):
        if isinstance(other, (int, float)):
            # Operation
            new_df = (other/(self.df.set_index(self.get("preferred_index") + self.get("dims")).drop("symbol", axis=1)))
            new_name = str(other) + "/" + "(" + self.get("name") + ")"
            new_dims = self.get("dims")
            return self.new_symbol(self, new_df, new_name, new_dims, other)

    def __rmul__(self,other):
        if isinstance(other, (int, float)):
            # Operation
            new_df = (other*(self.df.set_index(self.get("preferred_index") + self.get("dims")).drop("symbol", axis=1)))
            new_name = str(other) + "*" + "(" + self.get("name") + ")"
            new_dims = self.get("dims")
            return self.new_symbol(self, new_df, new_name, new_dims, other)

    def __radd__(self,other):
        if isinstance(other, (int, float)):
            # Operation
            new_df = (other + (self.df.set_index(self.get("preferred_index") + self.get("dims")).drop("symbol", axis=1)))
            new_name = str(other) + "+" + "(" + self.get("name") + ")"
            new_dims = self.get("dims")
            return self.new_symbol(self, new_df, new_name, new_dims, other)

    def __rsub__(self,other):
        if isinstance(other, (int, float)):
            # Operation
            new_object = self*(-1) + other
            return new_object

    def dimreduc(self, dim, aggfunc='sum'):
        new_dims = list(set(self.get("dims")).symmetric_difference(set([dim])))
        new_name = f"({self.get('name')}).dimreduc({dim})"
        new_df = (self.df.set_index(self.get("preferred_index") + self.get("dims")).drop("symbol", axis=1).sort_index())
        new_df = new_df.groupby(self.get("preferred_index") + new_dims).agg({'value':aggfunc})
        if self.hasNaN(new_df):
            logger.info(f'Null cells after dimreduc: {new_name} [{self.name}]')
            # new_df.fillna({'value':0}, inplace=True)
        return self.new_symbol(self, new_df, new_name, new_dims)

    def concat(self, other):

        flag = False
        if set(self.get("dims")) == set(other.get("dims")):
            new_df = pd.concat(
                [
                    self.df[
                        self.get("preferred_index")
                        + self.get("dims")
                        + ["symbol", "value"]
                    ],
                    other.df[
                        other.get("preferred_index")
                        + other.get("dims")
                        + ["symbol", "value"]
                    ],
                ]
            )
            new_object = Symbol(
                                self.get("name") + "-concat-" + other.get("name"),
                                "v",
                                dims=self.get("dims"),
                                symbol_type="expression",
                                index=self.get("preferred_index"),
                                )
            new_df["symbol"] = new_object.get("name")
            new_object.df = new_df
            new_object.info = self.info
            new_object.modifiers = self.modifiers_union(other)
            return new_object

        else:
            flag = True
        if flag:
            raise Exception(f'dims are not equal. {self.get("name")} Dims: {self.get("dims")}, {other.get("name")} Dims: {other.get("dims")}')

    @staticmethod
    def new_symbol(object, df, new_name, new_dims, other=None):
        new_object = Symbol(
                            name=new_name,
                            value_type="v",
                            dims=new_dims,
                            symbol_type="expression",
                            index=object.get("preferred_index"),
                            )
        df["symbol"] = new_object.get("name")
        new_object.df = df.reset_index()
        new_object.info = object.info
        new_object.modifiers = object.modifiers_union(other)
        return new_object

    def refdiff(self, reference_id='S000'):

        if not self.get('dims'):
            data = self.df.drop("symbol", axis=1)
            data['value'] = data['value'] - data[data["id"] == reference_id]['value'].values
        else:
            dataframes = []
            for ix, df in self.df.drop("symbol", axis=1).groupby(self.get('dims')):
                df['value'] = df['value'] - df[df["id"] == reference_id]['value'].values
                dataframes.append(df)
            data = pd.concat(dataframes)
        new_object = self*1
        df = data[self.get("preferred_index") + self.get("dims") + ['value']].reset_index(drop=True)
        df['symbol'] = "--"
        new_object.df = df
        new_object.info = self.info
        if isinstance(reference_id, str):
            new_object.name = self.get('name')+'_diff_on_'+ reference_id
        else:
            new_object.name = self.get('name')+'_diff_on_'+ str(reference_id)
 
        return new_object

    def create_mix(self, criteria):
        ''' '''
        combination = self.create_combination(criteria)
        order = criteria.keys()
        return self._find_ids_by_tuple(order,combination)

    def create_combination(self, criteria: dict):
        return list(itertools.product(*criteria.values()))


    def _find_ids_by_tuple(self,key_order,combination):
        groups = {}
        for i, pair in enumerate(combination):
            config = {}
            for k, v in zip(key_order, pair):
                config[k] = ('==',v)
            groups[i] = list(self.find_ids(**config))
        return groups

    def _ref_diff_group(self,refs,groups, verbose=False):
        symbols = []
        for key in groups:
            if len(refs[key]) == 0:
                if verbose:
                    logger.info(f"{refs} for key = {key} no reference id found [{self.name}]")
                    logger.info(groups)
                continue
            else:
                refdiff_symbol = self.shrink_by_id(groups[key]).refdiff(refs[key][0])
                symbols.append(refdiff_symbol)
        return sum(symbols)

    def refdiff_by_sections(self, criteria_dict, criteria_ref_dict, verbose=False):
        ''' '''
        groups = self.create_mix(criteria_dict)
        refs = self.create_mix({**criteria_dict,**criteria_ref_dict})
        return self._ref_diff_group(refs,groups,verbose)

    def refdiff_by_sections_tuple(self, key_ref: str, key_order: list, combination: list, verbose: bool=False):
        ''' '''
        combination_no_ref = []
        index = key_order.index(key_ref)
        for cluster in combination:
            cluster_list = list(cluster)
            cluster_list.pop(index)
            no_ref_cluster = tuple(cluster_list)
            combination_no_ref.append(no_ref_cluster)
        order_no_ref = [key for key in key_order if key != key_ref]
        groups = self._find_ids_by_tuple(order_no_ref,combination_no_ref)
        refs = self._find_ids_by_tuple(key_order,combination)
        return self._ref_diff_group(refs,groups,verbose)



    @property
    def dims(self):
        return self.get('dims')

    @property
    def name(self):
        return self.get('name')

    @property
    def info(self):
        return self.get('info')

    @property
    def items(self):
        if len(self.get('dims')) > 0:
            elements = dict()
            for dim in self.get('dims'):
                elements[dim] = self.df[dim].unique().tolist()
            return elements
        else:
            logger.info(f'This Symbol has no dimensions [{self.name}]')
            return dict()

    @staticmethod
    def hasNaN(df):
        output = False
        for val in df['value'].unique().tolist():
            if pd.isna(val):
                output = True
        return output

    def rename_dim(self, old_dim: str, new_dim: str):
        """ This function renames a dimension in a symbol.

        Args:
            old_dim (str): dimension to be renamed
            new_dim (str): new dimension name

        Returns:
            symbol: Returns a new symbol with the renamed dimension.
        """
        df = self.df.copy()
        df.rename(columns={old_dim: new_dim}, inplace=True)
        new_object      = self*1
        new_object.dims = self.get('dims') + [new_dim]
        new_object.dims.remove(old_dim)
        new_object.df   = df
        new_object.info = self.info
        new_object.name = f"({self.get('name')}).rename_dim({old_dim},{new_dim})"
        return new_object
        
    def add_dim(self, dim_name: str, value: Union[str,dict]):
        '''
        dim_name: new dimension name
        value: if value is a string, the dimension column will contain this value only.
               if value is a dict, the dict must look like {column_header:{column_element: new_element_name}}
               where column_header must currently exists and all column_elements must have a new_element_name.
        '''
        if isinstance(value, str):
            df = self.df.copy()
            df.insert(1, dim_name, value)
            new_object = self*1
            new_object.dims = self.get('dims') + [dim_name]
            new_object.df = df
            new_object.info = self.info
            new_object.name = f"({self.get('name')}).add_dim({dim_name})"
            return new_object
        elif isinstance(value, dict):
            df = self.df.copy()
            df.insert(1, dim_name, None)
            key = list(value.keys())[0]
            val = value[key]
            df[dim_name] = df[key].map(val)
            new_object = self*1
            new_object.dims = self.get('dims') + [dim_name]
            new_object.df = df
            new_object.info = self.info
            new_object.name = f"({self.get('name')}).add_dim({dim_name})"
            return new_object
        else:
            raise Exception('value is neither str nor dict')

    def round(self, decimals:int):
        df = self.df.set_index(self.get("preferred_index") + self.get("dims")).drop("symbol", axis=1)
        df['value'] = df['value'].round(decimals)
        return self.new_symbol(self, df, f"{self.name}.round({str(decimals)})", self.dims)

    def elems2str(self, by='h', string='t', digits=4):
        df = self.df.copy()
        df[by] = df[by].apply(lambda x: string+str(x).zfill(digits))
        new_object = self*1
        new_object.dims = self.get('dims')
        new_object.df = df
        new_object.info = self.info
        new_object.name = f"({self.get('name')}).elems2str({by},{string},{str(digits)})"
        return new_object

    def elems2int(self, by='h'):
        df = self.df.copy()
        df[by] = df[by].str.extract(r"(\d+)", expand=False).astype("int16")
        new_object = self*1
        new_object.dims = self.get('dims')
        new_object.df = df
        new_object.info = self.info
        new_object.name = f"({self.get('name')}).elems2int({by})"
        return new_object

    def replacezero(self, by=1):
        df = self.df.copy()
        df['value'] = df['value'].replace(0.0,by)
        new_object = self*1
        new_object.dims = self.get('dims')
        new_object.df = df
        new_object.info = self.info
        new_object.name = f"({self.get('name')}).replacezero(by={str(by)})"
        return new_object

    def replace(self, this, by=1):
        df = self.df.copy()
        df['value'] = df['value'].replace(this,by)
        new_object = self*1
        new_object.dims = self.get('dims')
        new_object.df = df
        new_object.info = self.info
        new_object.name = f"({self.get('name')}).replace({str(this)},{str(by)})"
        return new_object

    def replaceall(self, by=1):
        df = self.df.copy()
        df['value'] = by
        new_object = self*1
        new_object.dims = self.get('dims')
        new_object.df = df
        new_object.info = self.info
        new_object.name = f"({self.get('name')}).replaceall(by={str(by)})"
        return new_object

    def replacenan(self, by=0):
        df = self.df.copy()
        df['value'] = df['value'].fillna(by)
        new_object = self*1
        new_object.dims = self.get('dims')
        new_object.df = df
        new_object.info = self.info
        new_object.name = f"({self.get('name')}).replacenan(by={str(by)})"
        return new_object

    def fillelems(self):
        dims = self.dims
        if len(dims) == 0:
            raise Exception("Symbol without dimensions")
        elif len(dims) == 1:
            df = pd.concat({'value':
                                self.df.drop("symbol", axis=1)
                                .pivot_table(
                                            index=self.get("preferred_index"),
                                            columns=dims,
                                            values='value',
                                            aggfunc=sum,
                                            )
                                .fillna(0)
                                .sort_index()
                            },
                            names=[''], axis=1,
                            ).stack(dims)
        elif len(dims) > 1:
            if 'h' in dims:
                dim = 'h'
            else:
                dim = dims[0]
            common_dims = [elem for elem in dims if elem != dim]
            df = self.reorganize(dim, common_dims)
            df = df.stack(common_dims)
        new_object = self*1
        new_object.dims = self.get('dims')
        new_object.df = df.reset_index()
        new_object.info = self.info
        new_object.name = f"({self.get('name')}).fillelems()"
        return new_object
    
    def find_ids(self, **karg):
        '''
        find ids whose headings comply the criteria to the value indicated
        dictionary heading as key and value as tuple of (operator, value)
        Example: Z.find_ids(**{'time_series_scen':('==','NaN'),'co2price(n,tech)':('<',80)})
        '''
        dc = self.get('modifiers')
        collector = []
        for k,v in dc.items():
            if k in karg.keys():
                flag = False
                nan_str = False
                id_list = []
                for k2, v2 in v.items():
                    if isinstance(v2,str):
                        if isinstance(karg[k][1],str):
                            if eval(f"'{v2}' {karg[k][0]} '{karg[k][1]}'"):
                                id_list.append(k2)
                                if not flag:
                                    flag = True
                            if karg[k][1] != 'NaN' and v2 == 'NaN':
                                nan_str = True
                        else:
                            continue
                    elif np.isnan(v2):
                        if np.isnan(karg[k][1]):
                            if karg[k][0] == '==':
                                id_list.append(k2)
                                if not flag:
                                    flag = True
                        else:
                            if karg[k][0] == '!=':
                                id_list.append(k2)
                                if not flag:
                                    flag = True
                            elif karg[k][0] != '==':
                                logger.info(f"{k} in {k2} has NaN value for condition '{karg[k][0]} {str(karg[k][1])}'. Not included [{self.name}]")
                            
                    elif np.isnan(karg[k][1]):
                        if karg[k][0] == '!=':
                            id_list.append(k2)
                            if not flag:
                                flag = True
                        else:
                            continue
                    elif eval(f"{v2} {karg[k][0]} {karg[k][1]}"):
                        id_list.append(k2)
                        if not flag:
                            flag = True
                collector.append(set(id_list))
                if not flag:
                    logger.info(f"Column '{k}' does not contain '{karg[k][1]}' [{self.name}]")
                if nan_str:
                    logger.info(f"Column '{k}' has 'NaN' as string. You can filter such string too. [{self.name}]")
        not_present = []
        for cond in karg.keys():
            if cond in dc.keys():
                pass
            else:
                not_present.append(cond)
        if not_present:
            str_cond = ";".join(not_present)
            logger.info(f"{str_cond} not in symbol's data [{self.name}]")
        return set.intersection(*collector)

    def id_info(self,ID):
        '''Gives informaion about the ID

        Args:
            ID (str): ID of the scenario
        Returns:
              A dictionary with the following Modifiers as keys and the corresponding value.
        Example:
           >>> Z.id_info('S0001')
        '''
        dc = dict()
        for k, v in self.get('modifiers').items():
            if ID in v.keys():
                dc[k] = v[ID]
        return dc
    
    def shrink(self, **karg):
        ''' 
        Shrinks the symbol to keep only those rows that comply the given criteria.
        karg is a dictionary of symbol sets as key and elements of the set as value.
        sets and elements must be present in the symbol.
        
        eg:
        Z.shrink(**{'tech':['pv','bio'],'h':[1,2,3,4]})
        
        returns a new symbol
        '''
        for key, value in karg.items():
            if key in self.dims:
                if set(value).issubset(self.items[key]):
                    pass
                else:
                    not_present = set(value) - (set(value) & set(self.items[key]))
                    raise Exception(f"{not_present} is/are not in {self.items[key]}")
            else:
                raise Exception(f"'{key}' is not in {self.dims} for symbol {self.name}")
        query_code = " & ".join([f"{k} in {v}" for k,v in karg.items()])
        df = self.df.copy().query(query_code)

        new_object = self*1
        new_object.dims = self.get('dims')
        new_object.df = df
        new_object.info = self.info
        new_object.name = f"({self.get('name')}).shrink({','.join(['='.join([k,str(v)]) for k,v in karg.items()])})"
        return new_object

    def shrink_by_id(self, id_list):
        '''
        Shrinks the symbol to keep only those rows that comply the given criteria.
        id_list is a list of ids to keep.
        '''
        ids = sorted(list(self.get('modifiers')['run'].keys()))

        if set(id_list).issubset(ids):
            pass
        else:
            not_present = sorted(list(set(id_list) - (set(id_list) & set(ids))))
            logger.info(f"WARNING: {not_present} is/are not in {ids} [{self.name}]")
        query_code = f"id in {id_list}"
        df = self.df.copy().query(query_code)
        new_object = self*1
        new_object.dims = self.get('dims')
        new_object.df = df
        new_object.info = self.info
        new_object.name = f"({self.get('name')}).shrink_by_id({id_list})"
        return new_object

    def shrink_by_attr(self, **kargs):
        ''' 
        shrink_with_attributes generates new symbol based on other attributes of the dataframe. Attributes can be seen with Symbol.get('modifiers').
        Shrink the symbol to keep only the row that comply the criteria in kargs.
        kargs is a dictionary of symbol attributes as key and elements of the attribute columns as value.
        attributes and attribute's elements must be present in the symbol.

        eg:
        Z.shrink(**{'run':[0,1],'country_set':['NA']})

        returns a new symbol
        '''
        for key, value in kargs.items():
            dc = self.get('modifiers')
            if key in dc.keys():
                if set(value).issubset(set(dc[key].values())):
                    pass
                else:
                    not_present = set(value) - (set(value) & set(dc[key].values()))
                    # raise Exception(f"{not_present} is/are not in {list(set(dc[key].values()))}")
            else:
                raise Exception(f"'{key}' is not in {list(dc.keys())} for symbol {self.name}")
        query_code = " & ".join([f"{k} in {v}" for k,v in kargs.items()])
        df = self.dfm.copy().query(query_code)
        new_object = self*1
        new_object.dims = self.get('dims')
        new_object.df = df[['id','symbol'] + self.get('dims') + ['value']]
        new_object.info = self.info
        new_object.name = f"({self.get('name')}).shrink_by_attr({','.join(['='.join([k,str(v)]) for k,v in kargs.items()])})"
        return new_object
    
    def transform(self, subset_of_sets=['n'], func='sum', condition='!=', value=0):
        '''
        transform consists of providing a list of sets to group the dataframe and apply the function. Then the result is compared with a condition and a value. If the condition is true, the resulting rows are kept, otherwise it is dropped. 
        subset_of_sets is a list of sets that are present in the symbol.
        At least one set must be left out of subset_of_sets to apply the function.
        
        eg: N_TECH.transform(subset_of_sets=['n'], func='sum', condition='!=', value=0)
            As N_TECH has 'n' and 'tech' as sets, the function is applied to 'n' and agregating all 'tech' and the result is compared with '!= 0'.
            The final result is a dataframe without elements of 'n' that has a sum of element of 'tech' equal to zero.
            It is a way to clean up the dataframe by removing elements of a set that are not needed.
        '''
        
        ops = {'>': operator.gt,
                '<': operator.lt,
                '>=': operator.ge,
                '<=': operator.le,
                '==': operator.eq,
                '!=': operator.ne}
        
        keep = ops[condition](self.df.groupby(["id"]+subset_of_sets)["value"].transform(func), value)
        df = self.df[keep]
        new_object = self*1
        new_object.dims = self.get('dims')
        new_object.df = df
        new_object.info = self.info
        new_object.name = f"({self.get('name')}).transform({subset_of_sets},{func},{condition},{value})"
        return new_object


    def modifiers_union(self, other=None):
        if isinstance(other, Symbol):
            A = self.get('modifiers')
            B = other.get('modifiers')
            new_modifiers = {}
            for elem in A.keys():
                new_modifiers[elem] = {**A[elem],**B[elem]}
        else:
            new_modifiers = self.get('modifiers')
        return new_modifiers


    def __repr__(self):
        return f'''Symbol(name='{self.get("name")}', \n       value_type='{self.get("value_type")}', \n       dims={self.get("dims")}, \n       symbol_type='{self.get("symbol_type")}', \n       index={self.get("index")}, \n       symbol_handler={self.get("symbol_handler")})'''


def storagecycling(storage_in: Symbol, storage_out: Symbol) -> Symbol:
    '''
    Symbol whose dataframe in the column 'value' has three possible options 0,1,2.
    Where 2 indicates storage cycling. This function gives a 1 if the flow occurs, 
    otherwise, is 0 for each symbol (input and output flow). The both symbols are added,
    if at certain hour input and output flows have 1, the result will be 2.
    
    Args:
        storage_in (Symbol): Symbol storage input flow
        storage_out (Symbol): Symbol storage output flow
        
    Return:
        sto
    '''
    stoin = storage_in/storage_in
    stoin.df['value'] = stoin.df['value'].fillna(0)
    stoout = storage_out/storage_out
    stoout.df['value'] = stoout.df['value'].fillna(0)
    sto = stoout + stoin
    sto.df['value'] = sto.df['value'].fillna(0)
    unique = sto.df['value'].unique().tolist()
    logger.info(f"{unique} [{storage_in} | {storage_out}]")
    if 2.0 in unique:
        logger.success('Storage cycling: True, as the number 2 in "value" column')
    else:
        logger.success('Storage cycling: False, as the number 2 is not present in "value" column')
    logger.success('Use .df to get the dataframe')
    return sto

def add_column_datetime(df, totalrows=8760, reference_date='01-01-2030', t=1):
    """
    Useful to convert the time series from hours index to datetime index.

    Args:
        df (pd.DataFrame): Table on which datetime column should be added.
        totalrows (int): Number of rows on which datetime column should be added.
        reference_date (str): Starting date for adding. E.g. '01/01/2020'.
        t (float): Float frequency, will be changed to string.

    Returns:
        pd.DataFrame: Table with added datetime column.
    """
    fr = {1: "H", 0.5: "30min", 0.25: "15min", 0.125: "450s"}
    freq = fr[t]
    start_date = pd.to_datetime(reference_date)
    drange = pd.date_range(start_date, periods=totalrows, freq=freq)
    df = pd.DataFrame(df.values, columns=df.columns, index=drange)
    df = df.rename_axis("date").copy()
    return df
