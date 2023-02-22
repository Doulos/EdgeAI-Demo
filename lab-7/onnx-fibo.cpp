#include <onnxruntime/onnxruntime_cxx_api.h>
#include <iostream>

int main()
{
	Ort::Env env;
	Ort::RunOptions runOptions;
	Ort::Session session(nullptr);

   // create session
    session = Ort::Session(env, "/home/..../fibonacci.onnx", 		Ort::SessionOptions{ nullptr });

   
    // define shape
    const std::array<int64_t, 2> inputShape = { 1, 3  };
    const std::array<int64_t, 2> outputShape = { 1, 2 };

    // define array
    std::array<float, 3 > input = {21.0, 34.0, 55.0};
    std::array<float, 2 > results;

// define Tensor

auto memory_info = Ort::MemoryInfo::CreateCpu(OrtDeviceAllocator, 			OrtMemTypeCPU);

auto inputTensor = Ort::Value::CreateTensor<float>(memory_info, 			input.data(), input.size(), 					inputShape.data(), inputShape.size());

auto outputTensor = Ort::Value::CreateTensor<float>(memory_info, 			results.data(), results.size(), 					outputShape.data(), outputShape.size());


// define names

Ort::AllocatorWithDefaultOptions ort_alloc;

const char* inputName = session.GetInputName(0, ort_alloc);
const char* outputName = session.GetOutputName(0, ort_alloc);
const std::array<const char*, 1> inputNames = {inputName };
const std::array<const char*, 1> outputNames = {outputName };

// run inference

try {
     session.Run(runOptions, inputNames.data(), &inputTensor, 1, 				outputNames.data(), &outputTensor, 1);
    }
catch (Ort::Exception& e) {
     std::cout << e.what() << std::endl;
        return 1;
    }

    
for (size_t i =0; i<2; ++i) {
	  std::cout << results[i] << std::endl;
   }
}