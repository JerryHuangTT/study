import tflite_runtime.interpreter as tflite
import numpy as np

interpreter = tflite.Interpreter(model_path="tflite_no_smote_no_normal.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def main(x_test,y_test):
    x_test = x_test.astype(np.float32)
    i = 0
    acc = 0 
    for x in x_test:
        x = x.reshape(x.shape[0],1).T
        y_infer = infer_once(x)

        y = y_test[i]
        y = y.reshape(y.shape[0],1).T
        y = y.argmax(axis=1).tolist()[0]
        if y_infer == y:
            acc += 1
        i += 1
    acc /= y_test.shape[0]   
    return acc

def infer_once(input):
    interpreter.set_tensor(input_details[0]['index'], input)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    res = output_data.argmax(axis=1).tolist()
    return res[0]