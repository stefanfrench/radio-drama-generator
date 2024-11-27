import numpy as np
from transformers import PreTrainedModel, PreTrainedTokenizerBase


def _speech_generation_parler(
    input_text: str,
    model: PreTrainedModel,
    tokenizer: PreTrainedTokenizerBase,
    speaker_description: str,
) -> np.ndarray:
    input_ids = tokenizer(speaker_description, return_tensors="pt").input_ids
    prompt_input_ids = tokenizer(input_text, return_tensors="pt").input_ids

    generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
    waveform = generation.cpu().numpy().squeeze()

    return waveform


def text_to_speech(
    input_text: str,
    model: PreTrainedModel,
    tokenizer: PreTrainedTokenizerBase,
    speaker_profile: str,
) -> np.ndarray:
    """
    UPDATE! Generates a speech waveform using the input_text and a speaker configuration that defines which model to use and its parameters.

    Examples:
        >>> waveform = text_to_speech("Welcome to our amazing podcast", "parler-tts/parler-tts-mini-v1", "Laura's voice is exciting and fast in delivery with very clear audio and no background noise.")

    Args:
        input_text (str): The text to convert to speech.
        model (PreTrainedModel): The model used for generating the waveform.
        tokenizer (PreTrainedTokenizerBase): The tokenizer used for tokenizing the text in order to send to the model.
        speaker_profile (str): A description used by the ParlerTTS model to configure the speaker profile.
    Returns:
        numpy array: The waveform of the speech as a 2D numpy array
    """
    model_id = model.config.name_or_path
    if "parler" in model_id:
        return _speech_generation_parler(input_text, model, tokenizer, speaker_profile)
    else:
        raise NotImplementedError(f"Model {model_id} not yet implemented for TTS")
