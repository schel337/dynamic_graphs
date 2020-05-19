import numpy as np

def parse_matrix(matrix_string):
	"""
	Given inputs of the form a, b, c, ... ; x, y, z, ... ; ...
	Return np array
	"""
	rows = matrix_string.split(';')
	if len(rows) == 1:
		return parse_vector(rows[0])
	return np.array([[float(x) for x in row.split(',')] for row in rows])
	
def parse_vector(vector_string):
	"""
	Given inputs of the form a, b, c, ...
	Return np array
	"""
	return np.array([float(x) for x in vector_string.split(',')])