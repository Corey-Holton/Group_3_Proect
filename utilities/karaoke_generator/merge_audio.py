from pydub import AudioSegment

def merge_audio_stems(
    bass_file, 
    drums_file, 
    other_file, 
    output_format="mp3", 
    output_path=None
):
    """
    Merge the bass, drums, and other stems into a single audio file.

    Args:
        bass_file (str): Path to the bass stem audio file.
        drums_file (str): Path to the drums stem audio file.
        other_file (str): Path to the other stem audio file.
        output_format (str): Desired output format (e.g., 'mp3', 'wav'). Default is 'mp3'.
        output_path (str): Base name for the output file (without extension). Default is 'fused_audio'.

    Returns:
        str: Full path to the merged audio file.
    """
    # Validate that all required audio stem paths are provided
    if not all([bass_file, drums_file, other_file]):
        raise ValueError("All stem files (bass, drums, other) must be provided.")

    try:
        # Step 1: Load the audio stems
        # Each stem (bass, drums, other) is loaded as an AudioSegment object
        stems = [AudioSegment.from_file(file) for file in [bass_file, drums_file, other_file]]

        # Step 2: Merge the stems by overlaying them sequentially
        # Start with the first stem (bass) and overlay the rest (drums, other) one by one
        merged_audio = stems[0]
        for stem in stems[1:]:
            merged_audio = merged_audio.overlay(stem)

        # Step 3: Define the output file path
        # Combine the output base name with the specified format (e.g., fused_audio.mp3)
        output_file = f"{output_path}.{output_format}"

        # Step 4: Export the merged audio to the specified format
        merged_audio.export(output_file, format=output_format)

        # Return the full path to the merged audio file
        return output_file

    except Exception as e:
        # Handle any errors that occur during processing or exporting
        raise RuntimeError(f"Failed to merge audio stems: {e}") from e
