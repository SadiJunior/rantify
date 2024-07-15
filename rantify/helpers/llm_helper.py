import tiktoken

from tiktoken import Encoding

from pydantic import BaseModel, Field
from typing import List, Union

from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.schema.output_parser import OutputParserException
from langchain_openai import ChatOpenAI


from helpers import spotify_prompt_helper
from helpers.spotify_helper import SpotifyPlaylist


MAX_PROMPT_TOKENS = 12288
MAX_RETRY_ATTEMPTS = 3


# TODO: Put this somewhere else
with open('./prompts/rate.md', 'r') as file:
    rate_prompt_template = file.read()


# TODO: Put this somewhere else
with open('./prompts/roast.md', 'r') as file:
    roast_prompt_template = file.read()


# TODO: Put this somewhere else
with open('./prompts/rhyme.md', 'r') as file:
    rhyme_prompt_template = file.read()


# TODO: Put this somewhere else
with open('./prompts/limit_exceeded.md', 'r') as file:
    limit_exceeded_prompt_message = file.read()


class Review(BaseModel):
    """Model of the Review data."""
    facts: Union[str, List[str]] = Field(description="The facts about the playlist being reviewed, as a string or a numbered list")
    review: str = Field(description="The review of the playlist")
    rating: int = Field(description="The rating score from 0 to 10")


class Rhyme(BaseModel):
    """Model of the Rhyme data."""
    facts: Union[str, List[str]] = Field(description="The facts about the playlist being analyzed, as a string or a numbered list")
    stanzas: List[List[str]] = Field(description="The list of stanzas for the playlist. The stanzas are composed by a list of lines.")


class RantPromptManager:
    """Class to manage the Rant Prompt."""

    def __init__(
            self,
            parser_model: BaseModel,
            prompt_template: str,
            max_prompt_tokens: int = MAX_PROMPT_TOKENS,
            limit_exceeded_prompt_message: str = limit_exceeded_prompt_message):
        """Creates the Rant Prompt Manager object."""
        self.parser = PydanticOutputParser(pydantic_object=parser_model)
        self.prompt_template = PromptTemplate(
            template=prompt_template,
            input_variables=["playlist", "tracks"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()},
        )
        self.max_prompt_tokens = max_prompt_tokens
        self.limit_exceeded_prompt_message = limit_exceeded_prompt_message


    def generate_prompt(self, playlist: SpotifyPlaylist, encoding: Encoding):
        """Generates the prompt for the given playlist."""
        playlist_csv = spotify_prompt_helper.playlist_to_csv(playlist)
        tracks_csv = spotify_prompt_helper.tracks_to_csv(playlist.tracks)

        prompt = self.prompt_template.format(playlist=playlist_csv, tracks=tracks_csv)

        prompt_tokens = encoding.encode(prompt)

        if len(prompt_tokens) > self.max_prompt_tokens:
            prompt = self.adjust_prompt(prompt_tokens, encoding)
            prompt += self.limit_exceeded_prompt_message

        return prompt
    

    def adjust_prompt(self, tokens: List[int], encoding: Encoding):
        """Adjusts the prompt to fit the maximum context tokens."""
        if len(tokens) <= MAX_PROMPT_TOKENS:
            return tokens
        
        adjusted_prompt = tokens[:MAX_PROMPT_TOKENS]

        return encoding.decode(adjusted_prompt)


class LLMClient:
    """LLMClient object that interacts with the LLM API."""

    def __init__(self, model: str):
        """Creates the LLM Client object."""
        self.model = model
        self.llm = ChatOpenAI(model=model)
        self.encoding = tiktoken.encoding_for_model(model)

        self.rate_prompt_manager = RantPromptManager(parser_model=Review, prompt_template=rate_prompt_template)
        self.roast_prompt_manager = RantPromptManager(parser_model=Review, prompt_template=roast_prompt_template)
        self.rhyme_prompt_manager = RantPromptManager(parser_model=Rhyme, prompt_template=rhyme_prompt_template)


    def rate(self, playlist: SpotifyPlaylist):
        """Rates the given playlist."""
        return self.rant(playlist, self.rate_prompt_manager)


    def roast(self, playlist: SpotifyPlaylist):
        """Roasts the given playlist."""
        return self.rant(playlist, self.roast_prompt_manager)
    

    def rhyme(self, playlist: SpotifyPlaylist):
        """Creates a rhyme for the given playlist."""
        return self.rant(playlist, self.rhyme_prompt_manager)


    def rant(self, playlist: SpotifyPlaylist, prompt_manager: RantPromptManager):
        """Rants the given playlist."""
        prompt = prompt_manager.generate_prompt(playlist, self.encoding)

        return self.get_parsed_response(prompt, prompt_manager.parser)
    
    
    def get_parsed_response(self, prompt: str, parser: PydanticOutputParser):
        """Gets the parsed response."""
        parsed_response = None
        retry_attempts = 0

        while parsed_response is None:
            if retry_attempts >= MAX_RETRY_ATTEMPTS:
                raise OutputParserException("Failed to get a valid response from the LLM API.")

            try:
                response = self.llm.invoke(prompt)
                parsed_response = parser.parse(response.content)
            except OutputParserException:
                retry_attempts += 1

        return parsed_response
