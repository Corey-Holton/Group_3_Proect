from ..print_utilities import print_title, print_message
from pathlib import Path
from .main import modify_midi
from .prompt_config import execute_query


def process_midi_style_conversion(input_midi_file, song_dir_name=False, song_prefix_name=False, text_prompt=None):
    """
    Prompts the user for parameters to modify a MIDI file based on a text query.

    Args:
        input_midi_file (str): Path to input MIDI file.
        output_midi_path (str): Path to save the modified MIDI file.
        text_prompt (str): Text prompt to describe modifications.

    Returns:
        None
    """
    print_title("Modifing MIDI File", text_color="bright_white")

    if not song_dir_name:
        print_message("[ERROR]", text_color="bright_red")
        print_message("Song directory name is required.", text_color="bright_red", indent_level=1, include_border=True)
        return

    if not song_prefix_name:
        print_message("[ERROR]", text_color="bright_red")
        print_message("Song prefix name is required.", text_color="bright_red", indent_level=1, include_border=True)
        return

    output_midi_path = f"./audio_processing/output_midi_mods/{song_dir_name}/{song_prefix_name}_{Path(input_midi_file).stem}.mid"

    # Validate input MIDI file
    input_path = Path(input_midi_file)
    if not input_path.exists() or input_path.suffix.lower() != ".mid":
        print_message("[ERROR]", text_color="bright_red")
        print_message("Invalid MIDI file.", text_color="bright_red", indent_level=1, include_border=True)
        return

    # Validate output path
    output_dir = Path(output_midi_path).parent
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
        print_message("[DIR]", text_color="bright_yellow")
        print_message("Created output directory:", text_color="bright_yellow", indent_level=1)
        print_message(f"`{output_dir}`", text_color="bright_yellow", indent_level=2, include_border=True)

    # Display user query
    if text_prompt:
        print_message("[PROMPT]", text_color="bright_cyan")
        print_message("User Input:", text_color="bright_cyan", indent_level=1)
        print_message(f"`{text_prompt}`", text_color="bright_cyan", indent_level=2, include_border=True)

    # Execute query using the text prompt
    try:
        query_params = execute_query(text_prompt)
    except Exception as e:
        print_message("[ERROR]", text_color="bright_red")
        print_message("Failed to process query.", text_color="bright_red", indent_level=1, include_border=True)
        return

    # Modify MIDI file using provided parameters
    try:
        # Ensure instruments keys are integers
        query_params['instruments'] = {int(k): v for k, v in query_params['instruments'].items()}
        modify_midi(input_midi_file, output_midi_path, **query_params)
        print_message("[SUCCESS]", text_color="bright_green")
        print_message("Modified MIDI saved to:", text_color="bright_green", indent_level=1)
        print_message(f"`{output_midi_path}`", text_color="bright_green", indent_level=2, include_border=True)

    except Exception as e:
        print_message("[ERROR]", text_color="bright_red")
        print_message("MIDI modification failed:", text_color="bright_red", indent_level=1)
        print_message(f"`{e}`", text_color="bright_red", indent_level=2, include_border=True)

    return output_midi_path