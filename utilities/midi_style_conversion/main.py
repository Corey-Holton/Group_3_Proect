# Standard Library Imports
from pathlib import Path
from pprint import pprint

# Third-Party Imports
import pretty_midi

# Local Imports
from .utilities import (
    _change_scale,
    _change_tempo,
    _transpose_midi,
    _adjust_note_durations,
    _add_swing,
    _adjust_velocity,
    _add_arpeggiation,
    _add_harmony,
    _humanize_midi,
    _add_volume_effect,
    _modify_instruments,
)


def _midi_style_conversion(input_midi_file, output_midi_path, **kwargs):
    """
    Modifies a MIDI file based on provided parameters.
    Uses our custom built functions in the `utilities.py` file.
    The `kwargs` dictionary should contain the parameters to modify the MIDI file.

    Args:
        input_midi_file (str or pretty_midi.PrettyMIDI): Path to input MIDI file or a PrettyMIDI object.
        output_midi_path (str): Path to save the modified MIDI file.
        **kwargs: Dictionary of parameters to modify MIDI. Possible keys:
            - scale (str): Target scale (e.g., 'C_major', 'A_minor').
            - instruments (dict): Mapping of instrument indices to names.
            - tempo (float): Target tempo in beats per minute.
            - transpose (int): Number of semitones to transpose.
            - duration_factor (float): Factor to scale note durations.
            - swing (bool): Add swing to notes.
            - velocity_factor (float): Factor to scale note velocities.
            - arpeggiate (bool): Apply arpeggiation to chords.
            - harmony (bool): Add harmonic notes.
            - humanize (bool): Add randomness for a humanized feel.
            - volume_effect (dict): Dict with 'value' (int) and 'time' (float).

    Returns:
        None
    """
    # Load MIDI file
    if isinstance(input_midi_file, pretty_midi.PrettyMIDI):
        midi_data = input_midi_file
    else:
        midi_data = pretty_midi.PrettyMIDI(input_midi_file)

    # Function mapping for modifications
    modification_map = {
        "scale": _change_scale,
        "tempo": _change_tempo,
        "transpose": _transpose_midi,
        "duration_factor": _adjust_note_durations,
        "swing": _add_swing,
        "velocity_factor": _adjust_velocity,
        "arpeggiate": _add_arpeggiation,
        "harmony": _add_harmony,
        "humanize": _humanize_midi,
        "volume_effect": lambda midi, params: _add_volume_effect(midi, params["value"], params["time"]),
    }

    # Apply modifications
    for key, func in modification_map.items():
        if key in kwargs and kwargs[key] is not None:
            if key == "volume_effect":
                # Special handling for dict-based parameter
                func(midi_data, kwargs[key])
            elif key in ["duration_factor", "velocity_factor", "tempo", "transpose"]:
                func(midi_data, kwargs[key])
            elif key in ["scale"]:
                func(midi_data, kwargs[key])
            elif kwargs[key]:
                # For boolean flags like swing, arpeggiate, etc.
                func(midi_data)

    # Modify instruments if specified
    if "instruments" in kwargs and kwargs["instruments"]:
        _modify_instruments(midi_data, kwargs["instruments"])

    # Save the modified MIDI file
    midi_data.write(output_midi_path)


if __name__ == "__main__":
    print("This script is a utility module and cannot be executed directly.")
