import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
from keras.preprocessing.image import ImageDataGenerator
import models

train_data = "./imgs/splitted/train"
validation_data = "./imgs/splitted/validation"

types = [
    'like',
    'dislike',
    'fist',
    'victory',
    'ok',
    'c_letter',
    'w_letter',
    'number_5',
    'hook',
    'call_me'
]

batch_size = 2
num_classes = 10
epochs = 12
img_width, img_height = 640, 640

if K.image_data_format() == 'channels_first':
    input_shape = (1, img_width, img_height)
else:
    input_shape = (img_width, img_height, 1)

modelFactory = models.ModelFactory(input_shape, num_classes)
model = modelFactory.get_model2()

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])

train_datagen = ImageDataGenerator(rescale=1. / 255)
test_datagen = ImageDataGenerator(rescale=1. / 255)

train_generator = train_datagen.flow_from_directory(
    train_data,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    color_mode='grayscale'
)

validation_generator = test_datagen.flow_from_directory(
    validation_data,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    color_mode='grayscale'
)

model.fit_generator(
    train_generator,
    steps_per_epoch=4000 // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=2000 // batch_size,
    verbose=2
    #use_multiprocessing=True
)

model.save_weights('first_try.h5')


# score = model.evaluate(x_test, y_test, verbose=0)
# print('Test loss:', score[0])
# print('Test accuracy:', score[1])

