from flask import Flask, jsonify

import onnxruntime as rt
from numpy import array
import numpy as np

app = Flask(__name__)

x_input= array([21,34,55])

n_steps_in =3


x_input = x_input.reshape((1, n_steps_in))

input_data = np.array(x_input, dtype=np.float32)

sess = rt.InferenceSession("src/my_fibonacci_onnx_model.onnx")
input_name = sess.get_inputs()[0].name
output_name = sess.get_outputs()[0].name

pred_onx = sess.run([output_name], {input_name: input_data})
                     
print ('Predicted value from ONNX', pred_onx)

str_prediction_onnx = str(pred_onx)

@app.route('/')
def hello_world():
    return  str_prediction_onnx


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
