# src/test_structured_output.py
import requests
import json

def test_structured_output():
    """Test the structured output functionality with JSON schema."""
    
    url = "http://localhost:8000/generate"
    
    # Define a JSON schema for contact information extraction
    contact_schema = {
        "type": "json_schema",
        "json_schema": {
            "name": "contact_extraction",
            "schema": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The person's full name"
                    },
                    "email": {
                        "type": "string",
                        "description": "The person's email address"
                    },
                    "phone": {
                        "type": "string",
                        "description": "The person's phone number"
                    }
                },
                "required": ["name", "email", "phone"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
    
    # Test data
    test_text = "Contact our project manager Marc Dubois at 06-12-34-56-78 or marc.dubois@company.com"
    
    # Create the request payload with structured output
    payload = {
        "prompt": f"Extract the contact information from the following text: {test_text}",
        "system_prompt": "You are an assistant specialized in data extraction. Extract only the requested information in the specified JSON format.",
        "model": "groq-kimi-primary",
        "temperature": 0.1,
        "max_tokens": 150,
        "response_format": contact_schema
    }
    
    print("=== Test Structured Output ===")
    print(f"Input text: {test_text}")
    print(f"Schema used: {json.dumps(contact_schema, indent=2)}")
    print("\nSending request...")
    
    # Make the API call
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ Success! Response received:")
        print(f"Model used: {result['model']}")
        print(f"Tokens: {result['prompt_tokens']} prompt + {result['completion_tokens']} completion = {result['total_tokens']} total")
        print(f"Cost: {result['cost']}")
        
        # Parse and display the structured response
        try:
            structured_data = json.loads(result['response'])
            print(f"\n📋 Extracted data (structured format):")
            print(json.dumps(structured_data, indent=2, ensure_ascii=False))
            
            # Validate the structure
            required_fields = ["name", "email", "phone"]
            missing_fields = [field for field in required_fields if field not in structured_data]
            
            if not missing_fields:
                print(f"\n✅ Validation: All required fields are present")
            else:
                print(f"\n❌ Validation: Missing fields: {missing_fields}")
                
        except json.JSONDecodeError as e:
            print(f"\n❌ Error: Response is not valid JSON: {e}")
            print(f"Raw response: {result['response']}")
    else:
        print(f"\n❌ HTTP error {response.status_code}:")
        print(response.text)

def test_without_structured_output():
    """Test the same extraction without structured output for comparison."""
    
    url = "http://localhost:8000/generate"
    test_text = "Contact our project manager Marc Dubois at 06-12-34-56-78 or marc.dubois@company.com"
    
    payload = {
        "prompt": f"Extract the contact information from the following text as JSON: {test_text}",
        "system_prompt": "You are an assistant specialized in data extraction. Respond only in JSON with the fields name, email, phone.",
        "model": "groq-kimi-primary",
        "temperature": 0.1,
        "max_tokens": 150
    }
    
    print("\n\n=== Test Without Structured Output (for comparison) ===")
    print(f"Input text: {test_text}")
    print("\nSending request...")
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ Success! Response received:")
        print(f"Raw response: {result['response']}")
        
        try:
            structured_data = json.loads(result['response'])
            print(f"\n📋 Extracted data:")
            print(json.dumps(structured_data, indent=2, ensure_ascii=False))
        except json.JSONDecodeError as e:
            print(f"\n❌ Error: Response is not valid JSON: {e}")
    else:
        print(f"\n❌ HTTP error {response.status_code}:")
        print(response.text)

if __name__ == "__main__":
    # Test with structured output
    test_structured_output()
    
    # Test without structured output for comparison
    test_without_structured_output()
