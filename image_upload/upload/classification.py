import tensorflow as tf
import numpy as np


model = tf.keras.applications.MobileNetV2()

class ImageClassifier():
    def __init__(self, model):
        self.model = model

    def image_preprocess(image_array):
        return tf.keras.applications.mobilenet_v2.preprocess_input(image_array[tf.newaxis, ...])
    
    def get_labels(url):
        labels_path = tf.keras.utils.get_file('ImageNetLabels.txt', url)
        labels = np.array(
            open(labels_path).read().splitlines()
        )[1:]

        return labels

    def get_tags(probs, labels, max_classes=5, prob_threshold=0.01):
        probs_mask = probs > prob_threshold
        probs_filtered = probs[probs_mask] * 100
        labels_filtered = labels[probs_mask]
        
        sorted_index = np.flip(np.argsort(probs_filtered))
        labels_filtered = labels_filtered[sorted_index][:max_classes]
        probs_filtered = probs_filtered[sorted_index][:max_classes].astype(int)

        return labels_filtered, probs_filtered

