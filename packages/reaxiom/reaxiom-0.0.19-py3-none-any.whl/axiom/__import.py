import os
import sys
import yaml
import uuid
import time
import shutil
import datetime
import importlib
from .settings import config as _config
from functools import partial
#from .common import get_uuid_by_given_name, get_folder_md5, add_obj_common, download_obj_from_server
from .common import get_sha256_by_given_name, download_node_from_server, get_folder_sha256, add_obj_server



def get_function_by_given_name(given_name):
    sha256 = get_sha256_by_given_name(given_name)
    if sha256 is not None:
        function_folder = os.path.join(_config['axiom_cache'], sha256, 'obj')
        if not os.path.isdir(function_folder):
            download_node_from_server(sha256, given_name)
        sys.path.append(function_folder)
        print('function_folder', function_folder)
        ## when multiple functions are imported, they share the same "main"
        new_main = 'a'+str(uuid.uuid4())
        new_main_file = os.path.join(function_folder, new_main+'.py')
        open(new_main_file, 'w').write(open(os.path.join(function_folder, 'main.py')).read())
        x = importlib.import_module(new_main)
        print(x)
        os.remove(new_main_file)
        return x.main, sha256
    return None

def the_func(config={}, in_folder=[], given_name=[], out_folder=None, func_name=''):
    f, sha256 = get_function_by_given_name(func_name)
    if isinstance(given_name, str):
        given_name = [given_name]
    if out_folder is None:
        out_folders = []
        n = len(given_name)
        obj_folders = []
        for i in range(n):
            random_id = str(uuid.uuid4())
            out_folder = os.path.join(_config['axiom_cache'], random_id)
            obj_folder = os.path.join(out_folder, 'obj')
            obj_folders.append(obj_folder)
            print('making dir', obj_folder)
            os.makedirs(obj_folder)
            out_folders.append(out_folder)
    info_file = os.path.join(_config['axiom_cache'], sha256, 'info.yaml')
    function_info = yaml.safe_load(open(info_file))
    if function_info['axiom_name'] == '__AXIOM__':
        function_info['axiom_name'] = sha256
    print('function_info', function_info)
    t_begin = time.time()
    time_begin = str(datetime.datetime.now())
    if len(obj_folders) == 1:
        f(config, in_folder, given_name, obj_folders[0])
    else:
        f(config, in_folder, given_name, obj_folders)
    time_end = str(datetime.datetime.now())
    t_end = time.time()
    in_axiom_names = []
    if isinstance(in_folder, str):
        in_folder = [in_folder]
    for i in range(len(in_folder)):
        in_folder_ = in_folder[i]
        d = yaml.safe_load(open(os.path.join(os.path.split(in_folder_)[0], 'info.yaml')).read())
        if d['axiom_name'] == '__AXIOM__':
            in_axiom_names.append(os.path.split(os.path.split(in_folder_)[0])[-1])
        else:
            in_axiom_names.append(d['axiom_name'])


    print('in_axiom_names', in_axiom_names)
    info = {}
    uname = str(os.uname()).replace("'", '"').replace('\n', '')
    if isinstance(function_info['output'], str):
        function_outputs = [function_info['output']]
    else:
        function_outputs = function_info['output']
    n_out = len(function_outputs)
    return_folders = []
    for i in range(n_out):
        out_folder = out_folders[i]
        _name = given_name[i]
        the_type = function_outputs[i]
        description = 'data from function '+func_name
        info['type'] = the_type
        info['given_name'] = _name
        info['axiom_name'] = {'config': config, 'function': function_info['axiom_name'], 'in_data': in_axiom_names, 'out': '%d/%d' % (i, n_out)}
        info['description'] = description
        info['run_begin_time'] = time_begin
        info['run_end_time'] = time_end
        info['running_time'] = t_end - t_begin
        info['uname'] = uname
        info_file = os.path.join(out_folder,'info.yaml')
        yaml.safe_dump(info, open(info_file, 'w'))
    for out_folder in out_folders:
        sha256,_ = get_folder_sha256(os.path.join(out_folder, 'obj')) # md5 is the one with obj folder
        print('out_folder',out_folder)
        sha256_folder = os.path.join(os.path.split(out_folder)[0], sha256)
        print('sha256_folder', sha256_folder)
        shutil.move(out_folder, sha256_folder)
        return_folders.append(os.path.join(sha256_folder, 'obj'))
        add_obj_server(os.path.join(sha256_folder, 'obj'))
    if len(return_folders) == 1:
        return_folders = return_folders[0]
    return return_folders

def main(func_name):
    print('axiom import', func_name)
    return partial(the_func, func_name=func_name)
