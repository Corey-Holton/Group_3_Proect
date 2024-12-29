# Standard Library Imports
from pathlib import Path

# Third-Party Imports
from faster_whisper import WhisperModel
from deep_translator import GoogleTranslator

# Local Imports
from .constants import DEVICE, COMPUTE_TYPE, MODEL_SIZE
from ..print_utilities import print_title, print_message

# Initialize Whisper model globally to avoid reloading it multiple times
MODEL = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)


def _extract_lyrics(audio_file):
    """
    Extract lyrics from an audio file using the Whisper model.

    :param audio_file: Path to the audio file.
    :return: List of lyrics strings.
    """
    audio_file = Path(audio_file)

    print_title("Extracting Lyrics from Audio")

    print_message("[INFO] Model Configuration", text_color="bright_blue")
    print_message(f"Device: \t{DEVICE}", text_color="bright_blue", indent_level=1)
    print_message(f"Compute Type: \t{COMPUTE_TYPE}", text_color="bright_blue", indent_level=1)
    print_message(f"Model Size: \t{MODEL_SIZE}", text_color="bright_blue", indent_level=1, include_border=True)

    print_message("[INFO] Processing Audio File", text_color="bright_blue")
    print_message(f"`{audio_file.name}`", text_color="bright_blue", indent_level=1, include_border=True)

    # Transcribe audio file
    segments, info = MODEL.transcribe(audio_file, beam_size=1)

    print_message("[TRANSCRIPTION DETAILS]", text_color="bright_cyan")
    print_message(f"Detected Language: \t{info.language}", text_color="bright_cyan", indent_level=1)
    print_message(f"Language Probability: \t{info.language_probability:.2f}", text_color="bright_cyan", indent_level=1, include_border=True)

    # Collect and return lyrics
    lyrics = [segment.text for segment in segments]
    return lyrics


def _translate_lyrics(lyrics, target_language):
    """
    Translate extracted lyrics into the target language.

    :param lyrics: List of strings representing lyrics.
    :param target_language: Target language code (e.g., 'en' for English).
    :return: List of translated lyrics strings.
    """
    print_title("Translating Lyrics")
    translator = GoogleTranslator(target=target_language)
    return [translator.translate(line) for line in lyrics]
