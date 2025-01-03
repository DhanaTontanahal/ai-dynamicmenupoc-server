# llama_model.py
from transformers import AutoModelForCausalLM, AutoTokenizer
import json

# Load the LLaMA model and tokenizer (one-time initialization)
model_name = "meta-llama/Llama-2-7b-chat-hf"  # Replace with a smaller version if necessary
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def get_ranked_menus_with_llama(input_data):
    """
    Function to process menu ranking using the LLaMA model.
    Args:
        input_data (list): List of menu click data.
    Returns:
        dict: JSON-like dictionary with ranked menus.
    """
    # Prepare the prompt for the model
    prompt = f"""
    Here is the click data for menus: {json.dumps(input_data)}.
    Rank these menus in descending order of click count and return the ranked result in JSON format.
    """

    # Tokenize the input
    inputs = tokenizer(prompt, return_tensors="pt")

    # Generate a response
    outputs = model.generate(inputs["input_ids"], max_length=512, temperature=0.7)

    # Decode and return the JSON response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return json.loads(response)  # Parse the JSON response from the model
