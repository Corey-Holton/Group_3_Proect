# File Extensions to search for in the input directory
EXTENSIONS = {"mp3", "wav", "ogg", "flac"}

# Default Model and Thresholds
DEFAULT_MODEL = "htdemucs_ft"
DEFAULT_MP3_RATE = 320

# Default Output Directory
DEFAULT_OUTPUT_DIR = "./audio_processing/output_stems"

if __name__ == "__main__":
    print("This script contains the constants used in the audio stem separation process.")