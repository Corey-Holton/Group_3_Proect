from pathlib import Path

# Local Imports
from .main import _audio_stem_separation
from ..print_utilities import print_message


def process_audio_stem_separation(
    input_file,
    model="htdemucs_ft",
    save_as_mp3=True,
    mp3_bitrate=320,
    use_float32=False,
    use_int24=False,
):
    """
    Process audio stems using Demucs.
    """
    try:
        # Output directory for stems
        output_directory = Path("./audio_processing/output_stems")

        # Separate audio into stems
        results = _audio_stem_separation(
            input_file,
            output_path=output_directory,
            model=model,
            mp3=save_as_mp3,
            mp3_rate=mp3_bitrate,
            float32=use_float32,
            int24=use_int24,
        )

        if results is None:
            raise RuntimeError("No results returned from `_audio_stem_separation`.")


        # Convert paths to strings for consistency
        paths = [str(path) for path in results]

        return paths

    except Exception as e:
        print_message("[ERROR]", text_color="bright_red")
        print_message(f"Error in `process_audio_stems`:", text_color="bright_red", indent_level=1)
        print_message(f"{e}", text_color="bright_red", indent_level=2, include_border=True)
        return None