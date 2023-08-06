import os
import glob
import json
import yaml
import uuid
import shutil
import hashlib
import requests
import pandas as pd

from os.path import join
import huggingface_hub as hh
from .settings import config
from urllib.request import urlopen
fs_func = {} # file system func for local, huggingface, and bypy




def set_stage(stage):
    candidates = ['simple', 'test', 'dev', 'stable', 'publish', 'axiom_test']
    '''
    simple: to start over at any time, nothing will be lost when deleted
    test: testing some functions of axiom or to see how it works, suggesting delete time: daily
    develop: developing a project
    stable: the development is stable
    publish: publishing as a jounal paper, not deleting
    axiom_test: testing axiom itself
    '''
    assert stage in candidates
    stage_file = os.path.join(config['axiom_path'], 'stage')
    open(stage_file, 'w').write(stage)

def get_stage():
    stage_file = os.path.join(config['axiom_path'], 'stage')
    return open(stage_file).read()

def get_server():
    server_setting_file = os.path.join(config['axiom_path'], 'server')
    return open(server_setting_file).read()

def set_server(server):
    candidates = ['local', 'huggingface', 'bypy']
    assert server in candidates
    server_setting_file = os.path.join(config['axiom_path'], 'server')
    open(server_setting_file, 'w').write(server)

def get_folder_fs(folder):
    fs = []
    for subdir, _, files in os.walk(folder):
        fs += [os.path.join(subdir, f) for f in files]
    return fs

def get_folder_sha256(folder):
    md5 = hashlib.sha256()
    size_ = 0
    for subdir, _, files in os.walk(folder):
        for f in files:
            full_name = os.path.join(subdir, f)
            size_ += os.stat(full_name).st_size
            with open(full_name, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    md5.update(chunk)
    return md5.hexdigest(), size_

## todo, what if multiple sha256s share same given name or multiple given names share same sha256


def list_yamls(ys):
    sha256s = [y['sha256'][:10]+'...' for y in ys]
    columns = ['given_name', 'type', 'size', 'description']
    d = {}
    for i in range(len(ys)):
        d[sha256s[i]] = [ys[i]['given_name'], ys[i]['type'], ys[i]['compressed_size'], ys[i]['description'][:10]]
    df = pd.DataFrame.from_dict(d, orient='index', columns=columns)
    print(df)

def list_axiom(fs):
    ys = [yaml.safe_load(open(f).read()) for f in fs]
    list_yamls(ys)

def axiom_ls(base_folder, path, ignores=[]):
    if path is None:
        cwd = open(get_cwd_file()).read()
        folder = join(base_folder, cwd)
        folders = os.listdir(folder)
        folders = [folder for folder in folders if not folder in ignores]
        print('\n'.join(folders))
    else:
        folder = os.path.join(base_folder, path)
        fs = get_folder_fs(folder)
        list_axiom(fs)





def get_folder_by_given_name(given_name, server=None, stage=None):
    sha256s = glob.glob(os.path.join(config['axiom_cache'], '*'))
    sha256s = [x for x in sha256s if os.path.split(x)[-1].find('-') < 0]
    yas = [yaml.safe_load(open(os.path.join(sha256, 'info.yaml'))) for sha256 in sha256s]
    yas = [y for y in yas if y['given_name'] == given_name]
    if len(yas) == 0:
        sha256 = get_sha256_by_given_name(given_name, server, stage)
        if sha256 is None:
            return None
        download_node_from_server(sha256, given_name, server, stage)
    else:
        if len(yas) > 1:
            print('warning, multiple sha256s share with the same given_name', given_name)
            print('the are')
            print('\n'.join([y['sha256'] for y in yas]))
            print('only the first one is selected')
        sha256 = yas[0]['sha256']
    cache_folder = os.path.join(config['axiom_cache'], sha256, 'obj')
    return cache_folder


def add_obj_server(folder, server=None, stage=None): # folder with all data but not info.yaml
    if server is None:
        server = get_server()
    if stage is None:
        stage = get_stage()
    uuid_folder = os.path.split(folder)[0]
    info_file = os.path.join(uuid_folder, 'info.yaml')
    info_yaml = yaml.safe_load(open(info_file))
    if not os.path.exists(info_file):
        if info_file == 'info.yaml':
            info_file = os.path.join('.', info_file)
        print("make sure %s exists" % info_file)
        return None
    obj_folder = os.path.split(folder)[-1]
    cmd = 'cd '+folder+'&& tar zfc ../'+obj_folder+'.tar.gz ./'
    print(cmd)
    os.system(cmd)
    sha256, folder_size = get_folder_sha256(folder)
    gz_size = os.stat(folder+'.tar.gz').st_size
    info_yaml['original_size'] = folder_size
    info_yaml['compressed_size'] = gz_size
    info_yaml['sha256'] = sha256
    compressed_obj_file = folder+'.tar.gz'
    given_name = info_yaml['given_name']
    yaml.safe_dump(info_yaml, open(info_file, 'w'))
    fs_func[server]['put_node'](compressed_obj_file, info_yaml, sha256, given_name)
    if os.path.exists(compressed_obj_file):# when server is local, just move, this might not exist
        os.remove(compressed_obj_file)
    print(sha256, 'added')







def put_axiom_directory(info_yaml, stage=None):
    if stage is None:
        stage = get_stage()
    axiom_directory_server = open(os.path.join(config['home'], '.huggingface', 'axiom_directory_server')).read()
    key = open(os.path.join(config['home'], '.huggingface', 'key')).read()
    url = f'{axiom_directory_server}/put'
    d = {'key': key, 'stage': stage, 'info': info_yaml}
    response = requests.post(url, json=d)
    text = response.text
    print(text)
    return text






def get_axiom_directory(given_name, stage=None):
    if stage is None:
        stage = get_stage()
    axiom_directory_server = open(os.path.join(config['home'], '.huggingface', 'axiom_directory_server')).read()
    key = open(os.path.join(config['home'], '.huggingface', 'key')).read()
    url = f'{axiom_directory_server}/get'
    d = {'key': key, 'stage': stage, 'given_name': given_name}
    text = requests.post(url, json=d).text
    if not text.startswith('err'):
        return yaml.safe_load(text)
    else:
        return None




def get_info_huggingface(update=False): # return the info folder
    stage = get_stage()
    user_name = open(os.path.join(config['home'], '.huggingface', 'user_name')).read()
    cache_dir = config['huggingface_cache']
    repo_id_info = user_name+'/'+stage+'_info'
    sha_file = os.path.join(config['home'], '.huggingface', stage+'_info.sha')
    if update:
        hh.snapshot_download(repo_id_info, repo_type='dataset', cache_dir=cache_dir, token=True)
        sha = hh.dataset_info(repo_id_info).sha
        open(sha_file, 'w').write(sha)
    else:
        if os.path.exists(sha_file):
            sha = open(sha_file).read()
        else:
            sha = hh.dataset_info(repo_id_info).sha
            open(sha_file, 'w').write(sha)
    info_folder = os.path.join(config['huggingface_cache'], 'datasets--'+repo_id_info.replace('/','--'), 'snapshots', sha)
    return info_folder

def rm_axiom_directory(given_name):
    axiom_directory_server = open(os.path.join(config['home'], '.huggingface', 'axiom_directory_server')).read()
    key = open(os.path.join(config['home'], '.huggingface', 'key')).read()
    stage = get_stage()
    url = f"{axiom_directory_server}/rm"
    d = {'key': key, 'stage': stage, 'given_name': given_name}
    text = requests.post(url, json=d).text
    print('rm_axiom_directory', text)






def get_folder_by_sha256(sha256, server='local'):
    cache_folder = os.path.join(config['axiom_cache'], sha256, 'obj')
    if os.path.isdir(cache_folder):
        return cache_folder
    else:
        download_node_from_server(sha256, server) # download obj and info from server
        if os.path.isdir(cache_folder):
            return cache_folder
    return None


def get_folder_by_given_name(given_name, stage=None):
    sha256s = glob.glob(os.path.join(config['axiom_cache'], '*'))
    sha256s = [x for x in sha256s if os.path.split(x)[-1].find('-') < 0]
    yas = [yaml.safe_load(open(os.path.join(sha256, 'info.yaml'))) for sha256 in sha256s]
    yas = [y for y in yas if y['given_name'] == given_name]
    if len(yas) == 0:
        sha256 = get_sha256_by_given_name(given_name, stage)
        if sha256 is None:
            return None
        download_node_from_server(sha256, given_name, stage)
    else:
        if len(yas) > 1:
            print('warning, multiple sha256s share with the same given_name', given_name)
            print('the are')
            print('\n'.join([y['sha256'] for y in yas]))
            print('only the first one is selected')
        sha256 = yas[0]['sha256']
    cache_folder = os.path.join(config['axiom_cache'], sha256, 'obj')
    return cache_folder

def rm(given_name):
    server = get_server()
    fs_func[server]['rm'](given_name)

def get_working_folder(stage): # for local only
    return join(config['axiom_path'], 'stages', stage)

def get_cwd_file():
    stage = get_stage()
    return join(config['axiom_path'], 'stages', stage, 'cwd')


def reset_local():
    stage = get_stage()
    #assert stage in ['simple', 'test']
    assert stage in ['simple']
    working_folder = get_working_folder(stage)
    if os.path.isdir(working_folder):
        shutil.rmtree(working_folder)
    subs = ['obj', 'info', 'sha256_info']
    for sub in subs:
        folder = join(working_folder, sub)
        print('creating folder', folder)
        os.makedirs(folder)


def get_repo_id(what, stage=None): # what in ['info', 'obj', 'sha256_info']
    if stage is None:
        stage = get_stage()
    user_name = open(os.path.join(config['home'], '.huggingface', 'user_name')).read()
    repo_id = user_name+'/'+stage+'_'+what
    return repo_id

def reset_one(what):
    stage = get_stage()
#    assert stage in ['simple', 'test']
    assert stage in ['simple']
    repo_id = get_repo_id(what)
    try:
        hh.delete_repo(repo_id=repo_id, repo_type='dataset', token=True)
    except Exception as e:
        print(e)
    hh.create_repo(repo_id, repo_type='dataset', token=True)


def reset_axiom_directory():
    stage = get_stage()
    assert stage in ['simple']
    axiom_directory_server = open(os.path.join(config['home'], '.huggingface', 'axiom_directory_server')).read()
    url = f"{axiom_directory_server}/reset?stage={stage}"
    urlopen(url)


def reset_huggingface():
    stage = get_stage()
    #assert stage in ['simple', 'test']
    assert stage in ['simple']
    whats = ['obj']
    for what in whats:
        reset_one(what)
    reset_axiom_directory()


def reset():
    server = get_server()
    if server == 'local':
        reset_local()
    elif server == 'huggingface':
        reset_huggingface()

def getcwd():
    return open(get_cwd_file()).read()

def ls(sub=None):
    server = get_server()
    fs_func[server]['ls'](sub)

def show(given_name):
    folder = get_folder_by_given_name(given_name)
    sha256_folder = os.path.split(folder)[0]
    info_file = join(sha256_folder, 'info.yaml')
    print(open(info_file).read())

def set_cwd(folder):
    open(get_cwd_file(), 'w').write(folder)

def ls_cache(table=False):
    fs = glob.glob(os.path.join(config['axiom_cache'], '*'))
    ys = [yaml.safe_load(open(os.path.join(f, 'info.yaml'))) for f in fs]
    if table:
        list_yamls(ys)
    else:
        for i in range(len(fs)):
            print(fs[i], ys[i])

def cp(from_server, from_stage, to_server, to_stage, given_name):
    sha256 = fs_func[from_server]['get_sha256_by_given_name'](given_name, from_stage)
    folder = get_folder_by_given_name()


def get_sha256_by_given_name_local(given_name, stage=None):
    if stage is None:
        stage = get_stage()
    working_folder = get_working_folder(stage)
    info_folder = os.path.join(working_folder, 'info', given_name+'.yaml')
    return yaml.safe_load(open(info_folder))['sha256']



def put_node_local(compressed_obj_file, info_yaml, sha256, given_name, stage=None): # node means obj + info
    if stage is None:
        stage = get_stage()
    working_folder = get_working_folder(stage)
    shutil.move(compressed_obj_file, os.path.join(working_folder, 'obj', sha256))
    target_info_file = os.path.join(working_folder, 'info', given_name+'.yaml')
    target_info_folder = os.path.split(target_info_file)[0]
    if not os.path.isdir(target_info_folder):
        os.makedirs(target_info_folder)
    target_sha256_info_file = os.path.join(working_folder, 'sha256_info', sha256+'.yaml')
    yaml.safe_dump(info_yaml, open(target_info_file, 'w'))
    yaml.safe_dump(info_yaml, open(target_sha256_info_file, 'w'))


def download_node_from_server_local(sha256, given_name):
    extract_folder = os.path.join(config['axiom_cache'], sha256, 'obj')
    working_folder = get_working_folder(get_stage())
    if not os.path.isdir(extract_folder):
        os.makedirs(extract_folder)
        sha_full_path = os.path.join(working_folder, 'obj', sha256)
        cmd = 'tar zxf %s -C %s' % (sha_full_path, extract_folder)
        print(cmd)
        os.system(cmd)
    source_info_file = os.path.join(working_folder, 'info', given_name+'.yaml')
    target_info_file = os.path.join(config['axiom_cache'], sha256, 'info.yaml')
    shutil.copy(source_info_file, target_info_file)
    return extract_folder


def ls_local(path, ignores=[]):
    stage = get_stage()
    base_folder = join(config['axiom_path'], 'stages', stage, 'info')
    axiom_ls(base_folder, path, ignores)

def rm_local(given_name):
    stage = get_stage()
    working_folder = get_working_folder(stage)
    sha256 = get_sha256_by_given_name_local(given_name)
    obj_file = os.path.join(working_folder, 'obj', sha256)
    if os.path.exists(obj_file):
        os.remove(obj_file)
    sha256_info_file = os.path.join(working_folder, 'sha256_info', sha256+'.yaml')
    if os.path.exists(sha256_info_file):
        os.remove(sha256_info_file)
    if os.path.exists(obj_file):
        os.remove(obj_file)
    info_file = os.path.join(working_folder, 'info', given_name+'.yaml')
    if os.path.exists(info_file):
        os.remove(info_file)

fs_func['local'] = {
    'get_sha256_by_given_name': get_sha256_by_given_name_local,
    'put_node': put_node_local,
    'download_node_from_server': download_node_from_server_local,
    'ls': ls_local,
    'rm': rm_local,
}


def get_sha256_by_given_name_huggingface(given_name, stage=None):
    info = get_axiom_directory(given_name, stage)
    assert info is not None
    return info['sha256']


def put_node_huggingface(compressed_obj_file, info_yaml, sha256, given_name, stage=None): # node means obj + info
    if stage is None:
        stage = get_stage()
    repo_id = get_repo_id('obj', stage)
    hh.upload_file(path_or_fileobj=compressed_obj_file,path_in_repo=sha256,repo_id=repo_id,repo_type="dataset",token=True)
    put_axiom_directory(info_yaml, stage)


def download_node_from_server_huggingface(sha256, given_name, stage=None):
    cache_dir = config['huggingface_cache']
    repo_id = get_repo_id('obj', stage)
    hh.hf_hub_download(repo_id=repo_id, filename=sha256, repo_type="dataset", cache_dir=cache_dir, token=True)
    sha = hh.dataset_info(repo_id).sha
    obj_folder = os.path.join(config['huggingface_cache'], 'datasets--'+repo_id.replace('/','--'), 'snapshots', sha)
    extract_folder = os.path.join(config['axiom_cache'], sha256, 'obj')
    if not os.path.isdir(extract_folder):
        os.makedirs(extract_folder)
        md5_full_path = os.path.join(obj_folder, sha256)
        cmd = 'tar zxf %s -C %s' % (md5_full_path, extract_folder)
        print(cmd)
        os.system(cmd)

    target_info_file = os.path.join(config['axiom_cache'], sha256, 'info.yaml')
    info = get_axiom_directory(given_name)
    assert info is not None
    yaml.safe_dump(info, open(target_info_file, 'w'))
    return extract_folder

def ls_huggingface(path):
    axiom_directory_server = open(os.path.join(config['home'], '.huggingface', 'axiom_directory_server')).read()
    key = open(os.path.join(config['home'], '.huggingface', 'key')).read()
    stage = get_stage()
    if path is None:
        cwd = open(get_cwd_file()).read()
        url = f"{axiom_directory_server}/ls"
        d = {'key': key, 'stage': stage, 'path': cwd}
        text = requests.post(url, json=d).text
        print(text)
    else:
        url = f"{axiom_directory_server}/listall"
        d = {'key': key, 'stage': stage, 'path': path}
        text = requests.post(url, json=d).text
        if not text.startswith('err'):
            d = json.loads(text)
            ys = list(d.values())
            list_yamls(ys)


def rm_huggingface(given_name):
    sha256 = get_sha256_by_given_name_huggingface(given_name)
    repo_id = get_repo_id('obj')
    hh.delete_file(sha256, repo_id=repo_id, repo_type='dataset', token=True)
    rm_axiom_directory(given_name)    

fs_func['huggingface'] = {
    'get_sha256_by_given_name': get_sha256_by_given_name_huggingface,
    'put_node': put_node_huggingface,
    'download_node_from_server': download_node_from_server_huggingface,
    'ls': ls_huggingface,
    'rm': rm_huggingface,
}


def get_sha256_by_given_name(given_name, server=None, stage=None):
    if server is None:
        server = get_server()
    if stage is None:
        stage = get_stage()
    return fs_func[server]['get_sha256_by_given_name'](given_name, stage)


def download_node_from_server(sha256, given_name, server=None, stage=None):
    if server is None:
        server = get_server()
    if stage is None:
        stage = get_stage()
    fs_func[server]['download_node_from_server'](sha256, given_name, stage)
