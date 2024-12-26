import pretty_midi
from pathlib import Path
from pprint import pprint

from .modify_midi_utilities import (
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

from .modify_midi_prompt_config import execute_query
from .print_utilities import print_title, print_line


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


def modify_midi_prompt(input_midi_file, song_dir_name=False, song_prefix_name=False, text_prompt=None):
    """
    Prompts the user for parameters to modify a MIDI file based on a text query.

    Args:
        input_midi_file (str): Path to input MIDI file.
        output_midi_path (str): Path to save the modified MIDI file.
        text_prompt (str): Text prompt to describe modifications.

    Returns:
        None
    """
    print_title("Modify MIDI File", text_color="bright_white")

    if not song_dir_name:
        print_line("[ERROR] \n\tSong directory name is required.", text_color="bright_red")
        return

    if not song_prefix_name:
        print_line("[ERROR] \n\tSong prefix name is required.", text_color="bright_red")
        return

    output_midi_path = f"./audio_processing/output_midi_mods/{song_dir_name}/{song_prefix_name}_{Path(input_midi_file).stem}.mid"

    # Validate input MIDI file
    input_path = Path(input_midi_file)
    if not input_path.exists() or input_path.suffix.lower() != ".mid":
        print_line(f"[ERROR] \n\tInvalid MIDI file: \n\t\t{input_midi_file}", text_color="bright_red")
        return

    # Validate output path
    output_dir = Path(output_midi_path).parent
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
        print_line(f"[DIR] \n\tCreated output directory: \n\t\t{output_dir}", text_color="yellow")

    # Display user query
    if text_prompt:
        print_line(f"[PROMPT] \n\tUser Input: \n\t\t{text_prompt}", text_color="bright_blue")

    # Execute query using the text prompt
    try:
        query_params = execute_query(text_prompt)
    except Exception as e:
        print_line(f"[ERROR] \n\tFailed to process query: \n\t\t{e}", text_color="bright_red")
        return

    # Confirm query parameters
    print(f"[INFO] \n\tParsed Parameters:")
    pprint(query_params)
    print_line("", text_color="bright_blue")

    # Modify MIDI file using provided parameters
    try:
        query_params['instruments'] = {int(k): v for k, v in query_params['instruments'].items()}
        modify_midi(input_midi_file, output_midi_path, **query_params)
        print_line(f"[SUCCESS] \n\tModified MIDI saved to: \n\t\t{output_midi_path}", text_color="bright_green")
    except Exception as e:
        print_line(f"[ERROR] \n\tMIDI modification failed: \n\t\t{e}", text_color="bright_red")

    return output_midi_path

if __name__ == "__main__":
    print("This script is a utility module and cannot be executed directly.")