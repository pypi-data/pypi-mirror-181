##__AXIOM_BLOCK_BEGIN__
block_info = {
    "type": "function",
    "given_name": "axiom/example/int_add_by_config",
    "input": "data.int",
    "output": "data.int",
    "axiom_name": "__AXIOM__",
    "description": "add input by config['n']"
}


##__AXIOM_INFO_END__
import os

def int_reader(folder):
    return int(open(os.path.join(folder, 'value')).read())

def int_writer(folder, value):
    assert isinstance(value, int)
    open(os.path.join(folder, 'value'), 'w').write(str(value))

def main(config, in_folder, given_name, out_folder):
    assert isinstance(in_folder, str)
    value = int_reader(in_folder)
    int_writer(out_folder, value+config['n'])
    return out_folder

##__AXIOM_FUNCTION_END__


if __name__ == '__main__':
    out_folder = '/tmp/tmp/a'
    data = '/Users/test/reaxiom/cache/eccbc87e4b5ce2fe28308fd9f2a7baf3/obj'
    output = main(
        config={},
        in_folder=data,
        given_name = 'axiom/example/int_4',
        out_folder = out_folder
    )
    print(output)
##__AXIOM_BLOCK_END__