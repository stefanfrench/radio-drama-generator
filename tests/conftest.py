from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def example_data():
    return Path(__file__).parent.parent / "example_data"


@pytest.fixture()
def tts_prompt():
    return "Wow you are really good at writing unit tests!"


@pytest.fixture()
def tts_speaker_description():
    return "Laura's voice is enthusiastic and fast with a very close recording that has no background noise."


@pytest.fixture()
def podcast_script():
    return "Speaker 1: Welcome to our podcast. Speaker 2: It's great to be here!"
