# Note: Code has been modified and repurposed to work locally and with local hardware and computer.
# Original code obtained from https://colab.research.google.com/drive/1dC9nVxk3V_VPjUADsnFu8EiT-xnU1tGH?usp=sharing#scrollTo=79JbZGcAqX3p
# Reference Model Source from GitHub https://github.com/facebookresearch/demucs

"""
This script is designed to separate audio files into different stems using the Demucs model.
It has been modified and repurposed to work locally with local hardware and computer.

Original code obtained from:
https://colab.research.google.com/drive/1dC9nVxk3V_VPjUADsnFu8EiT-xnU1tGH?usp=sharing#scrollTo=79JbZGcAqX3p

Reference Model Source from GitHub:
https://github.com/facebookresearch/demucs
"""
from pathlib import Path

# Third-Party Libraries
import torch

# Local Imports
from ..print_utilities import print_title, print_message

from .utilities import (
    _create_directory, 
    _validate_audio_file, 
    _execute_command, 
)

from .constants import (
    DEFAULT_MODEL,
    DEFAULT_MP3_RATE,
)


def _audio_stem_separation(
    input_file,
    output_path,
    model=DEFAULT_MODEL,
    two_stems=None,
    mp3=True,
    mp3_rate=DEFAULT_MP3_RATE,
    float32=False,
    int24=False,
):
    """
    Separate an audio file into stems using the Demucs model.

    Args:
        input_file (str): Path to the input audio file.
        output_path (str): Path to the output directory.
        model (str): Model name to use for separation.
        two_stems (str, optional): Specify stems for separation.
        mp3 (bool, optional): Whether to output MP3 files.
        mp3_rate (int, optional): Bitrate for MP3 output.
        float32 (bool, optional): Whether to output float32 WAV files.
        int24 (bool, optional): Whether to output int24 WAV files.

    Returns:
        tuple: Paths to the separated audio stems. (other, vocals, bass, drums)
    """
    try:
        print_title("Separating Audio with Demucs")
        
        input_path = Path(input_file)
        output_path = Path(output_path)

        # Create the output directory if it does not exist
        _create_directory(output_path)

        # Validate the existence of the input file
        if not _validate_audio_file(input_path):
            return None
        
        # Set the device for processing the audio
        device = torch.device(
            f"cuda:{torch.cuda.current_device()}" if torch.cuda.is_available() else "cpu")
        
        # Prepare the command to execute the Demucs model
        cmd = [
            "python", "-m", "demucs.separate", 
            "-o", str(output_path), 
            "-n", model, 
            "--device", f"{device}"
        ]
        
        if mp3:
            cmd += ["--mp3", f"--mp3-bitrate={mp3_rate}"]

        if float32:
            cmd += ["--float32"]

        if int24:
            cmd += ["--int24"]

        if two_stems is not None:
            cmd += [f"--two-stems={two_stems}"]

        cmd.append(str(input_path))

        ## Print the list of files that will be processed
        print_message("[INFO]", text_color="bright_blue")
        print_message(f"Processing file:", text_color="bright_blue", indent_level=1)
        print_message(f"`{input_path.name}`", text_color="bright_blue", indent_level=2, include_border=True)

        # Print the full command being executed
        print_message("[CMD]", text_color="bright_cyan")
        print_message(f"`{' '.join(cmd)}`", text_color="bright_cyan", indent_level=1, include_border=True)

        # Execute the command to separate the audio stems using subprocess
        if not _execute_command(cmd):
            # Early exit if the command fails
            return None
        print_message("", include_border=True)

        # Prepare paths for output stems
        stems = ["other", "vocals", "bass", "drums"]
        stem_paths = [output_path / model / input_path.stem / f"{stem}{input_path.suffix}" for stem in stems]

        # Print the paths where the separated stems are saved
        print_message("[SUCCESS]", text_color="bright_green")
        print_message("Separated stems saved at:", text_color="bright_green", indent_level=1)
        for path in stem_paths:
            print_message(f"`{path}`", text_color="bright_green", indent_level=2)
        print_message("", include_border=True)

        return tuple(stem_paths)

    except Exception as e:
        # Print an error message if an exception occurs
        print_message("[ERROR]", text_color="bright_red")
        print_message(f"Error in `separate_audio`:", text_color="bright_red", indent_level=1)
        print_message(f"{e}", text_color="bright_red", indent_level=2, include_border=True)
        return None
    
if __name__ == "__main__":
    print("This script is designed to separate audio files into different stems using the Demucs model.")