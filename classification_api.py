from flask import Flask, request, jsonify
from ultralytics import YOLO

app = Flask(__name__)
model = YOLO('yolo11n-cls.pt')


@app.route('/')
def hello_world():
    return '<p>Hello world</p>'

@app.route('/classify', methods=['POST'])
def classify_image():

    img = request.files['image']

    results = model(img)

    return jsonify(results)

if __name__ == '__main__':
    app.run()