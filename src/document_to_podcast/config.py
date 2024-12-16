from pathlib import Path
from typing import Literal
from typing_extensions import Annotated

from pydantic import BaseModel, FilePath
from pydantic.functional_validators import AfterValidator

from document_to_podcast.preprocessing import DATA_LOADERS


DEFAULT_PROMPT = """
 You are a playwright generating engaging and immersive dialogue for a radio drama in JSON format.
 The drama is based on the  provided context
 The script features the following characters:
 {SPEAKERS}
 Instructions:
 - Write compelling, emotionally rich dialogue that reflects the personalities of the characters and advances the story.
 - Stay true to the original themes and tone of the provided context, emphasizing character development and moral lessons.
 - Add interjections to enhance the radio drama's atmosphere.
 - Format the output as a JSON conversation.
 - Avoid repeating ideas already discussed
 - Mix up the order of the speakers
 - End appropriately after around 20 dialogue exchanges
  Example:
 {
  "Speaker 1": "Bah, humbug! Why would I care for Christmas?",
  "Speaker 2": "If I may, sir, Christmas is about kindness, something we could all use more of.",
  "Speaker 3": "Uncle Scrooge, Christmas is a time for joy and goodwill!",
  "Speaker 1": "Enough about kindness!",
 }
"""


DEFAULT_SPEAKERS = [
    {
        "id": 1,
        "name": "Scrooge",
        "description": "Scrooge is the miserly and skeptical protagonist. He dismisses the joys of Christmas and struggles to see beyond his greed and bitterness.",
        "voice_profile": "male_1",
    },
    {
        "id": 2,
        "name": "Bob Cratchit",
        "description": "Bob is a kind-hearted but underpaid employee. He represents humility and warmth despite his hardships.",
        "voice_profile": "male_4",
    },
    {
        "id": 3,
        "name": "Fred",
        "description": "Fred is cheerful and good-natured nephew, who believes in the spirit of Christmas.",
        "voice_profile": "female_1",
    },
]

SUPPORTED_TTS_MODELS = Literal[
    "OuteAI/OuteTTS-0.1-350M-GGUF/OuteTTS-0.1-350M-FP16.gguf",
    "OuteAI/OuteTTS-0.2-500M-GGUF/OuteTTS-0.2-500M-FP16.gguf",
    "parler-tts/parler-tts-large-v1",
    "parler-tts/parler-tts-mini-v1",
    "parler-tts/parler-tts-mini-v1.1",
]


def validate_input_file(value):
    if Path(value).suffix not in DATA_LOADERS:
        raise ValueError(
            f"input_file extension must be one of {list(DATA_LOADERS.keys())}"
        )
    return value


def validate_text_to_text_model(value):
    parts = value.split("/")
    if len(parts) != 3:
        raise ValueError("text_to_text_model must be formatted as `owner/repo/file`")
    if not value.endswith(".gguf"):
        raise ValueError("text_to_text_model must be a gguf file")
    return value


def validate_text_to_text_prompt(value):
    if "{SPEAKERS}" not in value:
        raise ValueError("text_to_text_prompt must contain `{SPEAKERS}` placeholder")
    return value


class Speaker(BaseModel):
    id: int
    name: str
    description: str
    voice_profile: str

    def __str__(self):
        return f"Speaker {self.id}. Named {self.name}. {self.description}"


class Config(BaseModel):
    input_file: Annotated[FilePath, AfterValidator(validate_input_file)]
    output_folder: str
    text_to_text_model: Annotated[str, AfterValidator(validate_text_to_text_model)]
    text_to_text_prompt: Annotated[str, AfterValidator(validate_text_to_text_prompt)]
    text_to_speech_model: SUPPORTED_TTS_MODELS
    speakers: list[Speaker]
