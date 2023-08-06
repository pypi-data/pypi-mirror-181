import os
import sys
import uuid
import yaml
import json
import glob
import shutil
import getpass
import pandas as pd
from axiom.common import add_obj_server, rm, getcwd, fs_func, get_server, get_working_folder, get_stage, set_cwd, get_cwd_file, set_server, set_stage, reset, show, ls_cache, cp, ls
from itertools import chain
from axiom.settings import config



def main(sys_argv):
    shell_pid = str(os.getppid())
    global_value_file = os.path.join(config['axiom_path'], '.pid'+shell_pid)
    if not os.path.exists(global_value_file):
        cwd = ''
        global_value = {'cwd': cwd}
        json.dump(global_value, open(global_value_file,'w'))
    if len(sys_argv) == 1:
        lines = open(__file__).read().split('\n')
        lines = [line for line in lines if line.find('if sys_argv[1]') > 0][1:]
        cmds = [line.split("'")[1].split("'")[0] for line in lines]
        comments = [line.split("#")[-1] for line in lines]
        usages = [cmds[i]+': '+comments[i] for i in range(len(cmds))]
        print('\n'.join(usages))
        return

    if sys_argv[1] == 'info': # show basic info of the project
        print('my file name', __file__)
        print('config', config)

    def compile(txt):
        from axiom.settings import config
        folder = str(uuid.uuid4())
        os.makedirs(os.path.join(folder, 'obj'))
        me, code_txt = txt.split('##__AXIOM_INFO_END__\n')
        code_txt = code_txt.split('##__AXIOM_FUNCTION_END__')[0]
        print('me'.center(50,'='))
        print(me)
        print('code'.center(50,'='))
        print(code_txt)
        open(os.path.join(folder, 'obj', 'main.py'),'w').write(code_txt)
        info_file = os.path.join(folder, 'info.yaml')

        me = me[me.find('=')+1:]
        yaml.safe_dump(json.loads(me), open(info_file, 'w'))
        print('info_file', info_file)
        add_obj_server(os.path.join(folder, 'obj'))
        shutil.rmtree(folder)

    if sys_argv[1] == 'compile':
        txt = open(sys_argv[2]).read()
        blocks = txt.split('##__AXIOM_BLOCK_BEGIN__')[1:]
        blocks = [b.split('##__AXIOM_BLOCK_END__')[0] for b in blocks]
        for b in blocks:
            compile(b)

    if sys_argv[1] == 'what': # show what can we show
        fs = glob.glob(os.path.join(config['axiom_path'], 'info', '*'))
        yamls = [yaml.safe_load(open(f).read()) for f in fs]
        if len(sys_argv) == 2:
            keys = [list(y.keys()) for y in yamls]
            print(list(set(list(chain.from_iterable(keys)))))
        if len(sys_argv) == 3:
            obj_properties = []
            for y in yamls:
                x = y[sys_argv[2]]
                if isinstance(x, list):
                    obj_properties += x
                else:
                    obj_properties.append(x)

            obj_properties = sorted(list(set(obj_properties)))
            print('\n'.join(obj_properties))

    if sys_argv[1] == 'add': # add the current folder as the obj
        add_obj_server(sys_argv[2])

    if sys_argv[1] == 'rm': # remove an axiom object by given name
        rm(sys_argv[2])

    if sys_argv[1] == 'extract': # exting an object to the corrent folder
        md5 = sys_argv[2]
        f = os.path.join(config['axiom_path'], 'obj', md5)
        cmd = 'cp %s ./&& tar zfx %s&&rm %s' % (f, md5, md5)
        print(cmd)
        os.system(cmd)


    def run_python_block(txt):
        file_name = str(uuid.uuid4())
        open(file_name, 'w').write(txt)
        os.system('python '+file_name)
        os.remove(file_name)

    if sys_argv[1] == 't': # test a file with __AXIOM__BLOCK__BEGIN__ block, with test
        txt = open(sys_argv[2]).read()
        blocks = txt.split('##__AXIOM_BLOCK_BEGIN__')[1:]
        blocks = [b.split('##__AXIOM_BLOCK_END__')[0] for b in blocks]
        for b in blocks:
            run_python_block(b)

    if sys_argv[1] == 'pwd':
        print(getcwd())

    if sys_argv[1] == 'ls':
        if len(sys_argv) == 2:
            ls()
        else:
            ls(sys_argv[2])

    if sys_argv[1] == 'ls.update':
        if len(sys_argv) == 2:
            fs_func[get_server()]['ls'](None, update=True)
        else:
            fs_func[get_server()]['ls'](sys_argv[2], update=True)

    if sys_argv[1] == 'cd':
        if len(sys_argv) == 2:
            target_folder = ""
            set_cwd(target_folder)
        else:
            working_folder = get_working_folder(get_stage())
            sub = sys_argv[2]
            cwd = open(get_cwd_file()).read()
            if sub == '..':
                target_folder = os.path.split(cwd)[0]
            else:
                target_folder = os.path.join(cwd, sub)
            if os.path.isdir(os.path.join(working_folder, 'info', target_folder)):
                set_cwd(target_folder)
            else:
                print('not found:', target_folder)

    if sys_argv[1] == 'server': # set the server, from [local, huggingface, bypy] or get the server
        if len(sys_argv) == 2:
            print(get_server())
        else:
            set_server(sys_argv[2])

    if sys_argv[1] == 'huggingface': # settup the huggingface token and username
        token = getpass.getpass('huggingface token:')
        user_name = input('huggingface private db user:')
        axiom_directory_server = input('axiom_directory_server:')
        key = input('axiom_directory_server key:')

        huggingface_path = os.path.join(config['home'], '.huggingface')
        if not os.path.isdir(huggingface_path):
            os.mkdir(huggingface_path)
        open(os.path.join(huggingface_path, 'token'), 'w').write(token)
        open(os.path.join(huggingface_path, 'user_name'), 'w').write(user_name)
        open(os.path.join(huggingface_path, 'axiom_directory_server'), 'w').write(axiom_directory_server)
        open(os.path.join(huggingface_path, 'key'), 'w').write(key)

    if sys_argv[1] == 'data.info': ## add info.yaml template to the current folder
        s = '''axiom_name: __AXIOM__
description:
given_name: com/some-company/some-project/some-dataset
type: data.int'''
        open('info.yaml', 'w').write(s)

    if sys_argv[1] == 'stage': # ['simple', 'test', 'dev', 'stable', 'publish', 'axiom_test']
        if len(sys_argv) == 2:
            print(get_stage())
        else:
            set_stage(sys_argv[2])
    if sys_argv[1] == 'reset':
        reset()

    if sys_argv[1] == 'example':
        '''
            a add ./int_3/obj
            a add ./int_4/obj
            a compile add_func.py
            a compile add_one_func.py
            a compile add_one_and_two.py
        '''
        folder_me = os.path.split(__file__)[0]
        int_3_folder = os.path.join(folder_me, 'example', 'simple_add', 'int_3')
        int_4_folder = os.path.join(folder_me, 'example', 'simple_add', 'int_4')
        int_3_obj_folder = os.path.join(int_3_folder, 'obj')
        int_4_obj_folder = os.path.join(int_4_folder, 'obj')
        if not os.path.isdir(int_3_obj_folder):
            os.makedirs(int_3_obj_folder)
        if not os.path.isdir(int_4_obj_folder):
            os.makedirs(int_4_obj_folder)
        open(os.path.join(int_3_obj_folder, 'value'), 'w').write('3')
        open(os.path.join(int_4_obj_folder, 'value'), 'w').write('4')
        info3 = {
            'axiom_name': '__AXIOM__',
            'description': 'for test axiom utilities',
            'given_name': 'axiom/example/int_3',
            'type': 'data.int'
        }
        info4 = {
            'axiom_name': '__AXIOM__',
            'description': 'for test axiom utilities',
            'given_name': 'axiom/example/int_4',
            'type': 'data.int'
        }
        yaml.safe_dump(info3, open(os.path.join(int_3_folder, 'info.yaml'), 'w'))
        yaml.safe_dump(info4, open(os.path.join(int_4_folder, 'info.yaml'), 'w'))
        main(['a', 'add', int_3_obj_folder])
        main(['a', 'add', int_4_obj_folder])
        main(['a', 'compile', os.path.join(folder_me, 'example', 'simple_add', 'add_func.py')])
        main(['a', 'compile', os.path.join(folder_me, 'example', 'simple_add', 'add_one_func.py')])
        main(['a', 'compile', os.path.join(folder_me, 'example', 'simple_add', 'add_one_and_two.py')])
        main(['a', 'compile', os.path.join(folder_me, 'example', 'simple_add', 'add_by_config.py')])
        just_test_file = os.path.join(folder_me, 'example', 'simple_add', 'just_test.py')
        os.system('python %s' % just_test_file)
    if sys_argv[1] == 'show':
        show(sys_argv[2])

    if sys_argv[1] == 'ls.cache':
        if len(sys_argv) == 3 and sys_argv[2] == 'table':
            ls_cache(table=True)
        else:
            ls_cache(table=False)

    if sys_argv[1] == 'cp': # cp huggingface test local simple given_name
        from_server, from_stage, to_server, to_stage, given_name = sys_argv[2:]
        cp(from_server, from_stage, to_server, to_stage, given_name)

        

if __name__ == '__main__':
    main(sys.argv)
