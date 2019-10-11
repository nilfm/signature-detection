from PIL import Image
import numpy as np
from encode_decode import *
import os

PATH_DATA = "../../ImageData"
PATH_MATRIX = "../../MatrixData"

def convert():
	image_names = set(name[:-4] for name in os.listdir(PATH_DATA))
	matrix_names = set(os.listdir(PATH_MATRIX))

	for name in set.difference(image_names, matrix_names):
		namepng = f"{name}.png"
		im_frame = Image.open(os.path.join(PATH_DATA, namepng)).convert("RGB")
		np_frame = np.array(im_frame.getdata()).reshape(250, 400, 3)
		np_frame = np.sum(np_frame, axis=2)/3
		
		np_frame[np_frame < 255] = 0
		np_frame /= 255
		np_frame = 1 - np_frame
		
		print(f"Saving matrix {name}")
		with open(os.path.join(PATH_MATRIX, name), 'w') as outfile:
			matrix_in = np_frame.tolist()
			matrix_out = encode(matrix_in)
			outfile.write(str(matrix_out))
