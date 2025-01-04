import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from sklearn.metrics import classification_report, confusion_matrix


model = load_model('Voidex.h5')


class_names = [
    'Atelectasis', 'Brain_Tumor', 'Cardiomegaly', 'Consolidation', 'Edema',
    'Effusion', 'Emphysema', 'Fibrosis', 'Hernia', 'Infiltration', 'Mass',
    'No_Brain_Finding', 'No_Lung_Finding', 'Nodule', 'Pleural', 'Pneumonia',
    'Pneumothorax', 'Tuberculosis'
]


predictions = []
true_labels = []
image_names = []
images = []


for class_name in class_names:
    test_folder = os.path.join('dataset/test', class_name)
    for image_file in os.listdir(test_folder):
        image_path = os.path.join(test_folder, image_file)
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (150, 150)) 
        image = image / 255.0
        image = np.expand_dims(image, axis=0)

     
        prediction = model.predict(image)
        predicted_class_index = np.argmax(prediction)

       
        predictions.append(class_names[predicted_class_index])
        true_labels.append(class_name)
        image_names.append(image_file)
        images.append(image)


report = classification_report(true_labels, predictions, target_names=class_names)
confusion_mat = confusion_matrix(true_labels, predictions)


print("Classification Report:")
print(report)


print("Confusion Matrix:")
print(confusion_mat)

results_df = pd.DataFrame({
    'Image Name': image_names,
    'True Label': true_labels,
    'Predicted Label': predictions,
    'Image': images
})
results_df.to_csv('classification_results_one.csv', index=False)
