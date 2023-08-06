import os
import numpy as np

def int_reader(folder):
    return int(open(os.path.join(folder, 'value')).read())

def float_reader(folder):
    return float(open(os.path.join(folder, 'value')).read())

def two_d_matrix_reader(folder):
    A = np.load('A.npy')
    columns = None
    rows = None
    columns_file = os.path.join(folder, 'columns')
    rows_file = os.path.join(folder, 'rows')
    if os.path.exists(columns_file):
        columns = open(columns_file).read().strip().split('\n')
    if os.path.exists(rows_file):
        rows = open(rows_file).read().strip().split('\n')
    return {'A': A, 'rows': rows, 'columns': columns}

data_types_readers = {
    'int': int_reader,
    'float': float_reader,
    '2d-matrix': two_d_matrix_reader
}