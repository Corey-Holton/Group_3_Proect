from pathlib import Path

# Third-Party Imports
from basic_pitch.inference import predict_and_save, Model

# Local Imports
from .utilities import _create_directory
from ..print_utilities import print_title, print_message


def _audio_to_midi(
    # ! Reference: See `gradio_handlers.py` for how these parameters integrate with Gradio
    # ! Private function: Used internally for audio-to-MIDI conversion
    # ! Do not modify parameter names or order
    audio_path,               # Path to the input audio file
    output_directory,         # Directory to save MIDI output
    song_dir_name,            # Subdirectory for saving outputs
    save_midi,                # Whether to save the MIDI file
    sonify_midi,              # Generate audio from MIDI
    save_model_outputs,       # Save intermediate outputs
    save_notes,               # Save note-based data
    model_or_model_path,      # Model used for conversion
    onset_threshold,          # Onset detection threshold
    frame_threshold,          # Frame activation threshold
    minimum_note_length,      # Minimum note length in ms
    minimum_frequency,        # Minimum frequency for note detection
    maximum_frequency,        # Maximum frequency for note detection
    multiple_pitch_bends,     # Allow multiple pitch bends in MIDI
    melodia_trick,            # Apply Melodia trick for smoother results
    debug_file,               # Optional debug file
    sonification_samplerate,  # Sampling rate for MIDI sonification
    midi_tempo,               # Tempo for the generated MIDI
):
    """
    Internal function for audio-to-MIDI conversion.
    Parameters are explained in the `process_audio_to_midi_conversion` function.

    Returns:
    - str: Path to the generated MIDI file.
    """

    print_title("Converting Audio to MIDI with Basic-Pitch")

    # Convert the input paths and output directory to Path objects
    audio_path = Path(audio_path)

    # If a song directory name is provided, create a subdirectory for the song in the output directory
    output_directory = (
        Path(f"{output_directory}/{song_dir_name}") if song_dir_name else Path(output_directory)
    )

    # Create the output directory if it does not exist
    _create_directory(output_directory)

    # Print information about the audio file being converted
    print_message("[INFO]", text_color="bright_blue")
    print_message(f"Converting audio file:", text_color="bright_blue", indent_level=1)
    print_message(f"`{audio_path.name}`", text_color="bright_blue", indent_level=2, include_border=True)

    # Predict and save MIDI
    predict_and_save(
        # ! Reference: See `gradio_handlers.py` for how these parameters integrate with Gradio
        # ! Do not modify parameter names or order
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

    # Return MIDI file path
    midi_file_path = Path(f"{output_directory}/{audio_path.stem}_basic_pitch.mid")

    # Print success message and MIDI file path
    print_message("[SUCCESS]", text_color="bright_green")
    print_message("MIDI file saved in:", text_color="bright_green", indent_level=1)
    print_message(f"`{midi_file_path}`", text_color="bright_green", indent_level=2, include_border=True)

    return midi_file_path

if __name__ == "__main__":
    print("This script is designed to convert audio files to MIDI using the Basic Pitch model.")