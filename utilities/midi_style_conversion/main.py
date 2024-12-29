# Standard Library Imports
from pathlib import Path
from pprint import pprint

# Third-Party Imports
import pretty_midi

# Local Imports
from .utilities import (
    change_scale,
    change_tempo,
    transpose_midi,
    adjust_note_durations,
    add_swing,
    adjust_velocity,
    add_arpeggiation,
    add_harmony,
    humanize_midi,
    add_volume_effect,
    modify_instruments,
)
from .prompt_config import execute_query
from ..print_utilities import print_title, print_message


def modify_midi(input_midi_file, output_midi_path, **kwargs):
    """
    Modifies a MIDI file based on provided parameters.

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
        "scale": change_scale,
        "tempo": change_tempo,
        "transpose": transpose_midi,
        "duration_factor": adjust_note_durations,
        "swing": add_swing,
        "velocity_factor": adjust_velocity,
        "arpeggiate": add_arpeggiation,
        "harmony": add_harmony,
        "humanize": humanize_midi,
        "volume_effect": lambda midi, params: add_volume_effect(midi, params["value"], params["time"]),
    }

    # Apply modifications
    for key, func in modification_map.items():
        if key in kwargs and kwargs[key] is not None:
            if key == "volume_effect":
                func(midi_data, kwargs[key])  # Special handling for dict-based parameter
            elif key in ["duration_factor", "velocity_factor", "tempo", "transpose"]:
                func(midi_data, kwargs[key])
            elif key in ["scale"]:
                func(midi_data, kwargs[key])
            elif kwargs[key]:
                func(midi_data)  # For boolean flags like swing, arpeggiate, etc.

    # Modify instruments if specified
    if "instruments" in kwargs and kwargs["instruments"]:
        modify_instruments(midi_data, kwargs["instruments"])

    # Save the modified MIDI file
    midi_data.write(output_midi_path)


if __name__ == "__main__":
    print("This script is a utility module and cannot be executed directly.")