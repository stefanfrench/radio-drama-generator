from typing import Dict, Optional
from transformers import PreTrainedModel, PreTrainedTokenizerBase
from pydantic import BaseModel, ConfigDict


class SpeakerConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    model: PreTrainedModel
    speaker_id: str
    # ParlerTTS specific configuration
    tokenizer: Optional[PreTrainedTokenizerBase] = None
    speaker_description: Optional[str] = (
        None  # This description is used by the ParlerTTS model to configure the speaker profile
    )


class PodcastConfig(BaseModel):
    speakers: Dict[str, SpeakerConfig]
    sampling_rate: int = 44_100
