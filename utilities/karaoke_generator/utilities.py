import subprocess
import time
import os
from colorama import Fore, Style


def extract_audio_duration(audio_path):
    """
    Get the duration of an audio file using ffprobe.
    """
    try:
        # Run the ffprobe command to extract the duration of the audio file
        result = subprocess.run(
            [
                "ffprobe",                              # Command to run ffprobe
                "-i", audio_path,                       # Input file path
                "-show_entries", "format=duration",     # Request only the duration metadata
                "-v", "quiet",                          # Suppress unnecessary output
                "-of", "csv=p=0"                        # Format the output as plain CSV with no headers
            ],
            stdout=subprocess.PIPE,                     # Capture the standard output
            stderr=subprocess.PIPE,                     # Capture the standard error
            check=True                                  # Raise CalledProcessError if the command fails
        )

        # Decode the stdout result to a string, strip whitespace, and convert to float
        duration = float(result.stdout.decode("utf-8").strip())
        return duration  # Return the duration in seconds

    except subprocess.CalledProcessError as e:
        # Handle errors from ffprobe (e.g., if the command fails or the file is invalid)
        raise RuntimeError(f"ffprobe failed: {e.stderr.decode('utf-8')}") from e

    except ValueError as e:
        # Handle cases where the output cannot be converted to a float
        raise ValueError("Invalid duration format received from ffprobe.") from e

    except Exception as e:
        # Handle any other unexpected errors
        raise RuntimeError(f"Unexpected error: {e}") from e


def display_verses_with_timing(verses):
    """
    Displays verses with word-level timings.

    Args:
        verses (list): List of verses with text and timing metadata.
    """
    start_time = time.time()  # Track the start time for synchronization

    for verse in verses:
        # Wait until the verse's start time
        while time.time() - start_time < verse["words"][0]["start"]:
            time.sleep(0.01)

        for word in verse["words"]:
            # Highlight the current word and reset styles for others
            highlighted_text = " ".join(
                f"{Fore.YELLOW}{w['word']}{Style.RESET_ALL}" if w == word else w["word"]
                for w in verse["words"]
            )

            # Update the console output dynamically
            print(f"\r{highlighted_text}", end="", flush=True)

            # Wait until the current word's end time
            while time.time() - start_time < word["end"]:
                time.sleep(0.01)

        # Move to a new line after the verse
        print("\n")  


def validate_file(path, file_type="file"):
    """
    Validates the existence of a file or directory.

    Args:
        path (str): Path to validate.
        file_type (str): Type of validation ('file' or 'directory').

    Returns:
        bool: True if the file or directory exists, False otherwise.
    """
    if file_type == "file" and not os.path.isfile(path):
        print(f"❌ {file_type.capitalize()} not found: {path}")
        return False
    
    if file_type == "directory" and not os.path.isdir(path):
        print(f"❌ {file_type.capitalize()} not found: {path}")
        return False
    
    return True
