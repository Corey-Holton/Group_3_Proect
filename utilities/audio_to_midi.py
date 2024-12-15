"""
This script is designed to convert audio files to MIDI using the Basic Pitch model.

Summary:
- The main function `audio_to_midi` takes an input audio file and converts it to a MIDI file.
- The converted MIDI file is saved in the specified output directory.
- The script uses the Basic Pitch model for audio-to-MIDI conversion.

Usage:
- Call the `audio_to_midi` function with the path to the input audio file and the desired output directory.
- Customize the parameters of the `audio_to_midi` function as needed to suit your requirements.
"""
# Standard Library Imports
from pathlib import Path

# Third-Party Imports
from basic_pitch.inference import predict_and_save, Model
from basic_pitch import ICASSP_2022_MODEL_PATH

# Local Imports
from .print_utilities import print_title, print_line

# Function to convert audio to MIDI using the Basic Pitch model
def audio_to_midi(
        audio_path,
        output_directory="./audio_processing/output_midi",
        save_midi=True,
        sonify_midi=False,
        save_model_outputs=False,
        save_notes=False,
        model_or_model_path=Model(ICASSP_2022_MODEL_PATH),
        onset_threshold=0.5,
        frame_threshold=0.3,
        minimum_note_length=127.70,
        minimum_frequency=None,
        maximum_frequency=None,
        multiple_pitch_bends=False,
        melodia_trick=True,
        debug_file=None,
        sonification_samplerate=44100,
        midi_tempo=120,
):
    """
    Convert audio files to MIDI using the Basic Pitch model.
    """

    print_title("[STEP 2] Converting Audio to MIDI", text_color="bright_white")

    # Convert the input paths and output directory to Path objects
    audio_path = Path(audio_path)
    output_directory = Path(output_directory)

    # Create the output directory if it does not exist
    if not output_directory.exists():
        output_directory.mkdir(parents=True, exist_ok=True)
        print_line(f"[DIR] \n\tCreated output directory: \n\t\t{output_directory}", text_color="yellow")

    print_line(f"[INFO] \n\tConverting audio file to MIDI: \n\t\t`{str(audio_path).split('/')[-1]}`", text_color="bright_blue")

    # Call the predict_and_save function from the Basic Pitch model
    predict_and_save(
        audio_path_list=[audio_path],
        output_directory=output_directory,
        save_midi=save_midi,
        sonify_midi=sonify_midi,
        save_model_outputs=save_model_outputs,
        save_notes=save_notes,
        model_or_model_path=model_or_model_path,
        onset_threshold=onset_threshold,
        frame_threshold=frame_threshold,
        minimum_note_length=minimum_note_length,
        minimum_frequency=minimum_frequency,
        maximum_frequency=maximum_frequency,
        multiple_pitch_bends=multiple_pitch_bends,
        melodia_trick=melodia_trick,
        debug_file=debug_file,
        sonification_samplerate=sonification_samplerate,
        midi_tempo=midi_tempo,
    )
    print_line(" ")

    # Create the MIDI file path
    midi_file_path = Path(f"{output_directory}/{audio_path.stem}_basic_pitch.mid")
    print_line(f"[SUCCESS] \n\tMIDI file saved in: \n\t\t{midi_file_path}", text_color="bright_green")

    return midi_file_path