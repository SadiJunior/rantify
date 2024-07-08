import tiktoken

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


class Review(BaseModel):
    """Model of the Review data."""
    facts: Union[str, List[str]] = Field(description="The facts about the playlist being reviewed, as a string or a numbered list")
    review: str = Field(description="The review of the playlist")
    rating: int = Field(description="The rating score from 0 to 10")


class ReviewPromptManager:
    """Class to manage the Review Prompt."""

    def __init__(self, prompt_template: str):
        self.parser = PydanticOutputParser(pydantic_object=Review)
        self.prompt_template = PromptTemplate(
            template=prompt_template,
            input_variables=["playlist", "tracks"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()},
        )


class LLMClient:
    """LLMClient object that interacts with the LLM API."""

    def __init__(self, model: str):
        """Creates the LLM Client object."""
        self.model = model
        self.llm = ChatOpenAI(model=model)
        self.encoding = tiktoken.encoding_for_model(model)

        self.rate_prompt_manager = ReviewPromptManager(rate_prompt_template)


    def rate(self, playlist: SpotifyPlaylist):
        """Rates the given playlist."""
        playlist_csv = spotify_prompt_helper.playlist_to_csv(playlist)
        tracks_csv = spotify_prompt_helper.tracks_to_csv(playlist.tracks)

        prompt = self.rate_prompt_manager.prompt_template.format(playlist=playlist_csv, tracks=tracks_csv)

        return self.review(prompt, self.rate_prompt_manager.parser)

    
    def review(self, prompt: str, parser: PydanticOutputParser):
        """Review the given prompt."""
        prompt_tokens = self.get_tokens(prompt)

        if len(prompt_tokens) > MAX_PROMPT_TOKENS:
            prompt = self.adjust_prompt(prompt_tokens)
            prompt += "... The data exceeded the maximum context tokens. Make your review based on the data until here. You might also make a joke regarding the number of tracks and the fact you couldn't review all of them."

        return self.get_parsed_response(prompt, parser)


    def get_tokens(self, string: str):
        """Gets the tokens of the given string."""
        tokens = self.encoding.encode(string)
        return tokens
    

    def adjust_prompt(self, tokens: List[int]):
        """Adjusts the prompt to fit the maximum context tokens."""
        if len(tokens) <= MAX_PROMPT_TOKENS:
            return tokens
        
        adjusted_prompt = tokens[:MAX_PROMPT_TOKENS]

        return self.encoding.decode(adjusted_prompt)
    
    
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
