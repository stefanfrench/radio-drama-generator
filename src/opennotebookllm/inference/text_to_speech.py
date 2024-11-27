import numpy as np
from opennotebookllm.inference.model_loaders import (
    load_parler_tts_model_and_tokenizer,
)
from opennotebookllm.podcast_maker.config import SpeakerConfig


def _speech_generation_parler(input_text: str, tts_config: SpeakerConfig) -> np.ndarray:
    model, tokenizer = load_parler_tts_model_and_tokenizer(tts_config.model_id)

    prompt_input_ids = tokenizer(input_text, return_tensors="pt").input_ids
    input_ids = tokenizer(tts_config.speaker_description, return_tensors="pt").input_ids

    generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
    waveform = generation.cpu().numpy().squeeze()

    return waveform


def text_to_speech(input_text: str, tts_config: SpeakerConfig) -> np.ndarray:
    """
    Generates a speech waveform using the input_text and a speaker configuration that defines which model to use and its parameters.

    Examples:
        >>> waveform = text_to_speech("Welcome to our amazing podcast", "parler-tts/parler-tts-mini-v1", "Laura's voice is exciting and fast in delivery with very clear audio and no background noise.")

    Args:
        input_text (str): The text to convert to speech.
        tts_config: Configuration parameters for TTS model.

    Returns:
        numpy array: The waveform of the speech as a 2D numpy array
    """
    if "parler" in tts_config.model_id:
        return _speech_generation_parler(input_text, tts_config)
    else:
        raise NotImplementedError(
            f"Model {tts_config.model_id} not yet implemented for TTS"
        )
