import tensorflow as tf
import numpy as np

def main(data):
    model = tf.keras.models.load_model('tf1_no_smote_no_normal.h5',compile=False)
    record = np.array(data)
    res = model.predict(record)
    rel = res.argmax(axis=1).tolist()
    return rel