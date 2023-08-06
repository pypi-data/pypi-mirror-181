import karray as ka
import numpy as np
import glob
import json
import csv
import os


def load_scenario_info(path, serializer='json'):
    '''
    Load scenario info from file.
    '''
    options = ['json','yaml']
    assert serializer in options, f"Serializer options are {options}. Provided: '{serializer}'."
    if serializer == 'json':
        info = _load_scenario_info_json(path)
    elif serializer == 'yaml':
        info = _load_scenario_info_yaml(path)
    return info

def _load_scenario_info_json(path:str):
    '''
    Load scenario info from json file.
    '''
    base_name = os.path.basename(path.rstrip(os.sep))
    full_path = os.path.join(path, base_name + '.json')
    if os.path.exists(full_path):
        with open(full_path,'r') as stream:
            info = json.load(stream)
            assert all([key in info for key in ['name','metadata']])
            assert info['name'] == base_name, f"Folder name '{base_name}' and 'name':'{info['name']}' do not match."
        return info
    else:
        return {'name':base_name,'metadata':{}}

def _load_scenario_info_yaml(path):
    '''
    Load scenario info from yaml file compatible with dieterpy <= 1.6.0.
    '''
    import yaml
    base_name = os.path.basename(path.rstrip(os.sep))
    full_path1 = os.path.join(path, base_name + '.yml')
    full_path2 = os.path.join(path, base_name + '_config.yml')
    if os.path.exists(full_path1):
        with open(full_path1,'r') as stream:
            info = yaml.load(stream,Loader=yaml.FullLoader)
            assert all([key in info for key in ['name','metadata']])
            assert info['name'] == base_name, f"Folder name '{base_name}' and 'name':'{info['name']}' do not match."
        return info
    elif os.path.exists(full_path2): # dieterpy compatibility
        info = {}
        with open(full_path2,'r') as stream:
            info_ = yaml.load(stream,Loader=yaml.FullLoader)
            info['name'] = info_['id']
            info['metadata'] = info_['config']
            assert info['name'] == base_name, f"Folder name '{base_name}' and 'name':'{info['name']}' do not match."
        return info
    else:
        return {'name':base_name,'metadata':{}}

#### CSV load

def symbol_parser_csv(folder: str, symbol_names: list=[]):
    '''
    Parse all symbols from a folder and returns a dictionary
    '''
    symbol_dict_with_value_type = {}
    for symbs in symbol_names:
        symb_tp = _convert_symbol_name_to_tuple(symbs)
        symbol_dict_with_value_type[symb_tp] = None

    file_list = glob.glob(os.path.join(folder,'*/*.csv'))
    symbol_list = []
    for file in file_list:
        symbol_name = os.path.splitext(os.path.basename(file))[0]
        if (symbol_name, 'v') in symbol_dict_with_value_type if len(symbol_dict_with_value_type) != 0 else True:
            symbol_dict = {}
            # This fields are mandatory for a parser
            symbol_dict['symbol_name'] = symbol_name
            symbol_dict['value_type']  = 'v'
            symbol_dict['path']        = file
            symbol_dict['scenario_id'] = os.path.basename(os.path.dirname(file))
            # Until here
            # you can add more (custom) attributes. It must be added also see handler.py def add_custom_attr() and be an attribute for loader
            symbol_list.append(symbol_dict)
    return symbol_list

def load_csv(path:str, symbol_name:str, keep_zeros:bool, **kwargs):
    '''
    Load custom csv file.
    '''
    folder = os.path.dirname(path)
    file_name = symbol_name
    file_data = f"{file_name}.csv"
    file_coords = f"{file_name}.json"
    path_data = os.path.join(folder, file_data)
    path_coords = os.path.join(folder, file_coords)
    with open(path_data,'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            file_load_headers = row
            break
    file_load_dims = file_load_headers[:-1] # remove last column
    file_load_data =  np.loadtxt(path_data, delimiter=',', skiprows=1, dtype=object)
    index = {}
    for i, dim in enumerate(file_load_dims):
        arr = file_load_data[:,i]
        if np.char.isnumeric(arr[0]):
            arr = arr.astype(np.integer)
        index[dim] = arr
    if file_load_dims:
        value = file_load_data[:,-1].astype('float64')
    else:
        value = file_load_data.astype('float64')
    if os.path.exists(path_coords):
        with open(path_coords,'r') as jsonfile:
            coords = json.load(jsonfile)
    else:
        coords=None
    return {'data': (index, value), 'coords': coords, 'keep_zeros': keep_zeros}



#### Load symbols from arrow - feather file ####

def load_feather(path:str, keep_zeros:bool, **kwargs):
    '''
    Load custom feather file.
    '''
    import pyarrow.feather as ft
    table = ft.read_table(path)
    meta_bstring = table.schema.metadata
    meta_strings = {key.decode('utf-8'): value.decode('utf-8') for (key, value) in meta_bstring.items()}
    meta_custom = {}
    for (key, value) in meta_strings.items():
        k = key.split('.')
        if k[0] in ['symbol','value_type','coords','scenario_id']:
            meta_custom[key] = value
    metadata = _get_metadata(meta_custom, sep = '.')
    raw_coo = table.to_pandas().to_numpy()
    value = raw_coo[:, len(metadata['coords'])].astype(float)
    index = {dim: raw_coo[:,idx] for idx, dim in enumerate(metadata['coords'])}
    return {'data':(index,value), 'coords': metadata['coords'], 'keep_zeros': keep_zeros}

def symbol_parser_feather(folder: str, symbol_names: list=[]):
    '''
    Parse all symbols from a folder and returns a dictionary
    '''
    symbol_dict_with_value_type = {}
    for symbs in symbol_names:
        symb_tp = _convert_symbol_name_to_tuple(symbs)
        symbol_dict_with_value_type[symb_tp] = None

    file_list = glob.glob(os.path.join(folder,'*/*.feather'))
    symbol_list = []
    for file in file_list:
        symbol_info = _info_feather(file)
        if (symbol_info['symbol_name'], symbol_info['value_type']) in symbol_dict_with_value_type if len(symbol_dict_with_value_type) != 0 else True:
            symbol_dict = {}
            # This fields are mandatory for a parser
            symbol_dict['symbol_name'] = symbol_info['symbol_name']
            symbol_dict['value_type']  = symbol_info['value_type']
            symbol_dict['path']        = file
            symbol_dict['scenario_id'] = symbol_info['scenario_id']
            # Until here
            # you can add more (custom) attributes. It must be added also see handler.py def add_custom_attr() and be an attribute for loader
            symbol_list.append(symbol_dict)
    return symbol_list

def _unflatten_dict(a, result = None, sep = '_'):

    if result is None:
        result = dict()
    for k, v in a.items():
        if isinstance(k, str):
            k, *rest = k.split(sep, 1)
        elif isinstance(k, int):
            rest = []
        if rest:
            if rest[0].isdigit():
                _unflatten_dict({int(rest[0]): v}, result.setdefault(k, {}), sep = sep)
            else:
                _unflatten_dict({rest[0]: v}, result.setdefault(k, {}), sep = sep)
        else:
            result[k] = v
    return result

def _metadata_manipulation(metadata, sep = '.'):
    meta_dict = _unflatten_dict(metadata, sep = sep)
    new_dict = {}
    for key, value in meta_dict.items():
        if isinstance(value, dict):
            new_dict[key] = _metadata_manipulation(value, sep = sep)
        else:
            new_dict[key] = value
    return new_dict

def _sort_metadata(meta_dict):
    new_dict = {}
    for key, value in meta_dict.items():
        if isinstance(value, dict):
            keys_sorted_list = sorted(list(value.keys()))
            if all([isinstance(k, int) for k in keys_sorted_list]):
                new_dict[key] = [value[i] for i in keys_sorted_list]
            else:
                new_dict[key] = _sort_metadata(value)
        else:
            new_dict[key] = value
    return new_dict

def _get_metadata(metadata, sep = '.'):
    meta_dict = _metadata_manipulation(metadata, sep = sep)
    meta_dict = _sort_metadata(meta_dict)
    return meta_dict

def _info_feather(path:str):
    '''
    Load symbol info from feather file.
    '''
    import pyarrow.feather as ft
    table = ft.read_table(path)
    meta_bstring = table.schema.metadata
    symbol_name = meta_bstring[b'symbol'].decode('utf-8')
    value_type = meta_bstring[b'value_type'].decode('utf-8')
    scenario_id = meta_bstring[b'scenario_id'].decode('utf-8')
    return {'symbol_name': symbol_name, 'value_type': value_type, 'scenario_id': scenario_id}


#### Load symbols from gdx file ####

def set_gams_dir(gams_dir: str = None):
    """ 
    This function will add GAMS.exe temporarily to the PATH environment variable.

    WARNING: An incorrect path may cause python crashes!!!. Make sure GAMS path is correct.
    """

    from gdxcc import (
        gdxCreateD,
        new_gdxHandle_tp,
        gdxClose,
        gdxFree,
        GMS_SSSIZE,
    )

    gdxHandle = new_gdxHandle_tp()
    gdxCreateD(gdxHandle, gams_dir, GMS_SSSIZE)
    gdxClose(gdxHandle)
    gdxFree(gdxHandle)
    return True

def load_gdx(symbol_name: str, value_type: str='v', path: str='', gams_dir: str= None, inf_to_zero:bool=True, verbose:bool=False, keep_zeros:bool=False, **kwargs):
    '''
    Load custom GDX file.

    Parameters
    ----------
    symbol_name : str
        Name of the symbol to be extracted.
    value_type : str, optional
        Type of the symbol to be extracted. The default is 'v'.
    path : str
        Path to the gdx file.
    gams_dir : str, optional

    '''
    value_types = {'v':0, 'm':1, 'lo':2, 'up':3, 'scale':4}
    assert value_type in value_types.keys(), f'value_type must be one of the following: {value_types.keys()}'
    metadata = _gdx_get_symbol_data_dict(symbol_name=symbol_name, gdx_file=path, gams_dir=gams_dir)
    symbol = _gdx_get_symbol_array_str(symbol_name=symbol_name, gdx_file=path, gams_dir=gams_dir)
    nrdims = len(metadata['dims'])
    col_index = nrdims + value_types[value_type]
    raw_coo = symbol[:, list(range(nrdims)) + [col_index]]
    # Warning: gams2numpy pkg convert EPS to INF as 5e+300
    if inf_to_zero:
        EPS = raw_coo[:, nrdims] == np.float64("5e+300")
        raw_coo[EPS, nrdims] = 0.0
        if verbose:
            if sum(EPS) > 0:
                print('GAMS EPS to 0.0 changed')
    value = raw_coo[:, nrdims].astype(float)
    index = {dim: raw_coo[:,idx] for idx, dim in enumerate(metadata['dims'])}
    coords = {dim: metadata['coords'][dim] for dim in metadata['dims']}
    return {'data': (index, value),'coords': coords, 'keep_zeros': keep_zeros}

def symbol_parser_gdx(folder: str, symbol_names: list=[]):
    '''
    Parse all symbols from a folder and returns a dictionary
    '''
    symbol_dict_with_value_type = {}
    for symbs in symbol_names:
        symb_tp = _convert_symbol_name_to_tuple(symbs)
        symbol_dict_with_value_type[symb_tp] = None

    file_list = glob.glob(os.path.join(folder,'*/*.gdx'))
    symbol_list = []
    for file in file_list:
        scen_id = os.path.basename(file).split('.')[0]
        for (name, symb_type, nrdims) in _symbols_list_from_gdx(file):
            if symb_type == 0: # set
                options = []
            elif symb_type == 1: # parameter
                options = ['v']
            elif symb_type == 2: # variable
                options = ['v', 'm']
            elif symb_type == 3: # equation
                options = ['v', 'm']
            for value_type in options:
                symb_tp = (name, value_type)
                if symb_tp in symbol_dict_with_value_type:
                                        # This fields are mandatory for a parser
                    symbol_list.append({'symbol_name':symb_tp[0],
                                        'value_type':symb_tp[1],
                                        'path':file,
                                        'scenario_id':scen_id,
                                        # Until here
            # you can add more (custom) attributes. It must be added also see handler.py def add_custom_attr() and be an attribute for loader
                                        'inf_to_zero':True, # included with default value. This can be changed later in handler.py def add_custom_attr()
                                        'verbose':False,
                                        'keep_zeros':False,
                                        'gams_dir':None
                                        }) 
                else:
                    if not symbol_names:
                        symbol_list.append({'symbol_name':symb_tp[0],
                                            'value_type':symb_tp[1],
                                            'path':file,
                                            'scenario_id':scen_id,
                                            'inf_to_zero':True,
                                            'verbose':False,
                                            'keep_zeros':False,
                                            'gams_dir':None
                                            })
    return symbol_list

def _symbols_list_from_gdx(filename: str = None, gams_dir: str = None):
    """ It returns a list of symbols' names contained in the GDX file

    Args:
        gams_dir (str, optional): GAMS.exe path, if None the API looks at environment variables. Defaults to None.
        filename (str, optional): GDX filename. Defaults to None.

    Raises:
        Exception: GDX file does not exist or is failed

    Returns:
        list: a list of symbol's names contained in the GDX file
    """

    from gdxcc import (
        gdxSystemInfo,
        gdxSymbolInfo,
        gdxCreateD,
        gdxOpenRead,
        gdxDataReadDone,
        new_gdxHandle_tp,
        gdxClose,
        gdxFree,
        GMS_SSSIZE,
    )

    gdxHandle = new_gdxHandle_tp()
    gdxCreateD(gdxHandle, gams_dir, GMS_SSSIZE)
    gdxOpenRead(gdxHandle, filename)
    exists, nSymb, nElem = gdxSystemInfo(gdxHandle)
    symbols = []
    for symNr in range(nSymb):
        ret, name, nrdims, symb_type = gdxSymbolInfo(gdxHandle, symNr)
        symbols.append((name, symb_type, nrdims))
    gdxDataReadDone(gdxHandle)
    gdxClose(gdxHandle)
    gdxFree(gdxHandle)
    return symbols

def _gdx_get_symbol_array_str(symbol_name: str, gdx_file: str,  gams_dir: str=None):
    from gams2numpy import Gams2Numpy

    g2np = Gams2Numpy(gams_dir)
    uel_map = g2np.gdxGetUelList(gdx_file)
    arr = g2np.gdxReadSymbolStr(gdx_file, symbol_name,uel_map)
    return arr

def _gdx_get_symbol_data_dict(symbol_name: str, gdx_file: str, gams_dir: str=None):

    from gdxcc import (
        gdxSymbolInfo,
        gdxFindSymbol,
        gdxSymbolGetDomainX,
        gdxSymbolInfoX,
        gdxCreateD,
        gdxOpenRead,
        new_gdxHandle_tp,
        gdxClose,
        gdxFree,
        GMS_SSSIZE,
    )

    gdxHandle = new_gdxHandle_tp()
    ret, msg = gdxCreateD(gdxHandle, gams_dir, GMS_SSSIZE)
    ret, msg = gdxOpenRead(gdxHandle, gdx_file)
    assert ret, f"Failed to open '{gdx_file}'"
    ret, symidx = gdxFindSymbol(gdxHandle, symbol_name)
    assert ret, f"Symbol {symbol_name} not found in {gdx_file}"
    if not ret:
        return None
    _, name, NrDims, data_type = gdxSymbolInfo(gdxHandle, symidx)
    _, gdx_domain = gdxSymbolGetDomainX(gdxHandle, symidx)
    _, NrRecs, _, description = gdxSymbolInfoX(gdxHandle, symidx)
    gdxClose(gdxHandle)
    gdxFree(gdxHandle)

    data = {}
    data['symbol'] = symbol_name
    data['dims'] = gdx_domain
    data['coords'] = {dim: list(np.sort(_gdx_get_symbol_array_str(symbol_name=dim, gdx_file=gdx_file, gams_dir=gams_dir)[:,0])) for dim in gdx_domain}
    return data

#### Common functions ####

def _convert_symbol_name_to_tuple(symbol_name: str):
    '''
    Convert symbol name to tuple.
    '''
    symb_list = symbol_name.split('.')
    if len(symb_list) == 1:
        symb_tp = (symb_list[0],'v')
    elif len(symb_list) == 2:
        symb_tp = (symb_list[0], symb_list[1])
    else:
        raise ValueError(f"Symbol name '{symbol_name}' is not valid")
    return symb_tp