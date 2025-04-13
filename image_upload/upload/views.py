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

model = tf.keras.applications.MobileNetV2()


def image_preprocess(image_array):
    return tf.keras.applications.mobilenet_v2.preprocess_input(image_array[tf.newaxis, ...])

def get_tags(probs, labels, max_classes=5, prob_threshold=0.01):
    probs_mask = probs > prob_threshold
    probs_filtered = probs[probs_mask] * 100
    labels_filtered = labels[probs_mask]
    
    sorted_index = np.flip(np.argsort(probs_filtered))
    labels_filtered = labels_filtered[sorted_index][:max_classes]
    probs_filtered = probs_filtered[sorted_index][:max_classes].astype(int)
    
    tags = ''
    for i in range(0, len(labels_filtered)):
        tags = tags + labels_filtered[i] + ' (' + str(probs_filtered[i]) + '%), ' 

    return tags, labels_filtered, probs_filtered


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

            # Vorverarbeitung des Bildes
            img_array = image_preprocess(img_array)

            # Vorhersage generieren
            result = model.predict(img_array)
            np_result = result[0]

            # Labels laden (kann auch aus einer Datei geladen werden)
            LABELS_URL = 'https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt'
            labels_path = tf.keras.utils.get_file('ImageNetLabels.txt', LABELS_URL)
            labels = np.array(open(labels_path).read().splitlines())[1:]

            # Tags extrahieren
            tags, labels_filtered, probs_filtered = get_tags(np_result, labels)

            # Zeige das Vorhersage-Ergebnis an
            prediction_result = {
                'tags': tags,
                'labels': labels_filtered,
                'probs': probs_filtered,
            }

    


    return render(request, 'upload/upload_image.html', {'image_path': image_name, 'form': form, 'prediction_result': prediction_result})