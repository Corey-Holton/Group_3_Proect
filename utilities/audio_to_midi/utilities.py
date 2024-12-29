from pathlib import Path

# Local Imports
from ..print_utilities import print_message


def _validate_frequency(value):
    """Validate frequency to ensure it is not zero."""
    return None if value == 0 else value


def _create_directory(path):
    """
    Create a directory if it does not exist.
    """
    path = Path(path)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        print_message("[DIR]", text_color="bright_yellow")
        print_message(f"Created output directory:", text_color="bright_yellow", indent_level=1)
        print_message(f"`{path}`", text_color="bright_yellow", indent_level=2, include_border=True)
