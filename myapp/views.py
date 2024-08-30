from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
import os
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render
import tensorflow as tf 
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

model = load_model('./savedModels/bellpeppermodel.keras')

#
def home(request):
    return render(request, 'myapp/home.html')

def fertilizer_calculator(request):
    return render(request, 'myapp/fertilizer-calculator.html')

def disease_diagnosis(request):
    return render(request, 'myapp/disease_diagnosis.html')

from django.http import JsonResponse
from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.applications.imagenet_utils import preprocess_input

# Load the pre-trained model
model = load_model('./savedModels/bellpeppermodel.keras')

# Preprocess the uploaded image
def preprocess_image(image_path):
    img = keras_image.load_img(image_path, target_size=(128, 128))  # Adjust target size as needed
    img_array = keras_image.img_to_array(img)
    img_array = preprocess_input(img_array)  # Preprocessing as per model requirement
    return img_array

# View for handling the image upload and prediction
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        uploaded_file_url = fs.url(filename)

        # Convert URL path to filesystem path
        file_path = fs.path(filename)
        
        # Preprocess the image
        preprocessed_image = preprocess_image(file_path)
        image_batch = np.expand_dims(preprocessed_image, axis=0)
        
        # Make prediction using the model
        prediction = model.predict(image_batch)
        predicted_class = np.argmax(prediction[0])
        
        # Define class names and remedies
        class_names = ['Healthy', 'Bacterial Infection']
        remedies = {
            'Healthy': 'No disease detected. Continue with regular care.',
            'Bacterial Infection': 'Use fungicides like chlorothalonil or copper-based products.'
        }
        
        predicted_label = class_names[predicted_class]
        remedy = remedies[predicted_label]

        # Return JSON response with the detected disease, remedy, and image URL
        response_data = {
            'result': predicted_label,
            'remedy': remedy,
            'image_url': uploaded_file_url
        }

        return JsonResponse(response_data)

    return render(request, 'myapp/disease_diagnosis.html')