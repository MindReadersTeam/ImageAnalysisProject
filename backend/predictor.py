from keras.models import load_model
from img_processing import *
import numpy as np
import sys
import keras
from keras.preprocessing.image import ImageDataGenerator

def main(name, input_path):
    model = load_model(name)

    model.compile(loss='binary_crossentropy',
                  optimizer='adadelta',
                  metrics=['accuracy'])

    img = load_image(input_path)
    img = process_image(img)
    img = np.expand_dims(img, axis=2)
    img = np.expand_dims(img, axis=0)
    
    probas = model.predict(img, None, 1, 1)
    np.set_printoptions(precision=3, suppress=True)
    print(probas)
    print(probas.argmax())

if __name__=='__main__':
    mname = sys.argv[1]
    path = sys.argv[2]
    
    main(mname, path)
