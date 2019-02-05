import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
from keras.preprocessing.image import ImageDataGenerator
import models
from matplotlib import pyplot as plt

raw_data = "./imgs/raw"

batch_size = 32
num_classes = 10
epochs = 12
img_width, img_height = 128, 128

if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)

modelFactory = models.ModelFactory(input_shape, num_classes)
model = modelFactory.get_model2()

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer='adam',
              metrics=['accuracy'])

data_datagen = ImageDataGenerator(
    rescale=1. / 255,   
    rotation_range=5,
    validation_split=0.2
)

train_generator = data_datagen.flow_from_directory(
    raw_data,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    color_mode='rgb',
    subset='training'
)

validation_generator = data_datagen.flow_from_directory(
    raw_data,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    color_mode='rgb',
    subset='validation'
)

def show(i = 0):
    img = train_generator.next()[0][i]
    plt.imshow(img)
    plt.savefig("img")


model.summary()

history = model.fit_generator(
    train_generator,
    steps_per_epoch=train_generator.n // batch_size,
    validation_data=validation_generator,
    validation_steps=validation_generator.n // batch_size,
    epochs=epochs,
    verbose=2,
    use_multiprocessing=True
)

model.save('models/color_model.h5')

# Loss Curves
plt.figure(figsize=[8,6])
plt.plot(history.history['loss'],'r',linewidth=3.0)
plt.plot(history.history['val_loss'],'b',linewidth=3.0)
plt.legend(['Training loss', 'Validation Loss'],fontsize=18)
plt.xlabel('Epochs ',fontsize=16)
plt.ylabel('Loss',fontsize=16)
plt.title('Loss Curves',fontsize=16)

plt.savefig('loss.png')

# Accuracy Curves
plt.figure(figsize=[8,6])
plt.plot(history.history['acc'],'r',linewidth=3.0)
plt.plot(history.history['val_acc'],'b',linewidth=3.0)
plt.legend(['Training Accuracy', 'Validation Accuracy'],fontsize=18)
plt.xlabel('Epochs ',fontsize=16)
plt.ylabel('Accuracy',fontsize=16)
plt.title('Accuracy Curves',fontsize=16)

plt.savefig('accuracy.png')

