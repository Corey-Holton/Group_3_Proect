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
from .constants import EXTENSIONS


def _audio_stem_separation(
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
    Separate an audio file into stems using the Demucs model.
    """
    try:
        print_title("Separating Audio with Demucs")
        
        input_path = Path(input_file)
        output_path = Path(output_path)

        # Validate input file and prepare output directory
        _create_directory(output_path)

        if not _validate_audio_file(input_path):
            return None

        # Prepare the command
        device = torch.device(
            f"cuda:{torch.cuda.current_device()}" if torch.cuda.is_available() else "cpu")
        
        cmd = ["python", "-m", "demucs.separate", "-o",str(output_path), "-n", model, "--device", f"{device}"]
        if mp3:
            cmd += ["--mp3", f"--mp3-bitrate={mp3_rate}"]
        if float32:
            cmd += ["--float32"]
        if int24:
            cmd += ["--int24"]
        if two_stems is not None:
            cmd += [f"--two-stems={two_stems}"]
        cmd.append(str(input_path))

        # Check if the file exists and has a valid extension
        if not input_path.exists() or input_path.suffix.lower().lstrip(".") not in EXTENSIONS:
            print_message("[ERROR]", text_color="bright_red")
            print_message("No valid audio file found at:", text_color="bright_red", indent_level=1)
            print_message(f"`{input_file}`", text_color="bright_red", indent_level=2, include_border=True)
            return

        # Execute the command
        print_message("[INFO]", text_color="bright_blue")
        print_message(f"Processing file:", text_color="bright_blue", indent_level=1)
        print_message(f"`{input_path.name}`", text_color="bright_blue", indent_level=2, include_border=True)

        print_message("[CMD]", text_color="bright_cyan")
        print_message(f"`{' '.join(cmd)}`", text_color="bright_cyan", indent_level=1, include_border=True)

        if not _execute_command(cmd):
            return None
        print_message("", include_border=True)

        # Prepare paths for output stems
        stems = ["other", "vocals", "bass", "drums"]
        stem_paths = [output_path / model / input_path.stem / f"{stem}{input_path.suffix}" for stem in stems]

        print_message("[SUCCESS]", text_color="bright_green")
        print_message("Separated stems saved at:", text_color="bright_green", indent_level=1)
        for path in stem_paths:
            print_message(f"`{path}`", text_color="bright_green", indent_level=2)
        print_message("", include_border=True)

        return tuple(stem_paths)

    except Exception as e:
        print_message("[ERROR]", text_color="bright_red")
        print_message(f"Error in `separate_audio`:", text_color="bright_red", indent_level=1)
        print_message(f"{e}", text_color="bright_red", indent_level=2, include_border=True)
        return None