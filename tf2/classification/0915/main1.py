import tensorflow as tf
import numpy as np
new_model = tf.keras.models.load_model('tf1_no_smote_no_normal.h5')
record = np.array([[-0.075197596,0.093203514,0.375011389,-0.017456585,0.85573888,0.925443146],
[-0.075197596,0.093203514,0.375011389,-0.017456585,0.85573888,0.925443146]])
res = new_model.predict(record)
rel = res.argmax(axis=1)
print(rel)