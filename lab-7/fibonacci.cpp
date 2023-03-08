// The model takes 3 floating point inputs and provides two floating point outputs
// Verify this using Netron
// Compile model using $g++ fibonacci.cpp -o fibo -ltensorflow-lite -ldl

#include <iostream>
#include <tensorflow/lite/interpreter.h>
#include <tensorflow/lite/kernels/register.h>
#include <tensorflow/lite/model.h>
#include <iostream>

int main(){

    std::unique_ptr<tflite::FlatBufferModel> model = tflite::FlatBufferModel::BuildFromFile("fibonacci_1.tflite");

    if(!model){
        printf("Failed to mmap model\n");
        exit(0);
    }

    tflite::ops::builtin::BuiltinOpResolver resolver;
    std::unique_ptr<tflite::Interpreter> interpreter;
    tflite::InterpreterBuilder(*model.get(), resolver)(&interpreter);


    interpreter->AllocateTensors();
		
    float x[] = {34.0, 55.0, 89.0};
	
	
	float *inputTensor = interpreter->typed_input_tensor<float>(0);
	
			
	memcpy (inputTensor, x, sizeof(x));
	
    interpreter->Invoke();
	
    float *output0 = interpreter->typed_output_tensor<float>(0);
    

    printf("Result is: %f\n", output0[0]);
	printf("Result is: %f\n", output0[1]);

    return 0;

}
