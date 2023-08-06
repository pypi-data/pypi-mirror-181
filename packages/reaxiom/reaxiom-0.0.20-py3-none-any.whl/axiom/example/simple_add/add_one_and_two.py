##__AXIOM_BLOCK_BEGIN__
block_info = {
    "type": "function",
    "given_name": "axiom/example/int_add_one_and_two",
    "input": "data.int",
    "output": ["data.int", "data.int"],
    "axiom_name": "__AXIOM__",
    "description": "add input by one and two"
}
##__AXIOM_INFO_END__
import os

def int_reader(folder):
    return int(open(os.path.join(folder, 'value')).read())

def int_writer(folder, value):
    assert isinstance(value, int)
    open(os.path.join(folder, 'value'), 'w').write(str(value))

def main(config, in_folder, given_names, out_folder):
    value1 = int_reader(in_folder)
    int_writer(out_folder[0], value1+1)
    value2 = int_reader(in_folder)
    int_writer(out_folder[1], value2+2)
    return out_folder

##__AXIOM_FUNCTION_END__


if __name__ == '__main__':
    out_folder = ['/tmp/tmp/a', '/tmp/tmp/b']
    data = '/Users/test/reaxiom/cache/eccbc87e4b5ce2fe28308fd9f2a7baf3/obj'
    main(
        config={},
        in_folder=data,
        given_names=['axiom/example/int_4_2', 'axiom/example/int_5'],
        out_folder=out_folder
    )
##__AXIOM_BLOCK_END__