import base64
from PIL import Image
from flask import request, jsonify, Blueprint
from keras.models import load_model
import numpy as np
from img_processing import process_image
from skimage.color.colorconv import rgb2gray
import skimage
import io
from skimage.transform import resize

MODEL_PATH = '../models/color_model.h5'

predict_api = Blueprint('predict_api', __name__)
model = load_model(MODEL_PATH)
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])


@predict_api.route('/predict', methods=['POST'])
def predict():
    json = request.get_json()
    if json is None:
        return jsonify({"error": 'not json provided'})
    base64encoded_img = json.get('file')
    if base64encoded_img is None:
        return jsonify({"error": 'file not found'})
    img = base64.b64decode(base64encoded_img)
    img = load_image(img, as_gray=False)
    #img = skimage.img_as_float64(load_image(img))
    #img = process_image(img)
    img = resize(img, (128,128))
    #img = img / 255
    img = np.expand_dims(img, axis=0)

    probas = model.predict(img, None, 1, 1).tolist()[0]
    return jsonify(probas)

def load_image(img, as_gray=True):
    fo = io.BytesIO(img)
    img = skimage.io.call_plugin('imread', fo, plugin='pil', as_gray=as_gray)

    if not hasattr(img, 'ndim'):
        return img

    if img.ndim > 2:
        if img.shape[-1] not in (3, 4) and img.shape[-3] in (3, 4):
            img = np.swapaxes(img, -1, -3)
            img = np.swapaxes(img, -2, -3)

        if as_gray:
            img = rgb2gray(img)
    return img
