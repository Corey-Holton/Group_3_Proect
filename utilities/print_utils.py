TOTAL_WIDTH = 125
DEFAULT_TEXT_COLOR = 97
DEFAULT_BORDER_COLOR = 90

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
    """Print a message with the specified color."""
    if isinstance(color, str):
        color = COLOR_CODES.get(color.lower(), DEFAULT_TEXT_COLOR)
    
    bold = "\033[1m"
    color_code = f"\033[{color}m"
    reset = "\033[0m"
    return f"{bold}{color_code}{message}{reset}"

def print_title(title, text_color=DEFAULT_TEXT_COLOR, border_color=DEFAULT_BORDER_COLOR, closed_corners=True):
    """Print a title with specified colors and width."""
    padding = (TOTAL_WIDTH - len(title) - 2) // 2
    border_top = "╔" + "═" * (TOTAL_WIDTH - 2) + "╗"
    border_bottom = "╚" + "═" * (TOTAL_WIDTH - 2) + "╝" if closed_corners else "╠" + "═" * (TOTAL_WIDTH - 2) + "╣"
    padded_title = "║" + " " * padding + title + " " * (TOTAL_WIDTH - len(title) - padding - 2) + "║"

    left_border = padded_title[:1]
    right_border = padded_title[-1:]
    title_content = padded_title[1:-1]

    print(print_with_color(border_top, border_color))
    print(print_with_color(left_border, border_color) + print_with_color(title_content, text_color) + print_with_color(right_border, border_color))
    print(print_with_color(border_bottom, border_color))

def print_label(label, result, text_color=DEFAULT_TEXT_COLOR, border_color=DEFAULT_BORDER_COLOR, closed_corners=False):
    """Print a label with specified result and border color codes."""
    label_width = TOTAL_WIDTH // 2 - 2
    result_width = TOTAL_WIDTH - label_width - 7

    if len(label) > label_width:
        label = label[:label_width - 3] + "..."

    formatted_label = f"{label:<{label_width}}"
    formatted_result = f"{result:^{result_width},.5f}" if isinstance(result, (int, float)) else f"{result:^{result_width}}"
    padded_message = f"║ {formatted_label} | {formatted_result} ║"

    result_colored = print_with_color(padded_message[2:-2], text_color)
    result_with_border = print_with_color(padded_message[:2], border_color) + result_colored + print_with_color(padded_message[-2:], border_color)

    print(print_with_color(result_with_border))

    if closed_corners:
        border_bottom = "╚" + "═" * (TOTAL_WIDTH - 2) + "╝"
        print(print_with_color(border_bottom, border_color))

def print_footer(footer_text, text_color=DEFAULT_TEXT_COLOR, border_color=DEFAULT_BORDER_COLOR, closed_corners=True):
    """Print a footer with specified colors and alignment."""
    padded_footer = f"║ {footer_text:>{TOTAL_WIDTH - 4}} ║"

    footer_text_colored = print_with_color(f"\033[3m{padded_footer[2:-2]}\033[0m", text_color)
    footer_with_border = print_with_color(padded_footer[:2], border_color) + footer_text_colored + print_with_color(padded_footer[-2:], border_color)

    print(footer_with_border)
    if closed_corners:
        border_bottom = "╚" + "═" * (TOTAL_WIDTH - 2) + "╝"
        print(print_with_color(border_bottom, border_color))

def print_line(message, text_color=DEFAULT_TEXT_COLOR, border_color=DEFAULT_BORDER_COLOR):
    """Print a CMD message with separators."""
    border = "═" * TOTAL_WIDTH
    print(print_with_color(message, text_color))
    print(print_with_color(border, border_color))

if __name__ == "__main__":
    print("This script should not be run directly! Import these functions for use in another file.")