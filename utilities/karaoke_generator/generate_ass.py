def format_time(seconds):
    """Convert time in seconds to ASS format (h:mm:ss.cs)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    return f"{hours}:{minutes:02}:{seconds:05.2f}"


def write_section(file, section_name, content):
    """Write a named section to the ASS file."""
    # Write the section name enclosed in brackets, e.g., [Script Info] or [V4+ Styles]
    file.write(f"[{section_name}]\n")
    
    # Write the content associated with this section
    file.write(content)
    
    # Add a blank line after the section for proper formatting
    file.write("\n")


def write_script_info(file, title="Karaoke Subtitles"):
    """Write the script information section."""
    # Create the content for the script info section, including the title and script type
    content = f"Title: {title}\nScriptType: v4.00+\nPlayDepth: 0\n"
    
    # Write the script info section using the `write_section` helper
    write_section(file, "Script Info", content)


def write_styles(file, font="Arial", fontsize=48):
    """Write the styles section."""
    # Define the content for the styles section, including format and default style settings
    content = (
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
        "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
        "Alignment, MarginL, MarginR, MarginV, Encoding\n"
        f"Style: Default,{font},{fontsize},&H00FFFFFF,&H00FFFF00,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,3,0,5,0,0,0,1\n"
    )
    
    # Write the styles section using the `write_section` helper
    write_section(file, "V4+ Styles", content)


def write_events_header(file):
    """Write the header for the events section."""
    # Define the header for the events section, listing the format of dialogue events
    content = "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    
    # Write the events header using the `write_section` helper
    write_section(file, "Events", content)


def write_dialogue(file, start, end, text, style="Default", margin_l=0, margin_r=0, margin_v=0):
    """Write a single dialogue event."""
    # Write a dialogue event in the ASS format with specified start and end times,
    # text content, and optional margins and style
    file.write(
        f"Dialogue: 0,{format_time(start)},{format_time(end)},{style},,{margin_l},{margin_r},{margin_v},,{text}\n"
    )


def write_title_event(file, title, title_duration, screen_height, fontsize=72):
    """Write the title event."""

    # Calculate vertical margin for the title, placing it at approximately 40% of the screen height
    margin_v = int(screen_height * 0.4)

    # Format the title text with the specified font size
    # The ASS tag '\\fs' sets the font size dynamically
    text = f"{{\\fs{fontsize}}}{title}"

    # Write the dialogue event for the title
    # The title is displayed from the start (0 seconds) to the specified `title_duration`
    write_dialogue(file, 0, title_duration, text, margin_v=margin_v)


def write_loader_event(file, loader_duration, screen_width, screen_height, loader_color="&H00FF0000", border_color="&HFFFFFF00", start_time=0.0):
    """Write a loader animation event."""
    # Vertical margin for the loader, positioned near the bottom of the screen
    margin_v = int(screen_height * 0.8)
    
    # Total number of segments to divide the loader into
    bar_length = 30

    # Duration of each segment in the loader animation
    segment_duration = loader_duration / bar_length

    # Write the static border event for the entire loader duration
    # This ensures a consistent border is displayed while the loader animates
    write_dialogue(
        file,
        start_time,
        start_time + loader_duration,
        f"{{\\c{border_color}}}",
        margin_v=margin_v
    )

    # Write progressive loader events
    for i in range(1, bar_length + 1):
        # Create the loader text with the current progress filled (`█`) and remaining space empty
        loader_text = f"|{'█' * i}{' ' * (bar_length - i)}|"

        # Calculate the start and end times for the current segment
        segment_start = start_time + (i - 1) * segment_duration
        segment_end = start_time + i * segment_duration

        # Write the dialogue for the current loader segment
        # Each segment progressively fills the loader bar
        write_dialogue(
            file,
            segment_start,
            segment_end,
            f"{{\\c{loader_color}}}{loader_text}",
            margin_v=margin_v
        )


def write_lyrics_events(file, verses, primary_color="&H00FFFFFF", highlight_color="&H00FFFF00", spacing="\\N\\N\\N\\N"):
    """Write lyrics events with progressive highlighting."""
    for i, verse in enumerate(verses):
        # Construct the previous verse text with all words fully highlighted, if it exists
        previous_text = " ".join(
            [f"{{\\c{highlight_color}}}{w['word']}{{\\c{primary_color}}}" for w in verses[i - 1]["words"]]
        ) if i > 0 else ""

        # Construct the next verse text with no highlighting, if it exists
        next_text = " ".join([w["word"] for w in verses[i + 1]["words"]]) if i + 1 < len(verses) else ""

        for j, word in enumerate(verse["words"]):
            # Start and end times for the current word
            word_start = word["start"]
            word_end = word["end"]

            # Build the progressive text for the current verse with partial highlighting
            progressive_text = " ".join(
                f"{{\\c{highlight_color}}}{w['word']}{{\\c{primary_color}}}" if w["start"] < word_start else w["word"]
                for w in verse["words"]
            )

            # Combine previous, current, and next texts with specified spacing
            combined_text = f"{previous_text}{spacing}{progressive_text}{spacing}{next_text}"

            # Write the dialogue event for the current word
            write_dialogue(file, word_start, word_end, combined_text)


def extend_last_event(f, verses, audio_duration):
    """
    Extend the last line to the end of the audio.
    """
    if verses:
        # Retrieve the end time of the last verse
        last_verse_end = verses[-1]["end"]

        # Check if the end of the last verse is before the audio duration
        if last_verse_end < audio_duration:
            # Write a new dialogue event extending to the end of the audio
            f.write(f"Dialogue: 0,{format_time(last_verse_end)},{format_time(audio_duration)},Default,,0,0,0,,\n")


def create_ass_file(
    verses, 
    output_path, 
    audio_duration, 
    title="Karaoke", 
    font="Arial", 
    fontsize=48, 
    screen_width=1280, 
    screen_height=720
):
    """Generate an ASS subtitle file."""
    try:
        # Determine the start time of the first word in the verses
        first_word_start = verses[0]["words"][0]["start"]

        # Calculate the duration for the title display (25% of the pre-lyrics time)
        title_duration = first_word_start * 0.25

        # Calculate the duration for the loader animation (75% of the pre-lyrics time)
        loader_duration = first_word_start * 0.75

        # Open the output ASS file for writing
        with open(output_path, "w", encoding="utf-8") as file:
            # Write general script information such as title and script type
            write_script_info(file, title)

            # Write subtitle styles (e.g., font and alignment settings)
            write_styles(file, font, fontsize)

            # Write the header for the events section
            write_events_header(file)

            # Write the title event if a title 
            write_title_event(file, title, title_duration, screen_height)

            # Write the loader animation event after the title
            write_loader_event(file, loader_duration, screen_width, screen_height, start_time=title_duration)

            # Calculate the offset for the verses start times to follow the title and loader
            verses_start_time = title_duration + loader_duration

            # Adjust the start and end times of each verse
            for verse in verses:
                verse["start"] += verses_start_time
                verse["end"] += verses_start_time

            # Write the events for the lyrics with appropriate timing and formatting
            write_lyrics_events(file, verses)

            # Extend the last subtitle event to cover any remaining audio duration
            extend_last_event(file, verses, audio_duration)

    except Exception as e:
        # Handle and re-raise any errors that occur during file generation
        raise RuntimeError(f"Failed to create ASS file: {e}") from e