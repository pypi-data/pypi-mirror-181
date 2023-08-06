from axiom.__data import main as __data
from axiom.__import import main as __import

int_3 = __data('axiom/example/int_3')
int_5 = __data('axiom/example/int_5')
f = __import('axiom/example/int_add')

result = f({}, [int_3, int_5], given_name='axiom/example/some_number_1')
print('result', result)


