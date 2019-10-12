from keras.preprocessing.image import ImageDataGenerator
from Python import encode_decode

train_datagen = ImageDataGenerator(
		samplewise_center=True,
		rotation_range=20, # degrees
		width_shift_range=20, # px
		height_shift_range=20,
		zoom_range=0.2,
	)

def get_name(s):
	return s.split("_")[0]

def train_test_gen():
	for file in os.listdir("./img"):
		name = get_name(file)
		im = encode_decode.decode("./img/" + name)
		yield tuple(im, name)

for x, y in train_datagen.flow(*train_test_gen()):
	print(y)

'''
model.fit_generator(*train_datagen.flow(*train_test_gen()),
	epochs=1,
	validation_split=0.15,

	)
'''
