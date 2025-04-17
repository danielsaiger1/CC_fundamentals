"""
View to upload image and classify it using MobileNetV2 model.
"""

from django.shortcuts import render
from django.conf import settings

import os

from ultralytics import YOLO

from .forms import ImageUploadForm
from .classification import ImageClassifier

model = YOLO('yolo11n-cls.pt')

def upload_image(request):
    form = ImageUploadForm()
    image_name = None
    prediction_result = None

    if request.method == 'POST' and request.FILES['image']:
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            image_name = image.name
            image_path = os.path.join(settings.MEDIA_ROOT, image_name)

        with open(image_path, 'wb+') as f:
            for chunk in image.chunks():
                f.write(chunk)

        results = model(image_path)
        for result in results:
            prediction_result = {
                'class' : f"{result.names[result.probs.top1]}",
                'prob' : f"{result.probs.top1conf:.2f}"
            }        

    return render(request, 'upload/upload_image.html', {'image_path': image_name, 'form': form, 'prediction_result': prediction_result})