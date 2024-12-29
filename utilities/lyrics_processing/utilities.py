# Third-Party Imports
from deep_translator import GoogleTranslator


def get_available_languages():
    """
    Retrieve available language codes and names for translation.
    
    :return: dictionary of language names and codes.
    """
    g_translator = GoogleTranslator()
    return g_translator.get_supported_languages(as_dict=True)
