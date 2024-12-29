from pathlib import Path

# Third-Party Imports
from basic_pitch.inference import predict_and_save, Model

# Local Imports
from .constants import (
    DEFAULT_MODEL_PATH,
    DEFAULT_ONSET_THRESHOLD,
    DEFAULT_FRAME_THRESHOLD,
    DEFAULT_MIN_NOTE_LENGTH,
    DEFAULT_SAMPLERATE,
    DEFAULT_MIDI_TEMPO,
    DEFAULT_OUTPUT_DIR,
)
from .utilities import _create_directory
from ..print_utilities import print_title, print_message


def _audio_to_midi(
    audio_path,
    output_directory=DEFAULT_OUTPUT_DIR,
    song_dir_name=None,
    save_midi=True,
    sonify_midi=False,
    save_model_outputs=False,
    save_notes=False,
    model_or_model_path=Model(DEFAULT_MODEL_PATH),
    onset_threshold=DEFAULT_ONSET_THRESHOLD,
    frame_threshold=DEFAULT_FRAME_THRESHOLD,
    minimum_note_length=DEFAULT_MIN_NOTE_LENGTH,
    minimum_frequency=None,
    maximum_frequency=None,
    multiple_pitch_bends=False,
    melodia_trick=True,
    debug_file=None,
    sonification_samplerate=DEFAULT_SAMPLERATE,
    midi_tempo=DEFAULT_MIDI_TEMPO,
):
    """
    Convert audio files to MIDI using the Basic Pitch model.
    """
    print_title("Converting Audio to MIDI with Basic-Pitch")

    # Convert paths
    audio_path = Path(audio_path)
    output_directory = (
        Path(f"{output_directory}/{song_dir_name}") if song_dir_name else Path(output_directory)
    )

    # Create output directory
    _create_directory(output_directory)

    print_message("[INFO]", text_color="bright_blue")
    print_message(f"Converting audio file:", text_color="bright_blue", indent_level=1)
    print_message(f"`{audio_path.name}`", text_color="bright_blue", indent_level=2, include_border=True)

    # Predict and save MIDI
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

    # Return MIDI file path
    midi_file_path = Path(f"{output_directory}/{audio_path.stem}_basic_pitch.mid")
    print_message("[SUCCESS]", text_color="bright_green")
    print_message("MIDI file saved in:", text_color="bright_green", indent_level=1)
    print_message(f"`{midi_file_path}`", text_color="bright_green", indent_level=2, include_border=True)

    return midi_file_path
