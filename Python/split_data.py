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
	
	users = os.listdir(PATH_DATA)
	
	for user in users:	
		files = os.listdir(os.path.join(PATH_DATA, user))	
		discrim = 0
		for f in files:
			if discrim < VAL_RATE:
				shutil.copyfile(os.path.join(PATH_DATA, user, f), os.path.join(PATH_VAL, f"{user}_{f}"))
			else:
				shutil.copyfile(os.path.join(PATH_DATA, user, f), os.path.join(PATH_TRAIN, f"{user}_{f}"))
			discrim = (discrim+VAL_RATE)%1

if __name__ == '__main__':
	split_data()
