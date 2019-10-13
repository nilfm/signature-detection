from flask import Flask, jsonify
from flask_cors import CORS

import os
import tensorflow as tf
import json
import ftputil
from PIL import Image
from encode_decode import *
from keras.utils.np_utils import to_categorical # convert to one-hot-encoding
from keras.models import Model ,load_model
from keras.layers import TimeDistributed, Dense, Dropout, Flatten, LSTM, Conv2D, Conv3D, MaxPool2D, MaxPool3D, Input
from keras.optimizers import RMSprop
from keras.preprocessing.image import ImageDataGenerator

model = load_model('../../Models/model.h5')
num_photos = 0

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def dynamic_page():
    return predict()


'''
Guardarem les N imatges de la firma a la carpeta ../Predict
'''
def get_X():
	image_names = os.listdir('../../Predict')
	pages = []
	for name in image_names:
		im_frame = Image.open(os.path.join('../../Predict', name)).convert("RGB")
		np_frame = np.array(im_frame.getdata()).reshape(125, 200, 3)
		np_frame = np.sum(np_frame, axis=2)/3
		np_frame /= 255
		np_frame = 1-np_frame
		pages.append(np_frame)
	
	global num_photos
	num_photos = len(pages)
	while len(pages) < 20:
		pages.append(np.zeros((125, 200)))
	return np.array(pages).reshape(-1, 20, 125, 200, 1)
	

def predict():
	global num_photos
	X = get_X()
	
	with open('../../Models/classes.json', 'r') as infile:
		classes = json.load(infile)
	names = {v: k for k, v in classes.items()}

	with open('../../Models/stats.json', 'r') as infile:
		stats = json.load(infile)
		
	pred = model.predict(X)[0]
	winner = names[int(np.argmax(pred, axis=0))]
	prob = np.max(pred, axis=0)

	ret = {}
	ret['winner'] = winner
	ret['probs'] = str(pred.tolist())
	ret['names'] = names
	ret['maxprob'] = float(prob)
	ret['avgprop'] = stats[winner]
	ret['absdiff'] = stats[winner]-prob
	ret['reldiff'] = (stats[winner]-prob)/stats[winner]
	ret['numphotos'] = num_photos-1
	return jsonify(ret)

if __name__ == '__main__':
    app.run(host='192.168.43.36', port='8000', debug=True) #CANVIAR IP

