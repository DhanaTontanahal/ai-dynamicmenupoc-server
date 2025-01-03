import requests
import json  # Ensure this is imported

# Hugging Face API endpoint and token
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"
HEADERS = {"Authorization": "Bearer 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"}

def get_ranked_menus_with_llama(input_data):
    """
    Sends input data to Hugging Face's LLaMA model and gets the ranked menus.
    :param input_data: List of menu items with click counts.
    :return: Ranked menus in the format expected by the UI.
    """
    if len(input_data) == 0:
        return {"ranked_menus": []}

    # Prepare the payload
    payload = {
        "inputs": f"Rank these menus in descending order of click count: {json.dumps(input_data)}"
    }

    # Send request to Hugging Face Inference API
    response = requests.post(API_URL, headers=HEADERS, json=payload)

    # Handle API errors
    if response.status_code != 200:
        raise Exception(f"Hugging Face API Error: {response.text}")

    # Parse the Hugging Face response
    ranked_data = response.json()  # This is a list, not a dictionary
    print("Raw Response from Hugging Face API:", ranked_data)

    # Access the first element of the list to get the `generated_text`
    if isinstance(ranked_data, list) and len(ranked_data) > 0:
        generated_text = ranked_data[0].get("generated_text", "")
        print("Generated Text:", generated_text)
    else:
        raise Exception("Unexpected response format from Hugging Face API")

    # Parse the generated text to extract menu names
    try:
        lines = generated_text.split("The right order is:")[-1].strip().split("\n")
        ranked_menus = [{"menu": line.split(" (")[1].rstrip(")")} for line in lines if " (" in line]
    except Exception as e:
        print("Error parsing ranked menus:", e)
        ranked_menus = []

    print("Processed Ranked Menus:", ranked_menus)
    return {"ranked_menus": ranked_menus}
