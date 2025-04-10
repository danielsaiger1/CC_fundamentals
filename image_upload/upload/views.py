from django.shortcuts import render
from django.http import JsonResponse
from .forms import ImageUploadForm
import os
from django.conf import settings

def upload_image(request):
    form = ImageUploadForm()
    image_name = None

    if request.method == 'POST' and request.FILES['image']:
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            image_name = image.name
            image_path = os.path.join(settings.MEDIA_ROOT, image_name)

        with open(image_path, 'wb+') as f:
            for chunk in image.chunks():
                f.write(chunk)

    return render(request, 'upload/upload_image.html', {'image_path': image_name, 'form': form})