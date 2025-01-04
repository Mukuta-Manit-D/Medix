import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense


dataset_path = 'dataset/'

img_width, img_height = 150, 150

batch_size = 48
epochs = 30

model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(img_width, img_height, 3)))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(18, activation='sigmoid'))  


model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

datagen = ImageDataGenerator(rescale=1.0/255.0)

train_generator = datagen.flow_from_directory(
    dataset_path + '/train',
    target_size=(img_width, img_height),
    batch_size=batch_size,
    classes=['Atelectasis', 'Brain_Tumor', 'Cardiomegaly', 'Consolidation', 'Edema', 'Effusion',
             'Emphysema', 'Fibrosis', 'Hernia', 'Infiltration', 'Mass', 'No_Brain_Finding',
             'No_Lung_Finding', 'Nodule', 'Pleural', 'Pneumonia', 'Pneumothorax', 'Tuberculosis'],
    class_mode='categorical'
    )

validation_generator = datagen.flow_from_directory(
    dataset_path + '/validation',
    target_size=(img_width, img_height),
    batch_size=batch_size,
    classes=['Atelectasis', 'Brain_Tumor', 'Cardiomegaly', 'Consolidation', 'Edema', 'Effusion',
             'Emphysema', 'Fibrosis', 'Hernia', 'Infiltration', 'Mass', 'No_Brain_Finding',
             'No_Lung_Finding', 'Nodule', 'Pleural', 'Pneumonia', 'Pneumothorax', 'Tuberculosis'],
    class_mode='categorical'
    )

model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // batch_size)

model.save('Voidex.h5')


