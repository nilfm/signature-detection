import numpy as np

def encode(matrix_in):
	matrix_out = []
	for row in matrix_in:
		last = 0
		count = 0
		cur_list = []
		for elem in row:
			if int(elem) == last:
				count += 1
			else:
				cur_list.append(count)
				count = 1
				last = 1-last
		cur_list.append(count)
		matrix_out.append(cur_list)
	return matrix_out

def decode(matrix_in):
	matrix_out = []
	for row in matrix_in:
		last = 0
		cur_row = []
		for elem in row:
			for i in range(elem):
				cur_row.append(last)
			last = 1-last
		matrix_out.append(cur_row)
	return np.array(matrix_out)
			
