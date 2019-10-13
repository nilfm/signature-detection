import numpy as np

def encode(matrix_in):
	matrix_out = []
	for page in matrix_in:
		page_out = []
		for row in page:
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
			page_out.append(cur_list)
		matrix_out.append(page_out)
	return matrix_out

def decode(matrix_in):
	matrix_out = []
	for page in matrix_in:
		page_out = []
		for row in page:
			last = 0
			cur_row = []
			for elem in row:
				for i in range(elem):
					cur_row.append(last)
				last = 1-last
			page_out.append(cur_row)
		matrix_out.append(page_out)
	return np.array(matrix_out)
			
