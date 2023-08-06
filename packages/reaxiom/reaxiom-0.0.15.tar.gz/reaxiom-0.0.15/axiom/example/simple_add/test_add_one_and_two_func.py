from axiom.__data import main as __data
from axiom.__import import main as __import

int_3 = __data('axiom/example/int_3')
f = __import('axiom/example/int_add_one_and_two')

r1, r2 = f({}, int_3, given_name=['axiom/example/int_4', 'axiom/example/int_5'])
print('result', r1, r2)


