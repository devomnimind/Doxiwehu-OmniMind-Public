import torch

print("PyTorch version:", torch.__version__)
print("CUDA version (compiled):", torch.version.cuda)
print("CUDA available:", torch.cuda.is_available())
print("CUDA devices count:", torch.cuda.device_count())

if torch.cuda.is_available():
    print("Current CUDA device:", torch.cuda.current_device())
    print("Device name:", torch.cuda.get_device_name(torch.cuda.current_device()))
else:
    print("CUDA device not available.")
