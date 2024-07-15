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
    _rate_prompt_template = load_prompt_template('rate.md')
    _roast_prompt_template = load_prompt_template('roast.md')
    _rhyme_prompt_template = load_prompt_template('rhyme.md')
    _limit_exceeded_prompt_message = load_prompt_template('limit_exceeded.md')

    @property
    def rate_prompt_template(self) -> str:
        return self._rate_prompt_template

    @property
    def roast_prompt_template(self) -> str:
        return self._roast_prompt_template

    @property
    def rhyme_prompt_template(self) -> str:
        return self._rhyme_prompt_template

    @property
    def limit_exceeded_prompt_message(self) -> str:
        return self._limit_exceeded_prompt_message
