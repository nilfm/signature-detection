import shutil
import os

PATH_DATA = "../../MatrixData/"
PATH_TRAIN = "../../TrainData/"
PATH_VAL = "../../ValData/"

VAL_RATE = .15

def split_data():
	if not os.path.isdir(PATH_TRAIN):
		os.mkdir(PATH_TRAIN)
	if not os.path.isdir(PATH_VAL):
		os.mkdir(PATH_VAL)
	
	files = os.listdir(PATH_DATA)
	classes = dict((name, []) for i, name in enumerate(sorted(list(set(name.split('_')[0] for name in os.listdir(PATH_DATA))))))
	
	for f in files:
		classes[f.split('_')[0]].append(f)
		
	discrim = 0
	for c, files in classes.items():
		for f in files:
			if discrim < VAL_RATE:
				shutil.copyfile(os.path.join(PATH_DATA, f), os.path.join(PATH_VAL, f))
			else:
				shutil.copy(os.path.join(PATH_DATA, f), os.path.join(PATH_TRAIN, f))
			discrim = (discrim+VAL_RATE)%1

if __name__ == '__main__':
	split_data()
