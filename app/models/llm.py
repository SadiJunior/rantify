from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Union


class Review(BaseModel):
    """Model of the Review data."""

    facts: Union[str, List[str]] = Field(
        description="The facts about the playlist being reviewed, as a string or a numbered list"
    )
    review: str = Field(description="The review of the playlist")
    rating: int = Field(description="The rating score from 0 to 10")


class Rhyme(BaseModel):
    """Model of the Rhyme data."""

    facts: Union[str, List[str]] = Field(
        description="The facts about the playlist being analyzed, as a string or a numbered list"
    )
    stanzas: List[List[str]] = Field(
        description="The list of stanzas for the playlist. The stanzas are composed by a list of lines."
    )


class RantType(Enum):
    """The type of Rant to generate."""

    RATE = 0
    ROAST = 1
    RHYME = 2
