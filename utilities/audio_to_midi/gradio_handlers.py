# Local Imports
from .main import _audio_to_midi
from .utilities import _validate_frequency
from .constants import (
    DEFAULT_ONSET_THRESHOLD,
    DEFAULT_FRAME_THRESHOLD,
    DEFAULT_MIN_NOTE_LENGTH,
    DEFAULT_SAMPLERATE,
    DEFAULT_MIDI_TEMPO,
    DEFAULT_OUTPUT_DIR,
)


def process_audio_to_midi_conversion(
    input_file,
    song_dir_name=None,
    save_midi=True,
    generate_audio_from_midi=False,
    save_model_outputs=False,
    onset_threshold=DEFAULT_ONSET_THRESHOLD,
    frame_threshold=DEFAULT_FRAME_THRESHOLD,
    min_note_length=DEFAULT_MIN_NOTE_LENGTH,
    min_frequency=None,
    max_frequency=None,
    allow_multiple_pitch_bends=False,
    apply_melodia_trick=True,
    samplerate=DEFAULT_SAMPLERATE,
    midi_tempo=DEFAULT_MIDI_TEMPO,
):
    """
    Convert an audio file to MIDI format with specified parameters.
    """
    # Validate frequency values
    min_frequency = _validate_frequency(min_frequency)
    max_frequency = _validate_frequency(max_frequency)

    # Call the core conversion function
    midi_path = _audio_to_midi(
        audio_path=input_file,
        output_directory=DEFAULT_OUTPUT_DIR,
        song_dir_name=song_dir_name,
        save_midi=save_midi,
        sonify_midi=generate_audio_from_midi,
        save_model_outputs=save_model_outputs,
        onset_threshold=onset_threshold,
        frame_threshold=frame_threshold,
        minimum_note_length=min_note_length,
        minimum_frequency=min_frequency,
        maximum_frequency=max_frequency,
        multiple_pitch_bends=allow_multiple_pitch_bends,
        melodia_trick=apply_melodia_trick,
        sonification_samplerate=samplerate,
        midi_tempo=midi_tempo,
    )
    return str(midi_path)
