from axiom.__data import main as __data
from axiom.__import import main as __import

int_3 = __data('axiom/example/int_3')
int_4 = __data('axiom/example/int_4')
add = __import('axiom/example/int_add')

add_one = __import('axiom/example/int_add_one')
add_one_and_two = __import('axiom/example/int_add_one_and_two')
add_by_config = __import('axiom/example/int_add_by_config')
result = add({}, [int_3, int_4], given_name='axiom/example/some_number_1')
r2 = add({}, [int_3, result], given_name='axiom/example/some_number_2')
r3 = add_one({}, r2, given_name='axiom/example/some_number_3')
r4, r5 = add_one_and_two({}, r3, given_name=['axiom/example/a', 'axiom/example/b'])
r6 = add_by_config({'n':2}, r5, given_name='axiom/example/c')

