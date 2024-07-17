import tiktoken
from tiktoken import Encoding

from typing import List, Union
from pydantic import BaseModel
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.schema.output_parser import OutputParserException
from langchain_openai import ChatOpenAI

from helpers.spotify import spotify_prompt_helper

from models.llm_models import Review, Rhyme
from models.spotify_models import SpotifyPlaylist

from prompts import prompts


MAX_PROMPT_TOKENS = 12288
MAX_RETRY_ATTEMPTS = 3


class RantPromptManager:
    """Class to manage the Rant Prompt."""

    def __init__(
            self,
            parser_model: BaseModel,
            prompt_template: str,
            max_prompt_tokens: int = MAX_PROMPT_TOKENS,
            limit_exceeded_prompt_message: str = prompts.limit_exceeded_prompt_message
    ):
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
        if len(tokens) <= self.max_prompt_tokens:
            return tokens
        
        adjusted_prompt = tokens[:self.max_prompt_tokens]

        return encoding.decode(adjusted_prompt)


class LLMClient:
    """LLMClient object that interacts with the LLM API."""

    def __init__(self, model: str):
        """Creates the LLM Client object."""
        self.model = model
        self.llm = ChatOpenAI(model=model)
        self.encoding = tiktoken.encoding_for_model(model)

        self.rate_prompt_manager = RantPromptManager(parser_model=Review, prompt_template=prompts.rate_prompt_template)
        self.roast_prompt_manager = RantPromptManager(parser_model=Review, prompt_template=prompts.roast_prompt_template)
        self.rhyme_prompt_manager = RantPromptManager(parser_model=Rhyme, prompt_template=prompts.rhyme_prompt_template)


    def rate(self, playlist: SpotifyPlaylist) -> Review:
        """Rates the given playlist."""
        return self.rant(playlist, self.rate_prompt_manager)


    def roast(self, playlist: SpotifyPlaylist) -> Review:
        """Roasts the given playlist."""
        return self.rant(playlist, self.roast_prompt_manager)
    

    def rhyme(self, playlist: SpotifyPlaylist) -> Rhyme:
        """Creates a rhyme for the given playlist."""
        return self.rant(playlist, self.rhyme_prompt_manager)


    def rant(self, playlist: SpotifyPlaylist, prompt_manager: RantPromptManager) -> Union[Review | Rhyme]:
        """Rants the given playlist."""
        prompt = prompt_manager.generate_prompt(playlist, self.encoding)

        return self.get_parsed_response(prompt, prompt_manager.parser)
    
    
    def get_parsed_response(self, prompt: str, parser: PydanticOutputParser) -> Union[Review | Rhyme]:
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
