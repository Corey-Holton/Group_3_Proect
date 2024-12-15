"""
This script sets up a Gradio interface to process audio files by separating them into stems using the Demucs model
and converting the "other" stem to MIDI using the Basic Pitch model.

Summary:
- The main function `gradio_pipeline` takes an input audio file, separates it into stems, and converts the "other" stem to MIDI.
- The separated audio files and the generated MIDI file are returned as outputs.

Usage:
- Run this script to launch the Gradio interface.
- Upload an audio file and specify the Demucs model to use for separation.
"""


# ══════════════════════════
# Imports
# ══════════════════════════

# Standard Library Imports
from pathlib import Path


# Third-party imports
import gradio as gr


# Local imports
from utilities import separate_audio, audio_to_midi, print_line

# ══════════════════════════
# Functionality Pipeline
# ══════════════════════════

def gradio_pipeline(
    input_file,

    # Parameters for `separate_audio`
    model="htdemucs_ft",
    two_stems=None,
    mp3=True,
    mp3_rate=320,
    float32=False,
    int24=False,

    # Parameters for `audio_to_midi`
    save_midi=True,
    sonify_midi=False,
    save_model_outputs=False,
    save_notes=False,
    onset_threshold=0.5,
    frame_threshold=0.3,
    minimum_note_length=127.70,
    minimum_frequency=None,
    maximum_frequency=None,
    multiple_pitch_bends=False,
    melodia_trick=True,
    debug_file=None,
    sonification_samplerate=44100,
    midi_tempo=120,
):
    """
    Full pipeline function to process audio files by separating them into stems and converting the "other" stem to MIDI.
    """

    # Input Song Name
    song_name = Path(input_file).stem

    # Output path for audio stems
    output_path_stems = "./audio_processing/output_stems"

    # Step 1: Separate Audio Stems using Demucs Model
    results = separate_audio(
        input_file,
        output_path=output_path_stems,
        model=model,
        two_stems=two_stems,
        mp3=mp3,
        mp3_rate=mp3_rate,
        float32=float32,
        int24=int24,
    )

    # Check if results are returned
    if results is None:
        return print_line("[ERROR] \n\tNo results returned from `separate_audio`.", text_color="red")

    # Unpack audio stems paths from results
    other_stem_path, voice_stem_path, bass_stem_path, drums_stem_path = results

    # Output path for MIDI
    output_path_midi = f"./audio_processing/output_midi/{song_name}"

    # Step 2: Convert "other" stem to MIDI
    midi_file_path = audio_to_midi(
        audio_path=other_stem_path,
        output_directory=output_path_midi,
        save_midi=save_midi,
        sonify_midi=sonify_midi,
        save_model_outputs=save_model_outputs,
        save_notes=save_notes,
        onset_threshold=onset_threshold,
        frame_threshold=frame_threshold,
        minimum_note_length=minimum_note_length,
        minimum_frequency=minimum_frequency,
        maximum_frequency=maximum_frequency,
        multiple_pitch_bends=multiple_pitch_bends,
        melodia_trick=melodia_trick,
        debug_file=debug_file,
        sonification_samplerate=sonification_samplerate,
        midi_tempo=midi_tempo,
    )

    # Return both files for Gradio output
    return str(other_stem_path), str(midi_file_path)

# ══════════════════════════
# Gradio Interface
# ══════════════════════════

inputs = [
    gr.Audio(
        type="filepath",
        label="Upload Audio File"
    ),

    gr.Textbox(
        value="htdemucs_ft",
        label="Demucs Model"
    ),
]

outputs = [
    gr.File(
        type="filepath",
        label="Separated Audio (Other)"
    ),

    gr.File(
        type="filepath",
        label="Separated Audio (Other)"
    ),
]

# ══════════════════════════
# Launch Gradio Interface
# ══════════════════════════

interface = gr.Interface(
    fn=gradio_pipeline,
    inputs=inputs,
    outputs=outputs
)

interface.launch()
