import os
import tensorflow as tf
import json
import ftputil
import matplotlib.pyplot as plt
from encode_decode import *
from keras.utils.np_utils import to_categorical # convert to one-hot-encoding
from keras.models import Model
from keras.layers import TimeDistributed, Dense, Dropout, Flatten, LSTM, Conv2D, Conv3D, MaxPool2D, MaxPool3D, Input
from keras.optimizers import RMSprop
from keras.preprocessing.image import ImageDataGenerator

PATH_TRAIN = '../../TrainData'
PATH_VAL = '../../ValData'
PATH_MODEL = '../../Models/model.h5'

# Lol
classes = dict((name, i) for i, name in enumerate(sorted(list(set(name.split('_')[0] for name in os.listdir(PATH_TRAIN))))))
print(classes)

def get_name(s):
	return s.split("_")[0]

image_gen = ImageDataGenerator(
	samplewise_center=True,
	rotation_range=20, # degrees
	width_shift_range=20, # px
	height_shift_range=20,
	zoom_range=0.2,
)

def get_inputs(path):
	while True:
		for filename in os.listdir(path):
			name = get_name(filename)
			with open(os.path.join(path, filename), 'r') as infile:
				encoded = json.load(infile)
			im = decode(encoded)
			X = im.reshape(-1, 20, 125, 200, 1)
			y = to_categorical(classes[name], num_classes=len(classes))
			yield X, y.reshape(1, len(classes))

def get_model():
	inputs = Input(shape=(20, 125, 200, 1))
	
	conv = TimeDistributed(Conv2D(filters=32, kernel_size=(5, 5), padding='Valid', activation='relu'))(inputs)
	pool = TimeDistributed(MaxPool2D(pool_size=(2, 2)))(conv)
	
	conv = TimeDistributed(Conv2D(filters=32, kernel_size=(5, 5), padding='Valid', activation='relu'))(pool)
	pool = TimeDistributed(MaxPool2D(pool_size=(2, 2)))(conv)
		
	flat = Flatten()(pool)
	hidden = Dense(32, activation='relu')(flat)
	outputs = Dense(len(classes), activation='softmax')(hidden)

	model = Model(inputs=inputs, outputs=outputs)
	return model

def train():	
	num_train = len(os.listdir(PATH_TRAIN))
	num_val = len(os.listdir(PATH_VAL))	

	model = get_model()
	
	model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
	model.fit_generator(
		get_inputs(PATH_TRAIN),
		steps_per_epoch=num_train,
		epochs=3,
		validation_data=get_inputs(PATH_VAL),
		validation_steps=num_val
	)
	
	if not os.path.isdir('../../Models'):
		os.mkdir('../../Models')
	print('Saving model')
	model.save(PATH_MODEL)
	

	print('Saving classes')
	with open('../../Models/classes.json', 'w') as outfile:
		json.dump(classes, outfile, indent=2)
	
	print('Saving stats')
	names = {v: k for k, v in classes.items()}
	stats = {name: {'sum': 0, 'cnt': 0} for name in classes}

	i = 0
	for X, y in get_inputs(PATH_VAL):
		if i%10 == 0:
			print(f"Validation: {i}/{num_val}")
		name = names[int(np.argmax(y, axis=1))]
		num = np.argmax(y, axis=1)
		y_pred = model.predict(X)
		stats[name]['sum'] += y_pred[0][num]
		stats[name]['cnt'] += 1
		i += 1
		if i >= num_val:
			break
			
	for name in stats:
		stats[name] = float(stats[name]['sum']/stats[name]['cnt'])
		
	with open('../../Models/stats.json', 'w') as outfile:
		json.dump(stats, outfile, indent=2)	


if __name__ == '__main__':
	train()
