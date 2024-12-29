from pathlib import Path
import subprocess as sp
import sys

# Local Imports
from ..print_utilities import print_title, print_message
from .constants import EXTENSIONS


def _find_audio_files(directory):
    """
    Find audio files in the input directory.

    Args:
        input_directory (str): Path to the directory containing audio files.

    Returns:
        list: List of audio file paths.
    """
    audio_files = []

    for file in Path(directory).iterdir():
        if file.suffix.lower().lstrip(".") in EXTENSIONS:
            audio_files.append(file)
    return audio_files


def _create_directory(path):
    """
    Create a directory if it does not exist.
    """
    path = Path(path)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        print_message("[DIR]", text_color="bright_yellow")
        print_message(f"Created output directory:", text_color="bright_yellow", indent_level=1)
        print_message(f"`{path}`", text_color="bright_yellow", indent_level=2, include_border=True)


def _validate_audio_file(file_path):
    """
    Validate the existence and extension of an audio file.
    """
    file = Path(file_path)
    if not file.exists() or file.suffix.lower().lstrip(".") not in EXTENSIONS:
        print_message("[ERROR]", text_color="bright_red")
        print_message(f"Invalid or missing audio file:", text_color="bright_red", indent_level=1)
        print_message(f"`{file_path}`", text_color="bright_red", indent_level=2, include_border=True)
        return False
    return True


def _execute_command(cmd):
    """
    Execute a shell command and handle stdout and stderr.
    """
    try:
        process = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
        stdout, stderr = process.communicate()

        if stdout:
            sys.stdout.write(stdout.decode())
        if stderr:
            sys.stderr.write(stderr.decode())

        if process.returncode != 0:
            raise RuntimeError("Command execution failed.")
        return True
    except Exception as e:
        print_message("[ERROR]", text_color="bright_red")
        print_message(f"Command execution error:", text_color="bright_red", indent_level=1)
        print_message(f"{e}", text_color="bright_red", indent_level=2, include_border=True)
        return False