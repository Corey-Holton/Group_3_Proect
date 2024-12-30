# Third-Party Imports
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from pprint import pprint

# Local Imports
from .constants import INSTRUMENT_TO_PROGRAM, VALID_NOTES, ACCEPTABLE_PARAMETERS
from ..print_utilities import print_message


# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-1.5-flash"

# Initialize the Gemini model
llm = ChatGoogleGenerativeAI(
    google_api_key=GEMINI_API_KEY,
    model=GEMINI_MODEL,
    temperature=0
)

# Define schemas for the output parser
schemas = [
    ResponseSchema(
        name=key,
        type=value['type'],
        description=f"{value['description']} Constraints: {value['constraints']}"
        if value.get("complex", False) else value["description"],
    )
    for key, value in ACCEPTABLE_PARAMETERS.items()
]

# Initialize the parser
parser = StructuredOutputParser.from_response_schemas(schemas)

# Prompt components
PREFIX = "You are a music AI assistant. Based on the user's description, generate parameters to modify a MIDI file."
INSTRUCTIONS = parser.get_format_instructions()
CONSTRAINTS = f""" 
1. Instruments must be represented by their **MIDI program numbers (0-127)**. 
   Each program number corresponds to a specific instrument name based on the following mapping:
   {INSTRUMENT_TO_PROGRAM}.

2. The output format for instruments should be a dictionary where:
   - The keys are integers representing the instrument channel indices (e.g., 0, 1, 2, etc.).
   - The values are integers representing the MIDI program numbers (0-127).
"""

# Prompt template
PROMPT_TEMPLATE = f"""
{PREFIX}

ENSURE OUTPUT FORMAT IS STRICTLY VALID JSON (DO NOT ADD COMMENTS):
1. Instruments must use their MIDI program numbers (0-127) in the format described above.
2. Other parameters should follow the instructions provided.
{INSTRUCTIONS}

IMPORTANT CONSTRAINTS:
{CONSTRAINTS}
"""


def _execute_query(text_query):
    """ 
    Execute a query using the Gemini model and parse the response.

    Args:
        text_query (str): The user query to execute.

    Returns:
        dict: The parsed response from the model.
    """
    try:
        gemini_response = llm.invoke(
            f"{PROMPT_TEMPLATE}\n\nUser request: {text_query}. Reminder: Only select instruments from the list of available instruments.")

        print_message("[AI OUTPUT]", text_color="bright_blue")
        print(gemini_response.content)
        print_message("", text_color="bright_blue", include_border=True)

        parsed_response = parser.parse(gemini_response.content)

        invalid_programs = [
            program for program in parsed_response.get("instruments", {}).values()
            if program not in INSTRUMENT_TO_PROGRAM.values()
        ]
        if invalid_programs:
            raise ValueError(f"AI generated invalid MIDI program numbers: {invalid_programs}")

        print_message("[PARSED RESPONSE]", text_color="bright_cyan")
        pprint(parsed_response)
        print_message("", text_color="bright_cyan", include_border=True)

        return parsed_response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    print("This script is used to execute a query using the Gemini model and parse the response.")
    print(PROMPT_TEMPLATE)
