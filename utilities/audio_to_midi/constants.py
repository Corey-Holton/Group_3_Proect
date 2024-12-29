# Third-Party Constants
from basic_pitch import ICASSP_2022_MODEL_PATH

# Default Model and Thresholds
DEFAULT_MODEL_PATH = ICASSP_2022_MODEL_PATH
DEFAULT_ONSET_THRESHOLD = 0.5
DEFAULT_FRAME_THRESHOLD = 0.3
DEFAULT_MIN_NOTE_LENGTH = 127.7
DEFAULT_SAMPLERATE = 44100
DEFAULT_MIDI_TEMPO = 120

# Default Output Directory
DEFAULT_OUTPUT_DIR = "./audio_processing/output_midi"

if __name__ == "__main__":
    print("This script contains the constants used in the audio to MIDI conversion process.")
