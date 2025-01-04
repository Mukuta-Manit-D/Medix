import io
import base64
import numpy as np
from datetime import date
from pymongo import MongoClient
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import Flask, render_template, request

# Flask
app = Flask(__name__)

# model
model = load_model("Voidex.h5")

# db
client = MongoClient("mongodb://localhost:27017/")
db = client["Medix"]
collection = db["patients"]

class_labels = [
    "Atelectasis",
    "Brain_Tumor",
    "Cardiomegaly",
    "Consolidation",
    "Edema",
    "Effusion",
    "Emphysema",
    "Fibrosis",
    "Hernia",
    "Infiltration",
    "Mass",
    "No_Brain_Finding",
    "No_Lung_Finding",
    "Nodule",
    "Pleural",
    "Pneumonia",
    "Pneumothorax",
    "Tuberculosis",
]


@app.route("/")
def homepage():  # Function name and the url_for name should be same
    return render_template("homepage.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/report")
def report():
    return render_template("report.html")


@app.route("/submit", methods=["POST"])
def submit_image():
    if request.method == "POST":
        image_file = request.files["image"]
        img = image.load_img(io.BytesIO(image_file.read()), target_size=(150, 150))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = img / 255.0

        predictions = model.predict(img)
        predicted_class_index = np.argmax(predictions[0])
        predicted_class = class_labels[predicted_class_index]
        return predicted_class


@app.route("/save", methods=["POST"])
def save_image():
    if request.method == "POST":
        image_file = request.files["image"]
        if image_file:
            image_data = image_file.read()
            encoded_image = base64.b64encode(image_data).decode("utf-8")

        patient_id = request.form.get("patient_id")
        patient_name = request.form.get("patient_name")
        result = request.form.get("result")

        current_date = (date.today()).strftime("%Y-%m-%d")

        dictionary = {
            "_id": {"patient_id": patient_id, "date": current_date},
            "patient_id": patient_id,
            "patient_name": patient_name,
            "date": current_date,
            "symptoms": result,
            "image": encoded_image,
        }

        existing_data = collection.find_one(
            {"_id": {"patient_id": patient_id, "date": current_date}}
        )

        if existing_data:
            collection.update_one(
                {"_id": {"patient_id": patient_id, "date": current_date}},
                {
                    "$set": {
                        "patient_id": patient_id,
                        "patient_name": patient_name,
                        "date": current_date,
                        "symptoms": result,
                        "image": encoded_image,
                    }
                },
            )
            return "Data Updated Successfully"

        elif not existing_data:
            dictionary = {
                "_id": {"patient_id": patient_id, "date": current_date},
                "patient_id": patient_id,
                "patient_name": patient_name,
                "date": current_date,
                "symptoms": result,
                "image": encoded_image,
            }

            collection.insert_one(dictionary)
            return "Data Logged Successfully"
        
        else:
            return "Something Went Wrong"


@app.route("/report_analysis", methods=["GET", "POST"])
def report_analysis():
    error_message = None  # Initialize the error message

    if request.method == "POST":
        pid = request.form["patient_id"]
        date_req = request.form["calendarDate"]
        print(date_req)

        required_one = {
            "_id": {"patient_id": pid, "date": date_req},
        }

        data = collection.find_one(required_one)

        if data:
            patientid = data["patient_id"]
            patientname = data["patient_name"]
            patientsymptoms = data["symptoms"]
            encoded_image = data["image"]
            decoded_image = base64.b64decode(encoded_image)
            image_file = base64.b64encode(decoded_image).decode("utf-8")

            return render_template(
                "report.html",
                image=image_file,
                patient_id=patientid,
                patient_name=patientname,
                symptoms=patientsymptoms,
            )
        else:
            error_message = "Data not found"

    return render_template(
        "report.html",
        image=None,
        patient_id=None,
        patient_name=None,
        symptoms=None,
        error=error_message,
    )


if __name__ == "__main__":
    app.run(debug=True)
