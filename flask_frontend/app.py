from flask import Flask, render_template, request, redirect, url_for
import os
import requests
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    image_name = None
    prediction_result_flask = None
    flask_classifier_url = 'http://localhost:5000/classify' 

    if request.method == 'POST':
        if 'image' not in request.files:
            return "Kein Bild hochgeladen", 400

        file = request.files['image']
        if file.filename == '':
            return "Dateiname leer", 400

        if file:
            filename = secure_filename(file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)

            with open(image_path, 'rb') as img_file:
                files = {'image': img_file}
                response = requests.post(flask_classifier_url, files=files)
                prediction_result_flask = response.json()
                print("RESULT:", prediction_result_flask)

            image_name = filename

    return render_template('index.html', image_path=image_name, flask_response=prediction_result_flask)

# if __name__ == '__main__':
#     app.run(debug=True, port=8080)