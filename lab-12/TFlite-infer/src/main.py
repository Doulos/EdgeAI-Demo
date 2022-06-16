from flask import Flask, jsonify

import tflite_runtime.interpreter as tflite
import numpy as np
from numpy import array

interpreter = tflite.Interpreter(model_path=str('src/fibonacci_1.tflite'))

interpreter.allocate_tensors()

x_input= array([21,34,55])

n_steps_in =3

x_input = x_input.reshape((1, n_steps_in))

input_data = np.array(x_input, dtype=np.float32)

input_index = interpreter.get_input_details()[0]["index"]
output_index = interpreter.get_output_details()[0]["index"]

print ('Input Data', input_data)

interpreter.set_tensor(input_index, input_data)
interpreter.invoke()


prediction= str (interpreter.get_tensor(output_index))
print ('Predicted value from TFLite is',prediction)


app = Flask(__name__)


@app.route('/')
def hello_world():
    return '{}{}{}'.format('Predicted value',prediction, '\n')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
