from pathlib import Path

# Local Imports
from ..print_utilities import print_message


def _validate_frequency(value):
    """Validate frequency to ensure it is not zero.

    Args:
        value (int): The frequency value to validate.

    Returns:
        int or None: The frequency value if it is not zero, else None.
    """
    return None if value == 0 else value


def _create_directory(path):
    """
    Create a directory if it does not exist.

    Args:
        path (str): The path to the directory to create.
    """
    path = Path(path)

    # Create the directory if it does not exist
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)

        # Print a message if the directory is created
        print_message("[DIR]", text_color="bright_yellow")
        print_message(f"Created output directory:", text_color="bright_yellow", indent_level=1)
        print_message(f"`{path}`", text_color="bright_yellow", indent_level=2, include_border=True)

if __name__ == "__main__":
    print("This script contains utility functions for audio to MIDI conversion.")