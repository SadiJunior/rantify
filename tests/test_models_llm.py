from app.models.llm import RantType, Review, Rhyme


def test_rant_type():
    """Test the RantType Enum."""
    assert RantType.RATE.value == 0
    assert RantType.ROAST.value == 1
    assert RantType.RHYME.value == 2


def test_review_model():
    """Test the Review model."""
    review = Review(
        facts="- The playlist is awesome! \n - The playlist is cool!",
        review="The playlist is incredible!",
        rating=8)

    assert review.facts == "- The playlist is awesome! \n - The playlist is cool!"
    assert review.review == "The playlist is incredible!"
    assert review.rating == 8

    review = Review(
        facts=["1. The playlist is awesome!", "2. The playlist is cool!"],
        review="The playlist is incredible!",
        rating=10)

    assert review.facts == ["1. The playlist is awesome!", "2. The playlist is cool!"]
    assert review.review == "The playlist is incredible!"
    assert review.rating == 10


def test_rhyme_model():
    """Test the Rhyme model."""
    rhyme = Rhyme(
        facts="- The playlist is awesome! \n - The playlist is cool!",
        stanzas=[["The playlist is incredible!", "The playlist is beautiful!"]])

    assert rhyme.facts == "- The playlist is awesome! \n - The playlist is cool!"
    assert rhyme.stanzas == [["The playlist is incredible!", "The playlist is beautiful!"]]

    rhyme = Rhyme(
        facts=["1. The playlist is awesome!", "2. The playlist is cool!"],
        stanzas=[["The playlist is incredible!", "The playlist is beautiful!"]])

    assert rhyme.facts == ["1. The playlist is awesome!", "2. The playlist is cool!"]
    assert rhyme.stanzas == [["The playlist is incredible!", "The playlist is beautiful!"]]
