from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import io
import pymongo
import base64

app = Flask(__name__)
model = load_model("Voidex.h5")
client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client['CES']
collection = db['ML']

class_labels = [
    "Atelectasis", "Brain_Tumor", "Cardiomegaly", "Consolidation", "Edema", "Effusion",
    "Emphysema", "Fibrosis", "Hernia", "Infiltration", "Mass", "No_Brain_Finding",
    "No_Lung_Finding", "Nodule", "Pleural", "Pneumonia", "Pneumothorax", "Tuberculosis"
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/classify", methods=["POST"])
def classify():
    image_file = request.files["image"]
    img = image.load_img(io.BytesIO(image_file.read()), target_size=(150, 150))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = img / 255.0

    predictions = model.predict(img)
    predicted_class_index = np.argmax(predictions[0])
    predicted_class = class_labels[predicted_class_index]
    print(img)

    # dictionary={
    #     '_id':1 ,
    #     'image_data':img
    # }

    # if image_file:
    #     base64_string = image_file.read().encode('base64').replace('\n', '')  # Convert image to base64
    #     # Save the base64_string to your database along with other patient information
    #     print('Base64 image string:', base64_string)
    #     return "Image processed successfully!"
    # else:
    #     return "No image file received."

    # collection.insert_one(dictionary)

    return predicted_class


if __name__ == "__main__":
    app.run(debug=True)


