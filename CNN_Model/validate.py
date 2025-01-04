import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

img_width, img_height = 150, 150 

model = tf.keras.models.load_model('Voidex.h5')


def predict_diseases(image_path):
    image = tf.keras.preprocessing.image.load_img(image_path, target_size=(img_width, img_height))
    image = tf.keras.preprocessing.image.img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = image / 255.0

    prediction = model.predict(image)[0]
    disease_labels = ['Atelectasis', 'Brain_Tumor', 'Cardiomegaly', 'Consolidation', 'Edema', 'Effusion',
                      'Emphysema', 'Fibrosis', 'Hernia', 'Infiltration', 'Mass', 'No_Brain_Finding',
                      'No_Lung_Finding', 'Nodule', 'Pleural', 'Pneumonia', 'Pneumothorax', 'Tuberculosis']
    predicted_labels = [disease_labels[i] for i, p in enumerate(prediction) if p > 0.5]

    return predicted_labels


test_image_path = 'dataset/test/Nodule/testcase_X-014 (1).png'
predicted_diseases = predict_diseases(test_image_path)
print('Predicted Diseases:', predicted_diseases)
