import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

# Get OpenAI API key
openai_api_key = os.getenv("CHROMA_OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("CHROMA_OPENAI_API_KEY is not set in .env file")

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

def identify_themes(answers_dict):
    """
    Uses GPT to identify common themes across multiple document-specific answers.

    Args:
        answers_dict (dict): Dictionary where keys are document names and
                             values are answers related to the same user question.

    Returns:
        str: Synthesized summary of common themes with document-level citations.
    """
    combined_text = ""
    for doc, answer in answers_dict.items():
        combined_text += f"[{doc}]: {answer}\n\n"

    prompt = f"""
You are an AI research assistant. Below are responses from different documents answering the same question.

Task:
1. Identify 2–3 major recurring themes across the answers.
2. For each theme, provide a short, clear explanation.
3. Cite which documents support each theme using the format [document_name].

Responses:
{combined_text}

Generate the final theme summary below:
"""

    # Send prompt to GPT-4
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content
