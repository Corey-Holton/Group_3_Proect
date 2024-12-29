# Standard Library Imports
from collections import Counter
import random

# Third-Party Imports
import pretty_midi

# Local Imports
from .constants import VALID_INSTRUMENTS


def modify_instruments(midi_data, instruments):
    """
    Modify the instruments in a MIDI file.

    Args:
        midi_data (pretty_midi.PrettyMIDI): MIDI data object.
        instruments (dict): Mapping of instrument indices to names.

    Returns:
        None
    """
    for idx, instrument in instruments.items():
        if instrument not in VALID_INSTRUMENTS:
            raise ValueError(f"Invalid instrument name: '{instrument}'. Must be one of: {VALID_INSTRUMENTS}")
        
        if idx < len(midi_data.instruments):
            midi_data.instruments[idx].name = instrument
            midi_data.instruments[idx].program = pretty_midi.instrument_name_to_program(instrument)


def detect_scale(midi_data):
    """
    Detect the most likely scale (major or minor) of the MIDI file.

    Args:
        midi_data (pretty_midi.PrettyMIDI): MIDI data object.

    Returns:
        str: Detected scale, e.g., 'C_major' or 'A_minor'.
    """
    # Count occurrences of each pitch class
    pitch_classes = Counter()
    for instrument in midi_data.instruments:
        for note in instrument.notes:
            pitch_classes[note.pitch % 12] += 1

    # Major and minor scale intervals
    major_intervals = [0, 2, 4, 5, 7, 9, 11]
    minor_intervals = [0, 2, 3, 5, 7, 8, 10]

    # Check each root note
    best_match = None
    best_score = 0
    for root in range(12):
        major_scale = [(root + i) % 12 for i in major_intervals]
        minor_scale = [(root + i) % 12 for i in minor_intervals]

        # Score scales based on note frequency
        major_score = sum(pitch_classes[pc] for pc in major_scale)
        minor_score = sum(pitch_classes[pc] for pc in minor_scale)

        if major_score > best_score:
            best_score = major_score
            best_match = f"{pretty_midi.note_number_to_name(root)}_major"

        if minor_score > best_score:
            best_score = minor_score
            best_match = f"{pretty_midi.note_number_to_name(root)}_minor"

    # Handle ambiguous cases by adding a threshold check
    if abs(major_score - minor_score) < 5: 
        print("Scale detection is ambiguous; scores are close.")

    return best_match


def change_scale(midi_data, target_scale):
    """
    Change the scale of a MIDI file.

    Args:
        midi_data (pretty_midi.PrettyMIDI): MIDI data object.
        target_scale (str): Target scale, e.g., 'C_major' or 'A_minor'.

    Returns:
        None
    """
    # Validate target scale
    if "_" not in target_scale or len(target_scale.split("_")) != 2:
        raise ValueError("Target scale must be in the format 'Root_Type', e.g., 'C#-1_major'.")

    # Parse target scale
    root_note, scale_type = target_scale.split("_")
    try:
        root_note_number = pretty_midi.note_name_to_number(root_note)
    except ValueError as e:
        raise ValueError(f"Invalid root note '{root_note}': {e}")

    if scale_type == "major":
        target_intervals = [0, 2, 4, 5, 7, 9, 11]
    elif scale_type == "minor":
        target_intervals = [0, 2, 3, 5, 7, 8, 10]
    else:
        raise ValueError(f"Unknown scale type: {scale_type}. Supported types are 'major' and 'minor'.")

    # Generate target scale
    target_scale = [(root_note_number + i) % 12 for i in target_intervals]

    # Map notes to the target scale
    for instrument in midi_data.instruments:
        for note in instrument.notes:
            original_pitch = note.pitch % 12
            nearest_pitch = min(target_scale, key=lambda x: abs(x - original_pitch))
            note.pitch = note.pitch - original_pitch + nearest_pitch


def change_tempo(midi_data, target_tempo):
    """
    Adjust the tempo of a MIDI file.

    Args:
        midi_data (pretty_midi.PrettyMIDI): MIDI data object.
        target_tempo (float): Target tempo in beats per minute (BPM).

    Returns:
        None
    """
    # Validate target tempo
    if target_tempo <= 0:
        raise ValueError("Target tempo must be a positive value.")

    # Calculate the duration of the MIDI file
    tempo_times, tempo_values = midi_data.get_tempo_changes()
    
    if len(tempo_values) > 0:
        # Calculate the average tempo if there are multiple tempo changes
        original_tempo = sum(tempo_values) / len(tempo_values)
    else:
        # Default to 120 BPM if no tempo information exists
        original_tempo = 120

    # Calculate tempo ratio
    tempo_ratio = original_tempo / target_tempo

    # Scale the timing of all notes
    for instrument in midi_data.instruments:
        for note in instrument.notes:
            note.start *= tempo_ratio
            note.end *= tempo_ratio

    # Scale timing of control changes
    for instrument in midi_data.instruments:
        for control_change in instrument.control_changes:
            control_change.time *= tempo_ratio

    # Scale timing of meta events
    for lyric in midi_data.lyrics:
        lyric.time *= tempo_ratio

    for time_signature in midi_data.time_signature_changes:
        time_signature.time *= tempo_ratio
        
    for key_signature in midi_data.key_signature_changes:
        key_signature.time *= tempo_ratio

    # Update the total time in the MIDI file
    total_time = midi_data.get_end_time()
    midi_data.adjust_times([0, total_time], [0, total_time * tempo_ratio])


def adjust_note_durations(midi_data, duration_factor):
    """
    Adjust the duration of notes in a MIDI file.

    Args:
        midi_data (pretty_midi.PrettyMIDI): MIDI data object.
        duration_factor (float): Factor by which to scale note durations.

    Returns:
        None
    """
    if duration_factor <= 0:
        raise ValueError("Duration factor must be a positive value.")
    
    for instrument in midi_data.instruments:
        for note in instrument.notes:
            note.end = note.start + (note.end - note.start) * duration_factor


def add_swing(midi_data, swing_factor=0.2):
    """
    Add a swing feel to the MIDI file by delaying every second note slightly.

    Args:
        midi_data (pretty_midi.PrettyMIDI): MIDI data object.
        swing_factor (float): Proportion of delay for "swinging" notes (0.0 to 0.5).

    Returns:
        None
    """
    if not (0.0 <= swing_factor <= 0.5):
        raise ValueError("Swing factor must be between 0.0 and 0.5.")

    for instrument in midi_data.instruments:
        for i, note in enumerate(instrument.notes):
            if i % 2 == 1:  # Delay every second note
                delay = (note.end - note.start) * swing_factor
                note.start += delay
                note.end += delay


def adjust_velocity(midi_data, factor=1.2):
    """
    Adjust the velocity of all notes to change the dynamic intensity.

    Args:
        midi_data (pretty_midi.PrettyMIDI): MIDI data object.
        factor (float): Factor to scale velocities (e.g., 1.2 for louder, 0.8 for softer).

    Returns:
        None
    """
    if factor <= 0:
        raise ValueError("Velocity factor must be a positive value.")

    for instrument in midi_data.instruments:
        for note in instrument.notes:
            note.velocity = min(max(int(note.velocity * factor), 0), 127)


def add_arpeggiation(midi_data, interval=0.1):
    """
    Convert chords into arpeggios by staggering the timing of notes.

    Args:
        midi_data (pretty_midi.PrettyMIDI): MIDI data object.
        interval (float): Time interval to stagger arpeggiated notes.

    Returns:
        None
    """
    if interval < 0:
        raise ValueError("Interval must be a non-negative value.")

    for instrument in midi_data.instruments:
        arpeggiated_notes = []
        for note in instrument.notes:
            staggered_time = note.start
            arpeggiated_notes.append(pretty_midi.Note(
                velocity=note.velocity,
                pitch=note.pitch,
                start=staggered_time,
                end=note.end,
            ))
            note.start += interval  # Shift the start time for the next note
        instrument.notes = arpeggiated_notes


def add_harmony(midi_data, interval=7):
    """
    Add harmonic notes to the melody.

    Args:
        midi_data (pretty_midi.PrettyMIDI): MIDI data object.
        interval (int): Interval (in semitones) to add as harmony.

    Returns:
        None
    """
    for instrument in midi_data.instruments:
        new_notes = []
        for note in instrument.notes:
            harmony_pitch = note.pitch + interval
            if 0 <= harmony_pitch <= 127:  # Ensure valid MIDI range
                harmony_note = pretty_midi.Note(
                    velocity=note.velocity,
                    pitch=harmony_pitch,
                    start=note.start,
                    end=note.end,
                )
                new_notes.append(harmony_note)
        instrument.notes.extend(new_notes)


def humanize_midi(midi_data, timing_variation=0.05, velocity_variation=10):
    """
    Add randomness to note timing and velocity for a humanized feel.

    Args:
        midi_data (pretty_midi.PrettyMIDI): MIDI data object.
        timing_variation (float): Maximum time deviation (in seconds).
        velocity_variation (int): Maximum velocity deviation.

    Returns:
        None
    """
    if timing_variation < 0:
        raise ValueError("Timing variation must be a non-negative value.")
    if velocity_variation < 0:
        raise ValueError("Velocity variation must be a non-negative value.")

    for instrument in midi_data.instruments:
        for note in instrument.notes:
            note.start += random.uniform(-timing_variation, timing_variation)
            note.end += random.uniform(-timing_variation, timing_variation)
            note.velocity = min(max(note.velocity + random.randint(-velocity_variation, velocity_variation), 0), 127)


def transpose_midi(midi_data, semitones):
    """
    Transpose all notes in the MIDI file by a given number of semitones.

    Args:
        midi_data (pretty_midi.PrettyMIDI): MIDI data object.
        semitones (int): Number of semitones to transpose (e.g., +2 or -2).

    Returns:
        None
    """
    # Validate semitones to prevent extreme values
    if not (-48 <= semitones <= 48):  # Typical instrument range limit
        raise ValueError("Semitones must be between -48 and 48 to ensure realistic transposition.")

    for instrument in midi_data.instruments:
        for note in instrument.notes:
            note.pitch = max(0, min(127, note.pitch + semitones))  # Ensure within MIDI range


def add_volume_effect(midi_data, value, time):
    """
    Add a volume control change to the MIDI file.

    Args:
        midi_data (pretty_midi.PrettyMIDI): MIDI data object.
        value (int): Volume value (0–127).
        time (float): Time in seconds for the control change.

    Returns:
        None
    """
    # Validate volume value
    if not (0 <= value <= 127):
        raise ValueError("Volume value must be between 0 and 127.")

    # Validate time to ensure it is within the MIDI file's duration
    if time < 0 or time > midi_data.get_end_time():
        raise ValueError("Time must be within the duration of the MIDI file.")

    for instrument in midi_data.instruments:
        instrument.control_changes.append(pretty_midi.ControlChange(number=7, value=value, time=time))

if __name__ == "__main__":
    print("This script is a utility module and cannot be executed directly.")