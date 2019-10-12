from PIL import Image
import numpy as np
from encode_decode import *
import os

PATH_DATA = "../../ImageData"
PATH_MATRIX = "../../MatrixData"

def convert():
	if not os.path.isdir(PATH_MATRIX):
		os.mkdir(PATH_MATRIX)
	
	image_names = set('_'.join(name.split('_')[0:2]) for name in os.listdir(PATH_DATA))
	matrix_names = set(os.listdir(PATH_MATRIX))
	
	steps = dict()
	for f in os.listdir(PATH_DATA):
		name, uuid, tstep = f[:-4].split('_')
		fid = '_'.join([name, uuid])
		if fid not in steps:
			steps[fid] = []
		steps[fid].append(tstep)
		
		

	for nameuuid in set.difference(image_names, matrix_names):
		name, uuid = nameuuid.split('_')
		np_frame = np.zeros((150, 250, 400, 3))
		cnt = 0
		for step in sorted(steps['_'.join([name, uuid])]):
			namepng = f"{name}_{uuid}_{step}.png"
			im_frame = Image.open(os.path.join(PATH_DATA, namepng)).convert("RGB")
			np_frame[cnt] = np.array(im_frame.getdata()).reshape(250, 400, 3)
			cnt += 1
			
		np_frame = np.sum(np_frame, axis=2)/3
		
		np_frame[np_frame < 255] = 0
		np_frame /= 255
		np_frame = 1 - np_frame
		
		print(f"Saving matrix {name}_{uuid}")
		with open(os.path.join(PATH_MATRIX, name+'_'+uuid), 'w') as outfile:
			matrix_in = np_frame.tolist()
			matrix_out = encode(matrix_in)
			outfile.write(str(matrix_out))

if __name__ == '__main__':
	convert()
