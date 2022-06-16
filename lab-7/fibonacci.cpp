#include <stdio.h>
#include "tensorflow/lite/interpreter.h"

#include "tensorflow/lite/kernels/register.h"
#include "tensorflow/lite/model.h"
#include "tensorflow/lite/tools/gen_op_registration.h"
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


    // Resize input tensors, if desired.
    interpreter->AllocateTensors();
		
	
	float* input0 = interpreter->typed_input_tensor<float>(0)[0] ;
	float* input0 = interpreter->typed_input_tensor<float>(0)[1] ;
	float* input0 = interpreter->typed_input_tensor<float>(0)[2] ;
		
	# const std::vector<int> inputs = interpreter->inputs();
    #const std::vector<int> outputs = interpreter->outputs();
	
	

    //std::cout << "input " <<  inputs[0] << "\r\n";
    std::cout << "number of inputs " <<  interpreter->inputs().size() <<"\r\n";
    std::cout << "number of outputs " << interpreter->outputs().size() << "\r\n";
	
	std::cout << "input(0) name: " <<  interpreter->GetInputName(0) << "\r\n";
	std::cout << "input(1) name: " <<  interpreter->GetInputName(1) << "\r\n";
	std::cout << "input(2) name: " <<  interpreter->GetInputName(2) << "\r\n";
    	std::cout << "output(0) name: " << interpreter->GetOutputName(0) << "\r\n";
	std::cout << "output(1) name: " << interpreter->GetOutputName(1) << "\r\n";
	
		
    interpreter->Invoke();
	
    float* output0 = interpreter->typed_output_tensor<float>(0)[0];
	float* output1 = interpreter->typed_output_tensor<float>(0)[1];

    printf("Result is: %f\n", *output0);
	printf("Result is: %f\n", *output1);

    return 0;

}
