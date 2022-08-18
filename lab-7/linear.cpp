#include <iostream>
#include <tensorflow/lite/interpreter.h>
#include <tensorflow/lite/kernels/register.h>

using namespace tflite;

int main()
{
    int numThreads = 4;

    std::unique_ptr<FlatBufferModel> model = FlatBufferModel::BuildFromFile("linear.tflite");

    ops::builtin::BuiltinOpResolver resolver;
    std::unique_ptr<Interpreter> interpreter;
    InterpreterBuilder(*model, resolver)(&interpreter, numThreads);

    interpreter->AllocateTensors();

    float x[] = {10.0};

    float *inputTensor = interpreter->typed_input_tensor<float>(0);
    memcpy(inputTensor, x, sizeof(x));

    interpreter->Invoke();

    float *y = interpreter->typed_output_tensor<float>(0);

    std::cout << y[0] << std::endl;

    return 0;
}
