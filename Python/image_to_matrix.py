from PIL import Image
import numpy as np
from encode_decode import *
import os

PATH_DATA = "../../ImageData"
PATH_MATRIX = "../../MatrixData"

def convert():
	if not os.path.isdir(PATH_MATRIX):
		os.mkdir(PATH_MATRIX)
	
	image_names = set(os.listdir(PATH_DATA))
	matrix_names = set(os.listdir(PATH_MATRIX))
	
	for name in set.difference(image_names, matrix_names):
		if not os.path.exists(os.path.join(PATH_MATRIX, name)):
			os.mkdir(os.path.join(PATH_MATRIX, name))
		for dir_name in os.listdir(os.path.join(PATH_DATA, name)):
			pages = []
			for file_name in os.listdir(os.path.join(PATH_DATA, name, dir_name)):
				im_frame = Image.open(os.path.join(PATH_DATA, name, dir_name, file_name)).convert("RGB")
				np_frame = np.array(im_frame.getdata()).reshape(125, 200, 3)
				np_frame = np.sum(np_frame, axis=2)/3
				np_frame[np_frame < 255] = 0
				np_frame /= 255
				np_frame = 1 - np_frame
				pages.append(np_frame)	
			while len(pages) < 20:
				pages.append(np.zeros((125, 200)))
			np_pages = np.array(pages)
			print(f"Saving matrix {name}_{dir_name}")
			with open(os.path.join(PATH_MATRIX, name, dir_name), 'w') as outfile:
				matrix_in = np_pages.tolist()
				matrix_out = encode(matrix_in)
				outfile.write(str(matrix_out))
	

if __name__ == '__main__':
	convert()
