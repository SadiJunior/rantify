import tiktoken

from pydantic import BaseModel, Field
from typing import List

from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.schema.output_parser import OutputParserException
from langchain_openai import ChatOpenAI


from helpers import spotify_prompt_helper
from helpers.spotify_helper import SpotifyPlaylist


# TODO: Put this somewhere else
with open('./prompts/rate.md', 'r') as file:
    rate_prompt_template = file.read()


class Review(BaseModel):
    """Model of the Review data."""
    facts: str = Field(description="The facts about the rating")
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

    def __init__(self, model, max_context_tokens=12288):
        """Creates the LLM Client object."""
        self.model = model
        self.llm = ChatOpenAI(model=model)
        self.encoding = tiktoken.encoding_for_model(self.model)
        self.max_context_tokens = max_context_tokens

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

        if (len(prompt_tokens) > self.max_context_tokens):
            prompt = self.adjust_prompt(prompt_tokens)
            prompt += "... The data exceeded the maximum context tokens. Make a joke regarding the number of tracks and the fact you couldn't review all of them."

        chain = self.llm.with_retry(retry_if_exception_type=(OutputParserException, )) | parser 

        return chain.invoke(prompt)


    def get_tokens(self, string: str):
        """Gets the tokens of the given string."""
        tokens = self.encoding.encode(string)
        return tokens
    

    def adjust_prompt(self, tokens: List[int]):
        """Adjusts the prompt to fit the maximum context tokens."""
        if len(tokens) <= self.max_context_tokens:
            return tokens
        
        adjusted_prompt = tokens[:self.max_context_tokens]

        return self.encoding.decode(adjusted_prompt)
