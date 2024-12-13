# Torch for deep learning models
import torch

# File and directory handling
from pathlib import Path
from shutil import rmtree

# Subprocess for running shell commands
import subprocess as sp

# System-specific parameters and functions
import sys

# Import Custom Print Utilities
from .print_utils import print_title, print_line

# Define the list of audio file extensions we want to process
EXTENSIONS = ["mp3", "wav", "ogg", "flac"]

# Define the find_files function to find audio files in the input directory
def _find_files(input_directory):
    audio_files = []

    # Path(in_path).iterdir() iterates over all files in the directory specified by in_path
    for file in Path(input_directory).iterdir():

        # Check if the file extension is in the list of extensions we want to process
        if file.suffix.lower().lstrip(".") in EXTENSIONS:
            audio_files.append(file)
    return audio_files

# Define the copy_process_streams function
def _copy_process_streams(process: sp.Popen):
    # communicate() handles the I/O streams of the process, capturing stdout and stderr
    stdout, stderr = process.communicate()

    # Print the outputs to the console
    if stdout:
        # Write standard output (stdout) to the console
        sys.stdout.write(stdout.decode())
    if stderr:
        # Write errors (stderr) to the console
        sys.stderr.write(stderr.decode())

# The main separation function to separate audio files
def separate_audio(
        input_file,
        out_path="./output/demucs",
        model='htdemucs_ft',
        two_stems=None,
        mp3=True,
        mp3_rate=320,
        float32=False,
        int24=False,
):
    print_title("Separating Audio with Demucs", text_color="bright_white")

    inp = Path(input_file)
    outp = Path(out_path)

    device = torch.device(
        f"cuda:{torch.cuda.current_device()}" if torch.cuda.is_available() else "cpu")

    # Create the command that will execute the Demucs model for separation
    cmd = ["python", "-m", "demucs.separate", "-o", str(outp), "-n", model, "--device", f"{device}"]
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
    print_line(f"[INFO] \n\tGoing to separate the audio file `{str(input_file).split('/')[-1]}`", text_color="bright_blue")

    # Print the full command being executed
    print_line(f"[CMD] \n\t`{' '.join(cmd)}`", text_color="bright_green")

    # Execute the separation command using subprocess
    p = sp.Popen(cmd + [str(inp)], stdout=sp.PIPE, stderr=sp.PIPE)

    # Handle the process output (stdout, stderr)
    _copy_process_streams(p)

    # Wait for the process to finish
    p.wait()
    print_line(" ")

    # Check the return code to see if the command ran successfully
    if p.returncode != 0:
        print_line(f"[ERROR] \n\tCommand failed, something went wrong.", text_color="bright_red")
