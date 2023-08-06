import os
import json
from .settings import config

for k in config:
    if k.endswith('_path') or k.endswith('_cache'):
        if not os.path.isdir(config[k]):
            os.makedirs(config[k])

f = os.path.join(config['home'], '.huggingface/token')
if os.path.exists(f):
    token = open(f).read()
else:
    token = 'please run python -m axiom huggingface add token to '+f

server_file = os.path.join(config['axiom_path'], 'server')
if not os.path.exists(server_file):
    open(server_file, 'w').write('local')

stage_file = os.path.join(config['axiom_path'], 'stage')
if not os.path.exists(stage_file):
    open(stage_file, 'w').write('simple')

stages = ['simple', 'test', 'dev', 'stable']
for stage in stages:
    stage_folder = os.path.join(config['axiom_path'], 'stages', stage)
    subs = ['info', 'obj', 'sha256_info']
    for sub in subs:
        folder = os.path.join(stage_folder, sub)
        if not os.path.isdir(folder):
            os.makedirs(folder)
    cwd_file = os.path.join(stage_folder, 'cwd')
    if not os.path.exists(cwd_file):
        open(cwd_file, 'w').write('')

setting_file = os.path.join(config['axiom_path'], 'settings.json')
if not os.path.exists(server_file):
    prefix = ['simple', 'test', 'dev', 'stable']
    d = {}
    for p in prefix:
        d[p] = os.path.join(config['axiom_path'], 'stages', p)
    json.dump(d, open(setting_file, 'w'))


