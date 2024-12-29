# Third-Party Imports
from deep_translator import GoogleTranslator


def get_available_languages():
    """
    Retrieve available language codes and names for translation.
    
    Returns:
        dict: Dictionary of language names and codes.
    """ 
    # Get languages as a dictionary from GoogleTranslator
    g_translator = GoogleTranslator()
    
    return g_translator.get_supported_languages(as_dict=True)

if __name__ == "__main__":
    print("This script contains utility functions for lyrics processing and translation.")