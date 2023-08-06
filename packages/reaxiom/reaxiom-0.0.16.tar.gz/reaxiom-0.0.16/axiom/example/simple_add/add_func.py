##__AXIOM_BLOCK_BEGIN__
block_info = {
    "type": "function",
    "given_name": "axiom/example/int_add",
    "input": ["data.int","data.int"],
    "output": "data.int",
    "axiom_name": "__AXIOM__",
    "description": "add two integers"
}


##__AXIOM_INFO_END__
import os

def int_reader(folder):
    return int(open(os.path.join(folder, 'value')).read())

def int_writer(folder, value):
    assert isinstance(value, int)
    open(os.path.join(folder, 'value'), 'w').write(str(value))

def main(config, in_folder, given_name, out_folder):
    assert len(in_folder) == 2
    value1 = int_reader(in_folder[0])
    value2 = int_reader(in_folder[1])
    int_writer(out_folder, value1+value2)
    return out_folder

##__AXIOM_FUNCTION_END__


if __name__ == '__main__':
    out_folder = '/tmp/tmp/a'
    data1 = '/Users/test/reaxiom/cache/eccbc87e4b5ce2fe28308fd9f2a7baf3/obj'
    data2 = '/Users/test/reaxiom/cache/e4da3b7fbbce2345d7772b0674a318d5/obj'
    
    output = main(
        config={},
        in_folder=[data1, data2],
        given_name = 'axiom/example/int_some_number_1',
        out_folder = out_folder
    )
    print(output)
##__AXIOM_BLOCK_END__