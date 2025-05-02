from flask import Flask, request, jsonify
from ultralytics import YOLO
import cv2
import numpy as np

app = Flask(__name__)
model = YOLO('yolo11n-cls.pt')

@app.route('/classify', methods=['POST'])
def classify_image():
    try:
        img_file = request.files['image']
        npimg = np.frombuffer(img_file.read(), np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({'error': 'Could not decode image'}), 400

        results = model.predict(source=img)
        result = results[0]

        top1_idx = result.probs.top1
        top1_conf = result.probs.top1conf

        class_name = model.names[top1_idx]

        prediction_result = {
            'class': class_name,
            'prob': f"{top1_conf:.2f}"
        }

        return jsonify(prediction_result), 200

    except Exception as e:
        import traceback
        return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 500



if __name__ == '__main__':
    app.run(port=5001)
