import numpy as np
from src.opennotebookllm.inference.model_loaders import (
    load_parler_tts_model_and_tokenizer,
)


default_speaker_1_description = "Laura's voice is exciting and fast in delivery with very clear audio and no background noise."
default_speaker_2_description = (
    "Jon's voice is calm with very clear audio and no background noise."
)


def _speech_generation_parler(
    input_text: str, model_id: str, speaker_description: str
) -> np.array:
    model, tokenizer = load_parler_tts_model_and_tokenizer(model_id)

    prompt_input_ids = tokenizer(input_text, return_tensors="pt").input_ids
    input_ids = tokenizer(speaker_description, return_tensors="pt").input_ids

    generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
    waveform = generation.cpu().numpy().squeeze()

    return waveform


def text_to_speech(
    input_text: str,
    model_id: str,
    speaker_description: str = default_speaker_1_description,
) -> np.array:
    """
    Generates a speech waveform using the input_text, a speaker description and a given model id.

    Examples:
        >>> waveform = text_to_speech("Welcome to our amazing podcast", "parler-tts/parler-tts-mini-v1", "Laura's voice is exciting and fast in delivery with very clear audio and no background noise.")

    Args:
        input_text (str): The text to convert to speech.
        model_id (str): A model id from the registered models list.
        speaker_description (str): A description in natural language of how we want the voice to sound.

    Returns:
        numpy array: The waveform of the speech as a 2D numpy array
    """
    if "parler" in model_id:
        return _speech_generation_parler(input_text, model_id, speaker_description)
    else:
        raise NotImplementedError(f"Model {model_id} not yet implemented for TTS")
