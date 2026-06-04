from doctest import Example
import requests
import json

def extract_contact_info(text):
    """Extract contact information using the local LLM API."""

    url = "http://localhost:8000/generate"

    # Define the system prompt for role specification
    system_prompt = "You are an assistant specialized in precise data extraction. Extract only the requested information in the specified JSON format. Do not make any comments."

    # Create few-shot examples in the prompt
    prompt = f"""Extract the name, email, and phone number from the following text and retrun them in JSON format.

    Example:
    Text: "Please contact Jean Martin at jean.martin@example.com or at 01-23-45-67-89"
    JSON: {{"name": "Jean Martin", "email": "jean.martin@example.com", "phone": "01-23-45-67-89"}}

    Text: "For more information: Sophie Durand (sophie@company.fr, 07-11-22-33-44)"
    JSON: {{"name": "Sophie Durand", "email": "sophie@company.fr", "phone": "07-11-22-33-44"}}

    Text: "COur representative Pierre Blanc (p.blanc@corp.com) can be reached at 06-99-88-77-66"
    JSON: {{"name": "Pierre Blanc", "email": "p.blanc@corp.com", "phone": "06-99-88-77-66"}}

    Now:
    Text: {text}
    JSON:
    """

    # Set parameters - low temperature for deterministic extraction
    payload = {
        "prompt": prompt, 
        "system_prompt" : system_prompt, # Role specification
        "model" : "groq-kimi-primary", 
        "temperature" : 0.1, # Low temperature for consistent data extraction
        "max_tokens" : 150, # Limit the response to 100 tokens
    }

    # Make the API request
    response = requests.post(url, json=payload)
    response_data = response.json()

    # Parse the JSON response
    try: 
        extracted_info = json.loads(response_data["response"])
        return extracted_info
    except json.JSONDecodeError:
        # Return a structured error message if parsing fails
        return {
            "error": "Failed to parse JSON response",
            "raw_response": response_data["response"]
        }

if __name__ == "__main__":
    # Test the function with a sample text
    test_text = "Contact our project manager Marc Dubois at 06-12-34-56-78 or marc.dubois@company.com"
    result = extract_contact_info(test_text)

    # Print the result
    print("Input text:", test_text)
    print("\nExtraction result:")
    print(json.dumps(result, indent=2))

    # Expected output:
    # {"name": "Marc Dubois", "email": "marc.dubois@entreprise.com", "phone": "06-12-34-56-78"}