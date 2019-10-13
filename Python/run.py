import image_to_matrix
import split_data
import os

PATH_IMGS = '../../ImageData/'
PATH_MATRIX = '../../MatrixData/'
PATH_TRAIN = '../../TrainData/'
PATH_VAL = '../../ValData/'

def main():
	for filename in os.listdir(PATH_TRAIN):
		os.remove(os.path.join(PATH_TRAIN, filename))
	for filename in os.listdir(PATH_VAL):
		os.remove(os.path.join(PATH_VAL, filename))
	
	image_to_matrix.convert()
	split_data.split_data()
	
	
if __name__ == '__main__':
	main()
