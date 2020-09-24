import datetime as dt
print('start import\t{}'.format(dt.datetime.now()))
import tflite_runtime.interpreter as tflite
import numpy as np

input_data = np.array([[-0.075197596,0.093203514,0.375011389,-0.017456585,0.85573888,0.925443146]],dtype=np.float32)
#[-0.075197596,0.093203514,0.375011389,-0.017456585,0.85573888,0.925443146]],dtype=np.float32)
print('start load\t{}'.format(dt.datetime.now()))
interpreter = tflite.Interpreter(model_path="greengrass\\train\\tflite_no_smote_no_normal.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

interpreter.set_tensor(input_details[0]['index'], input_data)
print('start infer\t{}'.format(dt.datetime.now()))
interpreter.invoke()
print('end infer\t{}'.format(dt.datetime.now()))

output_data = interpreter.get_tensor(output_details[0]['index'])
res = output_data.argmax(axis=1).tolist()
print(res)