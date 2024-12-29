# Third-Party Imports
from basic_pitch.inference import Model

# Local Imports
from .main import _audio_to_midi
from .utilities import _validate_frequency
from .constants import (
    DEFAULT_MODEL_PATH,
    DEFAULT_ONSET_THRESHOLD,
    DEFAULT_FRAME_THRESHOLD,
    DEFAULT_MIN_NOTE_LENGTH,
    DEFAULT_SAMPLERATE,
    DEFAULT_MIDI_TEMPO,
    DEFAULT_OUTPUT_DIR,
)

# ════════════════════════════════════════════════════════════
# Gradio Audio-to-MIDI Conversion Handler
# ════════════════════════════════════════════════════════════
def process_audio_to_midi_conversion(
    # ! Parameters here are handled in the Gradio Interface.
    # ! The order of parameters MUST match the Gradio interface to function correctly.
    input_file,                 # Path to the input audio file (provided by Gradio).
    song_dir_name=None,         # Optional: Directory name for saving MIDI output.
    save_midi=True,             # Save the generated MIDI file (Gradio toggle).
    generate_audio_from_midi=False,  # Generate audio from the MIDI file (Gradio toggle).
    save_model_outputs=False,   # Save intermediate model outputs (Gradio toggle).
    onset_threshold=DEFAULT_ONSET_THRESHOLD,  # Onset detection threshold for the model.
    frame_threshold=DEFAULT_FRAME_THRESHOLD,  # Frame activation threshold for the model.
    min_note_length=DEFAULT_MIN_NOTE_LENGTH,  # Minimum note length to consider (in ms).
    min_frequency=None,         # Optional: Minimum frequency for note detection.
    max_frequency=None,         # Optional: Maximum frequency for note detection.
    allow_multiple_pitch_bends=False,  # Enable multiple pitch bends in the MIDI.
    apply_melodia_trick=True,   # Apply Melodia trick for smoother transitions.
    samplerate=DEFAULT_SAMPLERATE,  # Sampling rate for sonification (default: 44100 Hz).
    midi_tempo=DEFAULT_MIDI_TEMPO,  # Default tempo for the generated MIDI file.
):
    """
    Convert an audio file to MIDI format with specified parameters.

    Parameters:
    - input_file (str): Path to the input audio file.
    - song_dir_name (str, optional): Subdirectory name for saving output files.
    - save_midi (bool): Whether to save the generated MIDI file.
    - generate_audio_from_midi (bool): Whether to generate an audio file from the MIDI.
    - save_model_outputs (bool): Save intermediate model outputs (if applicable).
    - onset_threshold (float): Threshold for onset detection.
    - frame_threshold (float): Threshold for frame activation.
    - min_note_length (float): Minimum length for detected notes, in milliseconds.
    - min_frequency (float, optional): Minimum frequency to consider for note detection.
    - max_frequency (float, optional): Maximum frequency to consider for note detection.
    - allow_multiple_pitch_bends (bool): Allow multiple pitch bends in MIDI.
    - apply_melodia_trick (bool): Apply Melodia trick to enhance smoothness.
    - samplerate (int): Sampling rate for audio processing.
    - midi_tempo (int): Tempo for the generated MIDI file.

    Returns:
    - str: Path to the generated MIDI file.
    """
    # Validate frequency inputs (Since 0 is not a valid frequency)
    min_frequency = _validate_frequency(min_frequency)
    max_frequency = _validate_frequency(max_frequency)

    # Call the core conversion function
    midi_path = _audio_to_midi(
        # Default parameters here that are not set by Gradio
        # Can be modified for internal automation
        audio_path=input_file,
        output_directory=DEFAULT_OUTPUT_DIR,
        song_dir_name=song_dir_name,
        save_midi=save_midi,
        sonify_midi=generate_audio_from_midi,
        save_model_outputs=save_model_outputs,
        save_notes=False,
        model_or_model_path=Model(DEFAULT_MODEL_PATH),
        onset_threshold=onset_threshold,
        frame_threshold=frame_threshold,
        minimum_note_length=min_note_length,
        minimum_frequency=min_frequency,
        maximum_frequency=max_frequency,
        multiple_pitch_bends=allow_multiple_pitch_bends,
        melodia_trick=apply_melodia_trick,
        debug_file=None, 
        sonification_samplerate=samplerate,
        midi_tempo=midi_tempo,
    )
    return str(midi_path)

if __name__ == "__main__":
    print("This script is designed to be used as a Gradio interface for audio-to-MIDI conversion.")