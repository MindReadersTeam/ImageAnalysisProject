import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Activation
from keras.layers import Conv2D, MaxPooling2D


class ModelFactory:
    def __init__(self, init_shape, num_classes):
        self.init_shape = init_shape
        self.num_classes = num_classes

    def get_modelo1(self):
        model = Sequential()
        model.add(Flatten(input_shape = self.init_shape))
        model.add(Dense(128, activation='relu'))
        model.add(Dense(182, activation='relu'))
        model.add(Dense(144, activation='relu')) 
        model.add(Dense(self.num_classes, activation='softmax'))
        return model

    def get_modelo2(self):
        model = Sequential()
        model.add(Flatten(input_shape = self.init_shape))
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.7))
        model.add(Dense(256, activation='relu'))
        model.add(Dropout(0.25))
        model.add(Dense(256, activation='relu')) 
        model.add(Dense(self.num_classes, activation='softmax'))
        return model

    def get_modelo3(self):
        model = Sequential()
        model.add(Conv2D(32, (3, 3), input_shape=self.init_shape))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        
        model.add(Conv2D(32, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.7))
        
        model.add(Conv2D(64, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.5))
        
        model.add(Flatten())
        model.add(Dense(256))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))
        model.add(Dense(self.num_classes, activation='softmax'))
        return model

