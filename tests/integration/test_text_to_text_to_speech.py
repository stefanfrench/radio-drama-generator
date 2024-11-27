from src.opennotebookllm.inference.model_loaders import load_llama_cpp_model
from src.opennotebookllm.inference.text_to_speech import text_to_speech
from src.opennotebookllm.inference.text_to_text import text_to_text


def test_text_to_text_to_speech():
    model = load_llama_cpp_model(
        "HuggingFaceTB/smollm-135M-instruct-v0.2-Q8_0-GGUF/smollm-135m-instruct-add-basics-q8_0.gguf"
    )
    result = text_to_text(
        "What is the capital of France?",
        model=model,
        system_prompt="",
        return_json=False,
        stop=".",
    )

    text_to_speech(
        input_text=result,
    )
