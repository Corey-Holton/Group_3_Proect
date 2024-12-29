TOTAL_WIDTH = 80
DEFAULT_TEXT_COLOR = 97
DEFAULT_BORDER_COLOR = 97

COLOR_CODES = {
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "white": 37,
    "bright_black": 90,
    "bright_red": 91,
    "bright_green": 92,
    "bright_yellow": 93,
    "bright_blue": 94,
    "bright_magenta": 95,
    "bright_cyan": 96,
    "bright_white": 97
}

def print_with_color(message, color=DEFAULT_TEXT_COLOR):
    """Return a formatted string with the specified color."""
    if isinstance(color, str):
        color = COLOR_CODES.get(color.lower(), DEFAULT_TEXT_COLOR)

    bold = "\033[1m"
    color_code = f"\033[{color}m"
    reset = "\033[0m"
    return f"{bold}{color_code}{message}{reset}"

def wrap_text(text, width):
    """Wrap text to fit within the specified width with optional indentation."""
    import textwrap
    return textwrap.fill(text, width=width, subsequent_indent="\t")

def generate_border(char="═", border_color=DEFAULT_BORDER_COLOR):
    """Generate a horizontal border of TOTAL_WIDTH length."""
    return print_with_color(char * TOTAL_WIDTH, border_color)

def format_with_indent(message, indent_char="\t", level=1):
    """Format a multi-line message with specified indentation levels."""
    indent = indent_char * level
    lines = message.splitlines()
    return "\n".join(f"{indent}{line}" if line.strip() else "" for line in lines)

def print_title(title, text_color=DEFAULT_TEXT_COLOR, border_color=DEFAULT_BORDER_COLOR, closed_corners=True):
    """Print a formatted title within a bordered box."""
    padding = (TOTAL_WIDTH - len(title) - 2) // 2
    border_top = "╔" + "═" * (TOTAL_WIDTH - 2) + "╗"
    border_bottom = "╚" + "═" * (TOTAL_WIDTH - 2) + "╝" if closed_corners else "╠" + "═" * (TOTAL_WIDTH - 2) + "╣"
    padded_title = "║" + " " * padding + title + " " * (TOTAL_WIDTH - len(title) - padding - 2) + "║"

    print(print_with_color(border_top, border_color))
    print(print_with_color(padded_title[:1], border_color) + print_with_color(padded_title[1:-1], text_color) + print_with_color(padded_title[-1:], border_color))
    print(print_with_color(border_bottom, border_color))

def print_message(message, text_color=DEFAULT_TEXT_COLOR, indent_level=0, include_border=False, border_color=DEFAULT_BORDER_COLOR):
    """Print a message with optional borders and indentation."""
    inner_width = TOTAL_WIDTH - 4
    formatted_message = format_with_indent(message, indent_char="\t", level=indent_level)
    wrapped_message = wrap_text(formatted_message, inner_width)

    print(print_with_color(wrapped_message, text_color))
    if include_border:
        print(generate_border(border_color=border_color))

if __name__ == "__main__":
    print("This script should not be run directly! Import these functions for use in another file.")