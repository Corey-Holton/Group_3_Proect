from ..print_utilities import print_title, print_message
from pathlib import Path
from .main import _midi_style_conversion
from .prompt_config import _execute_query

from .constants import DEFAULT_OUTPUT_DIR


def process_midi_style_conversion(
    # ! Parameters here are handled in the Gradio Interface.
    # ! The order of parameters MUST match the Gradio interface to function correctly.
    input_midi_file,
    song_dir_name=False,
    song_prefix_name=False,
    text_prompt=None
):
    """
    Modify a MIDI file based on a text query.

    Args:
        input_midi_file (str): Path to the input MIDI file.
        song_dir_name (str): Name of the directory for saving modified MIDI files.
        song_prefix_name (str): Prefix name for the output file.
        text_prompt (str, optional): Text prompt to describe modifications.

    Returns:
        str: Path to the modified MIDI file.
    """
    print_title("Modifing MIDI File", text_color="bright_white")

    # If no song directory name is provided, return an error message
    if not song_dir_name:
        print_message("[ERROR]", text_color="bright_red")
        print_message("Song directory name is required.", text_color="bright_red", indent_level=1, include_border=True)
        return
    
    # If no song prefix name is provided, return an error message
    if not song_prefix_name:
        print_message("[ERROR]", text_color="bright_red")
        print_message("Song prefix name is required.", text_color="bright_red", indent_level=1, include_border=True)
        return
    
    # Define the output MIDI file path
    output_midi_path = f"{DEFAULT_OUTPUT_DIR}/{song_dir_name}/{song_prefix_name}_{Path(input_midi_file).stem}.mid"

    # Validate input MIDI file path
    input_path = Path(input_midi_file)

    # Check if the input MIDI file exists and has a valid extension
    if not input_path.exists() or input_path.suffix.lower() != ".mid":
        print_message("[ERROR]", text_color="bright_red")
        print_message("Invalid MIDI file.", text_color="bright_red", indent_level=1, include_border=True)
        return

    # Validate output path and create the directory if it does not exist
    output_dir = Path(output_midi_path).parent
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
        print_message("[DIR]", text_color="bright_yellow")
        print_message("Created output directory:", text_color="bright_yellow", indent_level=1)
        print_message(f"`{output_dir}`", text_color="bright_yellow", indent_level=2, include_border=True)

    # Display user query prompt
    if text_prompt:
        print_message("[PROMPT]", text_color="bright_cyan")
        print_message("User Input:", text_color="bright_cyan", indent_level=1)
        print_message(f"`{text_prompt}`", text_color="bright_cyan", indent_level=2, include_border=True)

    try:
        # Execute query using the text prompt
        query_params = _execute_query(text_prompt)

    except Exception as e:
        # Print error message if query execution fails
        print_message("[ERROR]", text_color="bright_red")
        print_message("Failed to process query.", text_color="bright_red", indent_level=1, include_border=True)
        return

    # Modify MIDI file using provided parameters
    try:
        # Ensure instruments keys are integers
        query_params['instruments'] = {int(k): v for k, v in query_params['instruments'].items()}

        # Modify the MIDI file based on the query parameters received by Google's AI model
        _midi_style_conversion(input_midi_file, output_midi_path, **query_params)

        # Print success message if MIDI modification is successful
        print_message("[SUCCESS]", text_color="bright_green")
        print_message("Modified MIDI saved to:", text_color="bright_green", indent_level=1)
        print_message(f"`{output_midi_path}`", text_color="bright_green", indent_level=2, include_border=True)

    except Exception as e:
        # Print error message if MIDI modification fails
        print_message("[ERROR]", text_color="bright_red")
        print_message("MIDI modification failed:", text_color="bright_red", indent_level=1)
        print_message(f"`{e}`", text_color="bright_red", indent_level=2, include_border=True)

    return output_midi_path