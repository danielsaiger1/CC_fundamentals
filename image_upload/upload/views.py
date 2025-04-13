"""
View to upload image and classify it using MobileNetV2 model.
"""

from django.shortcuts import render
from django.conf import settings

import os
import numpy as np

import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array

from .forms import ImageUploadForm
from .classification import ImageClassifier

model = tf.keras.applications.MobileNetV2()

# Load Labels
LABELS_URL = 'https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt'
labels = ImageClassifier.get_labels(LABELS_URL)

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
            
            img = load_img(image_path, target_size=[224, 224])
            img_array = img_to_array(img, dtype=np.int32)

            img_array = ImageClassifier.image_preprocess(img_array)

            result = model.predict(img_array)
            np_result = result[0]

            labels_filtered, probs_filtered = ImageClassifier.get_tags(np_result, labels)

            prediction_result = {}
            for i in range(0, len(labels_filtered)):
                prediction_result[str(labels_filtered[i])] = int(probs_filtered[i])

    return render(request, 'upload/upload_image.html', {'image_path': image_name, 'form': form, 'prediction_result': prediction_result})