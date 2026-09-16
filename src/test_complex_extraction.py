from extract_contact_info import extract_contact_info
import json

def test_complex_extraction():
    """ Test structured output with more complex input."""

    test_texts = [
        "For any questions, please contact Dr. Marie-Claire Dupont at m.dupont@hospital.fr or at +33-1-42-86-75-30",
        "Jean-Baptiste de la Fontaine (jb.fontaine@company.org) - Tel: 07.89.12.34.56",
        "Ms. Sophie MARTIN, HR Manager (sophie.martin@entreprise.com, 06 12 34 56 78)",
        "Contact: Pierre Durand - Email: pierre@startup.io - Mobile: 0612345678",
        "Call Mr. Alexandre Petit at 01 23 45 67 89 or write to a.petit@corp.fr",
        "Our project manager Marc Dubois (marc.dubois@company.com) can be reached at 06-12-34-56-78"
    ]

    print("=== Extraction Test with Structured Output ===\n")

    for idx, text in enumerate(test_texts):
        print(f"\n📋 Testing text {idx + 1}: {text}\n")
        try:
            structured_data = extract_contact_info(text)
            print(f"\n📋 Extracted data for text {idx + 1}:")
            print(json.dumps(structured_data, indent=2, ensure_ascii=False))

            # Validate the extracted data against the expected schema
            expected_schema = {
                "name": str,
                "email": str,
                "phone": str
            }
            if isinstance(structured_data, dict) and all(key in structured_data for key in expected_schema):
                print("✅ Structure validated")
            else:
                print("❌ Structure validation failed")
        except Exception as e:
            print(f"\n❌ Error: Response is not valid JSON: {e}")
            print(f"Raw response: {structured_data}")
        print("\n" + "=" * 40 + "\n")

if __name__ == "__main__":
    test_complex_extraction()