import os
import tensorflow as tf
import json
from encode_decode import *
from keras.utils.np_utils import to_categorical # convert to one-hot-encoding
from keras.models import Model
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D, Input
from keras.optimizers import RMSprop
from keras.preprocessing.image import ImageDataGenerator

PATH_MATRIX = '../../MatrixData'

# Lol
classes = dict((name, i) for i, name in enumerate(sorted(list(set(name.split('_')[0] for name in os.listdir(PATH_MATRIX))))))

def get_name(s):
	return s.split("_")[0]

augment_data = ImageDataGenerator(
	samplewise_center=True,
	rotation_range=20, # degrees
	width_shift_range=20, # px
	height_shift_range=20,
	zoom_range=0.2,
)


def train_test_gen():
	while True:
		for filename in os.listdir(PATH_MATRIX):
			name = get_name(filename)
			with open(os.path.join(PATH_MATRIX, filename), 'r') as infile:
				encoded = json.load(infile)
			im = decode(encoded)
			print("START")
			for transformed_im in augment_data.flow(im.reshape(1, 250, 400, 1)):
				yield transformed_im, classes[name]
			print("END")

def get_inputs():
	X = []
	y = []
	for filename in os.listdir(PATH_MATRIX):
		name = get_name(filename)
		with open(os.path.join(PATH_MATRIX, filename), 'r') as infile:
			encoded = json.load(infile)
		im = decode(encoded)
		X.append(im)
		y.append(classes[name])
	return np.array(X), np.array(y)		

X, y = get_inputs()
gen = augment_data.flow(x=X.reshape(*X.shape, 1), y=y)


inputs = Input(shape=(250, 400, 1))
hidden = Dense(64, activation='relu')(inputs)
outputs = Dense(len(classes))(hidden)

model = Model(inputs=inputs, outputs=outputs)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit_generator(
	gen,
	epochs=1
)

with open(os.path.join(PATH_MATRIX, 'andreu_1570830292'), 'r') as infile:
	X_test = decode(json.load(infile))
pred = model.predict(X_test.reshape(100000))
