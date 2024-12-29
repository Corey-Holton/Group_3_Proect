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
from .print_utilities import print_title, print_message

# Function to convert audio to MIDI using the Basic Pitch model
def audio_to_midi(
        audio_path,
        output_directory="./audio_processing/output_midi",
        song_dir_name=None,
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

    print_title("Converting Audio to MIDI with Basic-Pitch", text_color="bright_white")

    # Convert the input paths and output directory to Path objects
    audio_path = Path(audio_path)

    # If a song directory name is provided, create a subdirectory for the song in the output directory
    output_directory = Path(f"{output_directory}/{song_dir_name}") if song_dir_name else Path(output_directory)

    # Create the output directory if it does not exist
    if not output_directory.exists():
        output_directory.mkdir(parents=True, exist_ok=True)
        print_message("[DIR]", text_color="bright_yellow")
        print_message("Created output directory:", text_color="bright_yellow", indent_level=1)
        print_message(f"`{output_directory}`", text_color="bright_yellow", indent_level=2, include_border=True)

    print_message("[INFO]", text_color="bright_blue")
    print_message("Converting audio file to MIDI:", text_color="bright_blue", indent_level=1)
    print_message(f"`{audio_path.name}`", text_color="bright_blue", indent_level=2, include_border=True)

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
    print_message("", include_border=True)

    # Create the MIDI file path
    midi_file_path = Path(f"{output_directory}/{audio_path.stem}_basic_pitch.mid")
    print_message("[SUCCESS]", text_color="bright_green")
    print_message("MIDI file saved in:", text_color="bright_green", indent_level=1)
    print_message(f"`{midi_file_path}`", text_color="bright_green", indent_level=2, include_border=True)

    return midi_file_path