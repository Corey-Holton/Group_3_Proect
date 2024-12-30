# Third-Party Imports
import pretty_midi

# Default Output Directory
DEFAULT_OUTPUT_DIR = "./audio_processing/output_midi_mods/"

def generate_note_list():
    """
    Generate a list of all possible MIDI note names (e.g., C0, C#0, D0, ..., G9).

    Returns:
        List[str]: A list of note names.
    """
    note_names = []
    pitch_map = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    # MIDI note range is 0–127
    for octave in range(-1, 10):  # Octaves -1 to 9
        for pitch_class in pitch_map:
            note_names.append(f"{pitch_class}{octave}")
    
    return note_names


def validate_note_list(note_list):
    """ 
    Validate the note list by converting each note to a MIDI note number.

    Args:
        note_list (List[str]): List of note names to validate.

    Returns:
        None
    """
    for note in note_list:
        try:
            print(f"{note}: {pretty_midi.note_name_to_number(note)}")
        except ValueError as e:
            print(f"Error with note {note}: {e}")


# Constants: A list of valid instruments and notes that are available for use
VALID_INSTRUMENTS = [pretty_midi.program_to_instrument_name(program) for program in range(128)]

# Constants: A mapping of MIDI program instrument names to program numbers
INSTRUMENT_TO_PROGRAM = {pretty_midi.program_to_instrument_name(program): program for program in range(128)}

# Constants: A mapping of MIDI program numbers to instrument names
PROGRAM_TO_INSTRUMENT = {v: k for k, v in INSTRUMENT_TO_PROGRAM.items()}

# Constants: A list of valid note syntaxes that are available for use
VALID_NOTES = generate_note_list() 

# Constants: Details of acceptable parameters for our functions in `utilities.py` that Google's AI model will use
ACCEPTABLE_PARAMETERS = {
    "instruments": {
    "type": "dict[int, int]",  # Map channel indices to program numbers
    "description": "Mapping of channel indices to MIDI program numbers.",
    "constraints": (
        "Keys must be integer channel indices; values must be integers corresponding to valid MIDI program numbers "
        f"(0-127). The mapping is: {INSTRUMENT_TO_PROGRAM}."
    ),
    "complex": True
    },
    "scale": {
        "type": "str",
        "description": (
            "Target scale to transpose the MIDI file to. "
            "Format: '(Note)(Accidental)(Octave)_(Type)', e.g., 'C#4_major' or 'D-1_minor'. "
            "Note: Acceptable notes are A, B, C, D, E, F, G. "
            "Accidentals: '#' for sharp, 'b' for flat. "
            "Octave: A number between -1 and 9."
        ),
        "constraints": "Must follow the exact format 'RootOctave_Type'. Types: major or minor.",
        "complex": True
    },
    "tempo": {
        "type": "float",
        "description": "Target tempo in beats per minute.",
        "constraints": "Must be a positive number.",
        "complex": True
    },
    "transpose": {
        "type": "int",
        "description": "Number of semitones to transpose.",
        "constraints": "Range: -48 to 48.",
        "complex": True
    },
    "duration_factor": {
        "type": "float",
        "description": "Factor to scale note durations.",
        "constraints": "Must be a positive number.",
        "complex": True
    },
    "swing": {
        "type": "bool",
        "description": "Add swing to notes.",
        "constraints": "Set to True to enable.",
        "complex": False
    },
    "velocity_factor": {
        "type": "float",
        "description": "Factor to scale note velocities.",
        "constraints": "Must be a positive number.",
        "complex": True
    },
    "arpeggiate": {
        "type": "bool",
        "description": "Apply arpeggiation to chords.",
        "constraints": "Set to True to enable.",
        "complex": False
    },
    "harmony": {
        "type": "bool",
        "description": "Add harmonic notes.",
        "constraints": "Set to True to enable.",
        "complex": False
    },
    "humanize": {
        "type": "bool",
        "description": "Add randomness for a humanized feel.",
        "constraints": "Set to True to enable.",
        "complex": False
    },
    "volume_effect": {
        "type": "dict",
        "description": "Volume effect parameters.",
        "constraints": "Must contain 'value' (int, 0-127) and 'time' (float, within MIDI duration).",
        "complex": True
    },
}


if __name__ == "__main__":
    print("Validating note list...")
    validate_note_list(VALID_NOTES)