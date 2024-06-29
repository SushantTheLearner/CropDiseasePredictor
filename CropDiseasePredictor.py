import os
import numpy as np
import cv2
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


# Function to extract image features
def extract_image_features(image_path):
    image = cv2.imread(image_path)
    newSize_image = cv2.resize(image, (100, 100))
    color_intensity = np.mean(newSize_image, axis=(0, 1))
    return color_intensity


# Mock model class for classification
class SampleModel:
    def predict(self, X):
        if X[0][0] > 100:
            return ["diseased"]
        else:
            return ["healthy"]

    def Pre_probabilities(self, X):
        if X[0][0] > 100:
            return [[0.1, 0.9]]
        else:
            return [[0.9, 0.1]]


# Function to load and predict the image
def load_and_predict_image():
    global img_label, result_label

    image_file_path = os.path.join(os.getcwd(), "newCropImage.png")

    if not os.path.isfile(image_file_path):
        messagebox.showerror("Error", "Image file not found")
        return

    image_features = extract_image_features(image_file_path)
    image_features = image_features.reshape(1, -1)

    model = SampleModel()
    predicted_label = model.predict(image_features)
    predicted_probabilities = model.Pre_probabilities(image_features)

    img = Image.open(image_file_path)
    img = img.resize((200, 200), Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)

    img_label.configure(image=img_tk)
    img_label.image = img_tk

    if predicted_label[0] !="healthy":
        result_label.configure(text="The crop is diseased. Predicted disease:")
    else:
        disease_types = ["Leaf Spot"]
        predicted_disease = disease_types[np.argmax(predicted_probabilities)]
        result_label.configure(text=f"The crop is diseased. Predicted disease: {predicted_disease}")


# Initialize the GUI
root = tk.Tk()
root.title("Crop Disease Identifier")
root.geometry("400x400")

instruction_label = tk.Label(root, text="Crop Disease Identifier", font=("Arial", 16))
instruction_label.pack(pady=10)

img_label = tk.Label(root)
img_label.pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 14))
result_label.pack(pady=10)

load_button = tk.Button(root, text="Load and Predict Image", command=load_and_predict_image)
load_button.pack(pady=10)

root.mainloop()