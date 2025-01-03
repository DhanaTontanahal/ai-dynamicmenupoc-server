import requests
import json

# Hugging Face API endpoint and token
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"
HEADERS = {"Authorization": "Bearer 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"}

def get_ranked_menus_with_llama(input_data):
    print("inside get_ranked_menus_with_llama")
    print(len(input_data))

    if len(input_data) == 0:
        return []
    print("moving on...............................s")
    """
    Sends input data to Hugging Face's LLaMA model and gets the ranked menus.
    :param input_data: List of menu items with click counts.
    :return: Ranked menus as JSON.
    """
    # Prepare the payload
    payload = {
        "inputs": f"Rank these menus in descending order of click count: {json.dumps(input_data)}"
    }

    # Send request to Hugging Face Inference API
    response = requests.post(API_URL, headers=HEADERS, json=payload)

    # Handle API errors
    if response.status_code != 200:
        raise Exception(f"Hugging Face API Error: {response.text}")

    # Parse and return the ranked menu JSON
    ranked_data = response.json()
    print("rankede data")
    print(ranked_data)
    return ranked_data
