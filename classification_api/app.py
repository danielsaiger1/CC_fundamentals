from flask import Flask, request, jsonify
import tensorflow as tf
import cv2
import numpy as np

app = Flask(__name__)

model = tf.keras.applications.EfficientNetB0(weights='imagenet')

@app.route('/classify', methods=['POST'])
def classify_image():
    try:
        img_file = request.files['image']
        npimg = np.frombuffer(img_file.read(), np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({'error': 'Could not decode image'}), 400

        img_resized = cv2.resize(img, (224, 224))
        img_array = np.expand_dims(img_resized, axis=0)
        img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)

        preds = model.predict(img_array)
        decoded_preds = tf.keras.applications.efficientnet.decode_predictions(preds, top=1)[0][0]

        class_name = decoded_preds[1]
        class_prob = decoded_preds[2]

        prediction_result = {
            'class': class_name,
            'prob': f"{class_prob:.2f}"
        }

        return jsonify(prediction_result), 200

    except Exception as e:
        import traceback
        return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 500

# hallo