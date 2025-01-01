import torch
import subprocess
from .utilities import extract_audio_duration, validate_file
from ..print_utilities import print_message

def generate_karaoke_video(
    audio_path,
    ass_path,
    output_path,
    resolution="1280x720",
    preset="fast",
    crf=23,
    fps=24,
    bitrate="3000k",
    audio_bitrate="192k"
):
    """
    Generate a karaoke video with a black background, utilizing GPU acceleration if available.

    Parameters:
    - audio_path (str): Path to the input audio file.
    - ass_path (str): Path to the ASS subtitle file.
    - output_path (str): Path to save the generated video.
    - resolution (str): Video resolution (default: "1280x720").
    - preset (str): FFmpeg encoding preset for speed/quality tradeoff (default: "fast").
    - crf (int): Quality setting for video encoding (lower is better, default: 23).
    - fps (int): Frames per second for the video (default: 24).
    - bitrate (str): Video bitrate for quality control (default: "3000k").
    - audio_bitrate (str): Audio bitrate for output quality (default: "192k").
    """

    # Validate input files
    if not validate_file(audio_path) or not validate_file(ass_path):
        return

    # Check for GPU availability
    if torch.cuda.is_available():
        # Use NVIDIA NVENC for GPU acceleration
        device = torch.cuda.get_device_name(0)
        print(f"✅ GPU detected: {device}")
        video_codec = "h264_nvenc"  
    else:
        # Use CPU codec
        print("⚠️ No GPU detected. Falling back to CPU.")
        video_codec = "libx264"  

    # Get audio duration
    audio_duration = extract_audio_duration(audio_path)
    if audio_duration is None:
        print("❌ Unable to retrieve audio duration. Aborting.")
        return

    # Build FFmpeg command
    command = [
        "ffmpeg",
        "-y",  # Overwrite output
        "-f", "lavfi",
        f"-i", f"color=c=black:s={resolution}:d={audio_duration}",  # Black background
        "-i", audio_path,  # Audio input
        "-vf", f"subtitles={ass_path}",  # Add subtitles
        "-c:v", video_codec,  # Select GPU or CPU codec
        "-preset", preset,  # Encoding preset
        "-crf", str(crf),  # Quality level
        "-r", str(fps),  # Frame rate
        "-b:v", bitrate,  # Video bitrate
        "-c:a", "aac",  # Audio codec
        "-b:a", audio_bitrate,  # Audio bitrate
        "-shortest",  # Match shortest stream
        output_path  # Output file
    ]

    # Debugging: Print the constructed command
    print("\nRunning FFmpeg command:")
    print(" ".join(command))

    # Execute FFmpeg command
    try:
        subprocess.run(command, check=True)
        print(f"✅ Video successfully created at: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg error: {e.stderr}")