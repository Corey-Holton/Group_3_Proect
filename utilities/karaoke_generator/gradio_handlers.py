from pathlib import Path
import json
import pandas as pd

# Local Imports
from ..print_utilities import print_message

from .extract_lyric_timing import extract_lyrics_with_timing
from .merge_audio import merge_audio_stems
from .generate_ass import create_ass_file
from .generate_video import generate_karaoke_video
from .utilities import extract_audio_duration

from .constants import (
    DEFAULT_OUTPUT_DIR_LYRICS_RAW,
    DEFAULT_OUTPUT_DIR_LYRICS_MODIFIED,
    DEFAULT_OUTPUT_DIR_INSTRUMENTAL,
    DEFAULT_OUTPUT_DIR_ASS,
    DEFAULT_OUTPUT_DIR_VIDEO
)

# ════════════════════════════════════════════════════════════
# Gradio Extract Raw Lyrics Handler
# ════════════════════════════════════════════════════════════
def process_audio_extract_lyric_timing(input_file, file_name):
    """
    Extract lyrics with timing metadata from an audio file.

    Args:
        input_file (str): Path to the vocals stem audio file.

    Returns:
        str: Path to the saved raw lyrics metadata JSON file.
    """

    if not file_name:
        raise ValueError("No file name provided. Please provide a valid file name.")
    
    output_directory = Path(DEFAULT_OUTPUT_DIR_LYRICS_RAW)
    output_directory.mkdir(parents=True, exist_ok=True)
    output_file = output_directory / f"{file_name}.json"

    try:
        # Extract lyrics metadata
        lyrics_metadata = extract_lyrics_with_timing(str(input_file))

        # Save raw metadata to JSON
        with open(output_file, "w") as f:
            json.dump(lyrics_metadata, f, indent=4)

        print_message(f"Raw lyrics metadata saved at: {output_file}", text_color="bright_green")
        return str(output_file), lyrics_metadata

    except Exception as e:
        print_message(f"Error during extraction: {e}", text_color="bright_red")
        return "An error occurred during lyric extraction."


# ════════════════════════════════════════════════════════════
# Gradio Modify Lyrics Metadata Handler
# ════════════════════════════════════════════════════════════
def load_lyrics_metadata(metadata_file):
    """
    Load the lyrics metadata and format it for editing in a table.

    Args:
        metadata_file (str): Path to the metadata JSON file.

    Returns:
        list: List of tuples with word properties for display in a table.
    """
    try:
        # Load the metadata from the JSON file
        with open(metadata_file, "r") as f:
            metadata = json.load(f)

        words = [
            (
                verse.get("verse_number"), # Verse Number
                word.get("word_number"),   # Word Number
                word.get("word"),          # Word
                word.get("start"),         # Start Time
                word.get("end"),           # End Time
                word.get("probability")    # Probability
            )
            for verse in metadata
            for word in verse.get("words", [])
        ]
        return words
    
    except Exception as e:
        print_message(f"Error loading metadata: {e}", text_color="bright_red")
        return []


def save_modified_lyrics(metadata_file, modified_words):
    """
    Save modified lyrics back to the original metadata structure and file.

    Args:
        metadata_file (str): Path to the original metadata JSON file.
        modified_words (DataFrame or list): Modified words from the user.

    Returns:
        str: Path to the saved modified metadata JSON file.
    """
    try:
        # Convert DataFrame to list of lists if needed
        if isinstance(modified_words, pd.DataFrame):
            modified_words = modified_words.values.tolist()

        # Load original metadata from JSON file
        with open(metadata_file, "r") as f:
            metadata = json.load(f)

        # Update words in the metadata structure
        word_index = 0
        for verse in metadata:
            for word in verse.get("words", []):
                if word_index < len(modified_words):
                    word["word"] = modified_words[word_index][2]  # Update the Word column (index 2)
                word_index += 1

        # Save updated metadata to JSON
        output_directory = Path(DEFAULT_OUTPUT_DIR_LYRICS_MODIFIED)
        output_directory.mkdir(parents=True, exist_ok=True)
        output_file = output_directory / f"{Path(metadata_file).stem}.json"

        # Save the modified metadata to a new JSON file
        with open(output_file, "w") as f:
            json.dump(metadata, f, indent=4)

        print_message(f"Modified lyrics metadata saved at: {output_file}", text_color="bright_green")
        return str(output_file), metadata

    except Exception as e:
        print_message(f"Error while saving modified metadata: {e}", text_color="bright_red")
        return "An error occurred while saving the modified metadata."


# ════════════════════════════════════════════════════════════
# Gradio Merge Audio Handler
# ════════════════════════════════════════════════════════════
""" 
What we will need:
INPUT
1. bass file
2. drum file
3. instrumental file
4. output format

OUTPUT
5. output path to save instrumental audio

"""
def process_audio_merging(
    bass_file, 
    drums_file, 
    instrumental_file, 
    output_format="mp3", 
):
    
    output_directory = Path(DEFAULT_OUTPUT_DIR_INSTRUMENTAL)
    output_directory.mkdir(parents=True, exist_ok=True)
    output_file = output_directory / f"{Path(instrumental_file).stem}_instrumental.{output_format}"

    try:
        output_file = merge_audio_stems(
            bass_file, 
            drums_file, 
            instrumental_file, 
            output_format=output_format, 
            output_path=output_file
        )

        print_message(f"Instrumental audio saved at: {output_file}", text_color="bright_green")
        return str(output_file)
    
    except Exception as e:
        print_message(f"Error during audio merging: {e}", text_color="bright_red")
        return "An error occurred during audio merging."


# ════════════════════════════════════════════════════════════
# Gradio Create Video Handler
# ════════════════════════════════════════════════════════════

def process_karaoke_creation(
    input_file_instrumental,
    input_file_lyrics_metadata,
    file_name,

    # ASS file creation parameters
    font="Arial",
    fontsize=10,
    title="Karaoke Title",

    # Video creation parameters
    resolution="1280x720",
    preset="fast",
    crf=23,
    fps=24,
    bitrate="3000k",
    audio_bitrate="192k"
):
    """
    Create a karaoke video by generating an ASS file and combining it with instrumental audio.

    Args:
        input_file_instrumental (str): Path to the instrumental audio file.
        input_file_lyrics_metadata (str): Path to the lyrics metadata JSON file.
        file_name (str): Name for the output files (ASS and video).
        font (str): Font for the lyrics in the video.
        fontsize (int): Font size for the lyrics.
        title (str): Title for the karaoke video.
        resolution (str): Resolution of the output video (e.g., "1280x720").
        preset (str): FFmpeg encoding preset for speed/quality tradeoff.
        crf (int): Quality setting for video encoding (lower is better).
        fps (int): Frames per second for the video.
        bitrate (str): Video bitrate for quality control.
        audio_bitrate (str): Audio bitrate for quality control.

    Returns:
        str: Path to the generated karaoke video.
    """
    try:
        # Create directories for ASS and video output
        output_ass_directory = Path(DEFAULT_OUTPUT_DIR_ASS)
        output_ass_directory.mkdir(parents=True, exist_ok=True)
        karaoke_ass_file = output_ass_directory / f"{file_name}.ass"

        output_video_directory = Path(DEFAULT_OUTPUT_DIR_VIDEO)
        output_video_directory.mkdir(parents=True, exist_ok=True)
        karaoke_video_file = output_video_directory / f"{file_name}.mp4"

        # Extract audio duration
        print_message("[INFO] Extracting audio duration", text_color="bright_blue")
        audio_duration = extract_audio_duration(input_file_instrumental)
        if audio_duration is None:
            raise ValueError(f"Could not extract audio duration from {input_file_instrumental}")
        
        # Load lyrics metadata from JSON
        print_message("[INFO] Loading lyrics metadata", text_color="bright_blue")
        with open(input_file_lyrics_metadata, "r") as f:
            lyrics_metadata = json.load(f)

        # Create ASS file
        print_message("[INFO] Creating ASS file", text_color="bright_blue")
        create_ass_file(
            lyrics_metadata,
            output_path=karaoke_ass_file,
            audio_duration=audio_duration,
            font=font,
            fontsize=fontsize,
            title=title,
        )
        print_message(f"[SUCCESS] ASS file created: {karaoke_ass_file}", text_color="bright_green")

        # Generate Karaoke Video
        print_message("[INFO] Generating Karaoke Video", text_color="bright_blue")
        generate_karaoke_video(
            audio_path=str(input_file_instrumental),
            ass_path=str(karaoke_ass_file).replace("\\", "/"),
            output_path=str(karaoke_video_file),
            resolution=resolution,
            preset=preset,
            crf=crf,
            fps=fps,
            bitrate=bitrate,
            audio_bitrate=audio_bitrate,
        )
        print_message(f"[SUCCESS] Karaoke video created: {karaoke_video_file}", text_color="bright_green")

        return str(karaoke_video_file)

    except FileNotFoundError as e:
        print_message(f"[ERROR] File not found: {e}", text_color="bright_red")
    except ValueError as e:
        print_message(f"[ERROR] Invalid input: {e}", text_color="bright_red")
    except Exception as e:
        print_message(f"[ERROR] An unexpected error occurred: {e}", text_color="bright_red")
    return "An error occurred during karaoke creation."
