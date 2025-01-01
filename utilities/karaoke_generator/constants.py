# Third-Party Imports
import torch

# Constants
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
COMPUTE_TYPE = "int8_float16" if DEVICE == "cuda" else "int8"
MODEL_SIZE = "large-v3"

if __name__ == "__main__":
    print("This script contains the constants used in the lyrics extraction process.")