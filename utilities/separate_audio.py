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

Summary:
- The main function `separate_audio` takes an input audio file and separates it into different stems (e.g., vocals, drums, bass, and other).
- The separated audio files are saved in the specified output directory.
- The script uses the Demucs model for audio source separation.
- Helper functions are provided to find audio files in a directory and handle process streams.

Usage:
- Call the `separate_audio` function with the path to the input audio file and the desired output directory.
- Customize the parameters of the `separate_audio` function as needed to suit your requirements.
"""

from pathlib import Path
import subprocess as sp
import sys

# Third-Party Imports
import torch

# Local Imports
from .print_utilities import print_title, print_line


# Constants
EXTENSIONS = ["mp3", "wav", "ogg", "flac"]


# Helper Functions
def _find_files(input_directory):
    """
    Find audio files in the input directory.

    Args:
        input_directory (str): Path to the directory containing audio files.

    Returns:
        list: List of audio file paths.
    """
    audio_files = []

    for file in Path(input_directory).iterdir():
        if file.suffix.lower().lstrip(".") in EXTENSIONS:
            audio_files.append(file)
    return audio_files


def _copy_process_streams(process: sp.Popen):
    """
    Handle the I/O streams of the process, capturing stdout and stderr.

    Args:
        process (subprocess.Popen): The process whose streams are to be handled.
    """
    stdout, stderr = process.communicate()

    if stdout:
        sys.stdout.write(stdout.decode())

    if stderr:
        sys.stderr.write(stderr.decode())


# Main Function
def separate_audio(
        input_file,
        output_path="./audio_processing/output_stems",
        model="htdemucs_ft",
        two_stems=None,
        mp3=True,
        mp3_rate=320,
        float32=False,
        int24=False,
):
    """
    Separate audio files using the Demucs model.

    Args:
        input_file (str): Path to the input audio file.
        output_path (str): Path to the output directory.
        model (str): Model name to use for separation.
        two_stems (str, optional): Specify stems for separation.
        mp3 (bool, optional): Whether to output MP3 files.
        mp3_rate (int, optional): Bitrate for MP3 output.
        float32 (bool, optional): Whether to output float32 WAV files.
        int24 (bool, optional): Whether to output int24 WAV files.
    """
    print_title("[STEP 1] Separating Audio with Demucs", text_color="bright_white")

    inp = Path(input_file)
    outp = Path(output_path)

    # Create the output directory if it does not exist
    if not outp.exists():
        outp.mkdir(parents=True, exist_ok=True)
        print_line(f"[DIR] \n\tCreated output directory: \n\t\t{outp}", text_color="yellow")

    device = torch.device(
        f"cuda:{torch.cuda.current_device()}" if torch.cuda.is_available() else "cpu")

    # Create the command that will execute the Demucs model for separation
    cmd = ["python", "-m", "demucs.separate", "-o",str(outp), "-n", model, "--device", f"{device}"]
    if mp3:
        cmd += ["--mp3", f"--mp3-bitrate={mp3_rate}"]
    if float32:
        cmd += ["--float32"]
    if int24:
        cmd += ["--int24"]
    if two_stems is not None:
        cmd += [f"--two-stems={two_stems}"]

    # Check if the file exists and has a valid extension
    if not inp.exists() or inp.suffix.lower().lstrip(".") not in EXTENSIONS:
        print_line(f"[ERROR] \n\tNo valid audio file at {input_file}", text_color="bright_red")
        return

    # Print the list of files that will be processed
    print_line(f"[INFO] \n\tSeparating the audio file `{inp.stem}{inp.suffix}`", text_color="bright_blue")

    # Print the full command being executed
    print_line(f"[CMD] \n\t`{' '.join(cmd)}`", text_color="bright_cyan")

    # Execute the separation command using subprocess
    p = sp.Popen(cmd + [str(inp)], stdout=sp.PIPE, stderr=sp.PIPE)

    # Handle the process output (stdout, stderr)
    _copy_process_streams(p)

    # Wait for the process to finish
    p.wait()

    # Check the return code to see if the command ran successfully
    if p.returncode != 0:
        print_line(f"[ERROR] \n\tCommand failed, something went wrong.", text_color="bright_red")

    print_line(" ")

    stems = ["other", "vocals", "bass", "drums"]
    stem_paths = [Path(f"{outp}/{model}/{inp.stem}/{stem}{inp.suffix}") for stem in stems ]
    
    print_line(f"[SUCCESS] \n\tSeparated audio files saved in: \n\t\t{stem_paths[0]} \n\t\t{stem_paths[1]} \n\t\t{stem_paths[2]} \n\t\t{stem_paths[3]}", text_color="bright_green")

    return tuple(stem_paths)