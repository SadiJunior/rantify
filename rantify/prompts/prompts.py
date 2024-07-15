from pathlib import Path


# Directory where the prompt templates are stored
PROMPTS_DIR = Path('./prompts/templates')


def load_prompt_template(filename: str) -> str:
    """Loads a prompt template from a file."""
    file_path = PROMPTS_DIR / filename

    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{filename}' not found in '{PROMPTS_DIR}'")


class PromptTemplates:
    """Class that contains all the prompt templates."""
    rate_prompt_template = load_prompt_template('rate.md')
    roast_prompt_template = load_prompt_template('roast.md')
    rhyme_prompt_template = load_prompt_template('rhyme.md')
    limit_exceeded_prompt_message = load_prompt_template('limit_exceeded.md')
