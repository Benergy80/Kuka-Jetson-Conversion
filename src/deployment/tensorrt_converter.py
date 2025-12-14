"""TensorRT Model Conversion"""
import torch
from typing import Dict, Tuple

class TensorRTConverter:
    """Converts PyTorch models to TensorRT for optimized inference."""

    def __init__(self, model, input_shapes: Dict[str, Tuple]):
        self.model = model
        self.input_shapes = input_shapes

    def convert(self, output_path: str, fp16: bool = True) -> str:
        """Convert model to TensorRT."""
        try:
            import torch_tensorrt

            # Create example inputs
            example_inputs = {}
            for name, shape in self.input_shapes.items():
                example_inputs[name] = torch.randn(shape).cuda()

            # Compile with TensorRT
            trt_model = torch_tensorrt.compile(
                self.model,
                inputs=[torch_tensorrt.Input(shape) for shape in self.input_shapes.values()],
                enabled_precisions={torch.float16} if fp16 else {torch.float32},
            )

            torch.jit.save(trt_model, output_path)
            return output_path

        except ImportError:
            print("torch_tensorrt not available, saving as TorchScript")
            scripted = torch.jit.script(self.model)
            scripted.save(output_path.replace(".trt", ".pt"))
            return output_path.replace(".trt", ".pt")

    def export_onnx(self, output_path: str) -> str:
        """Export model to ONNX format."""
        dummy_inputs = {name: torch.randn(shape) for name, shape in self.input_shapes.items()}
        torch.onnx.export(self.model, dummy_inputs, output_path, opset_version=13)
        return output_path
