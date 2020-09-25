import tflite_runtime.interpreter as tflite
import numpy as np

def main(data):
    input_data = np.array(data,dtype=np.float32)
    interpreter = tflite.Interpreter(model_path="tflite_no_smote_no_normal.tflite")
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])
    res = output_data.argmax(axis=1).tolist()
    return res[0]