# Third-Party Imports
import torch

# Constants
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
COMPUTE_TYPE = "int8_float16" if DEVICE == "cuda" else "int8"
MODEL_SIZE = "large-v3"

# Default Output Directories
DEFAULT_OUTPUT_DIR_LYRICS_RAW = "./audio_processing/karaoke_files/output_lyrics_raw/"
DEFAULT_OUTPUT_DIR_LYRICS_MODIFIED = "./audio_processing/karaoke_files/output_lyrics_modified/"
DEFAULT_OUTPUT_DIR_INSTRUMENTAL = "./audio_processing/karaoke_files/output_instrumentals/"
DEFAULT_OUTPUT_DIR_ASS = "./audio_processing/karaoke_files/output_ass/"
DEFAULT_OUTPUT_DIR_VIDEO = "./audio_processing/karaoke_files/output_videos/"

if __name__ == "__main__":
    print("This script contains the constants used in the lyrics extraction process.")