"""
View to upload image and classify it using MobileNetV2 model.
"""

from django.shortcuts import render
from django.conf import settings

import os
import requests

from .forms import ImageUploadForm

def upload_image(request):
    form = ImageUploadForm()
    image_name = None
    prediction_result_flask = None
    url = 'http://localhost:5000/classify'

    if request.method == 'POST' and request.FILES['image']:
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            image_name = image.name
            image_path = os.path.join(settings.MEDIA_ROOT, image_name)

        with open(image_path, 'wb+') as f:
            for chunk in image.chunks():
                f.write(chunk)

        with open(image_path, 'rb') as img_file:
            files = {'image': img_file}
            flask_response = requests.post(url, files=files)
            prediction_result_flask = flask_response.json()
            print(f"RESULT: {prediction_result_flask}")

    return render(request, 'upload/upload_image.html', {'image_path': image_name, 'form': form, 'flask_response': prediction_result_flask})
