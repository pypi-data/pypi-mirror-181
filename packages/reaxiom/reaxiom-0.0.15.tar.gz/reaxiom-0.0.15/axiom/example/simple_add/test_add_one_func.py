from axiom.__data import main as __data
from axiom.__import import main as __import

int_3 = __data('axiom/example/int_3')
add_one = __import('axiom/example/int_add_one')

result = add_one({}, int_3, given_names='axiom/example/int_4')

print('result', result)
