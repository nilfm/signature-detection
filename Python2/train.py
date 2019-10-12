import os
import tensorflow as tf
import json
import matplotlib.pyplot as plt
from encode_decode import *
from keras.utils.np_utils import to_categorical # convert to one-hot-encoding
from keras.models import Model
from keras.layers import Dense, Dropout, Flatten, Conv2D, Conv3D, MaxPool2D, Input
from keras.optimizers import RMSprop
from keras.preprocessing.image import ImageDataGenerator

PATH_TRAIN = '../../TrainData'
PATH_VAL = '../../ValData'

# Lol
classes = dict((name, i) for i, name in enumerate(sorted(list(set(name.split('_')[0] for name in os.listdir(PATH_TRAIN))))))

def get_name(s):
	return s.split("_")[0]

augment_data = ImageDataGenerator(
	samplewise_center=True,
	rotation_range=20, # degrees
	width_shift_range=20, # px
	height_shift_range=20,
	zoom_range=0.2,
)

def get_inputs(path):
	X = []
	y = []
	for filename in os.listdir(path):
		name = get_name(filename)
		with open(os.path.join(path, filename), 'r') as infile:
			encoded = json.load(infile)
		im = decode(encoded)
		X.append(im)
		y.append(to_categorical(classes[name], num_classes=len(classes)))
	return np.array(X), np.array(y)		

def get_model():
	inputs = Input(shape=(250, 400, 1))
	
	conv = Conv3D(filters=32, kernel_size=(5, 5, 5), padding='Same',
		activation='relu')(inputs)
	#pooled = MaxPool2D(pool_size=(2, 2))(conv)
	
	flat = Flatten()(conv)
	hidden = Dense(64, activation='relu')(flat)
	outputs = Dense(len(classes), activation='softmax')(hidden)

	model = Model(inputs=inputs, outputs=outputs)
	return model

def train():
	X, y = get_inputs(PATH_TRAIN)
	gen = augment_data.flow(x=X.reshape(*X.shape, 1), y=y)

	Xval, yval = get_inputs(PATH_VAL)
	
	model = get_model()

	model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
	model.fit_generator(
		gen,
		steps_per_epoch=10,
		epochs=10,
		validation_data=(Xval.reshape(-1, 250, 400, 1), yval)
	)


if __name__ == '__main__':
	train()
