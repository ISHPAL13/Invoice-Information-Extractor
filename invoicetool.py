import os
import pytesseract
from pdf2image import convert_from_path
from mistralai import Mistral
import json
import pandas as pd


# Set Tesseract executable path 
pytesseract.pytesseract.tesseract_cmd = #add ur tesseract path here

# Poppler path for pdf2image
POPPLER_PATH = #add ur poppler path here

# Invoice PDF path
INVOICE_PATH = #add ur invoice path here

def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path, dpi=300, poppler_path=POPPLER_PATH)
    full_text = ""
    for image in images:
        text = pytesseract.image_to_string(image)
        full_text += text + "\n"
    return full_text

import re

def run_mistral_prompt(text):
    API_KEY = os.getenv("MISTRAL_API_KEY")
    print(f"Using API Key: {API_KEY[:5]}... (hidden)")

    if not API_KEY:
        raise Exception("MISTRAL_API_KEY environment variable is not set!")

    client = Mistral(api_key=API_KEY)

    prompt = f"""
You are an invoice parser. Extract the following fields from this unstructured invoice text:

- Consignor Name
- Consignor GST
- Consignor Address
- Consignee Name
- Consignee GST
- Consignee Address
- Invoice Number
- Invoice Date
- HSN Code
- GST Details
- Invoice Value

Return your answer as valid JSON ONLY. Do not add any extra explanation.

Invoice Text:
{text}
    """

    response = client.chat.complete(
        model="mistral-medium",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=1000,
    )

    content = response.choices[0].message.content.strip()

    # Remove markdown code block wrappers if present
    content = re.sub(r"^```(?:json)?\n", "", content)  # Remove starting ```json or ```
    content = re.sub(r"\n```$", "", content)          # Remove ending ```

    # Now parse JSON
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # If JSON parsing fails, return raw content for debugging
        return content
    
def save_to_excel(data, filename="invoice_data.xlsx"):
    # If data is a dict, convert it to a DataFrame with one row
    if isinstance(data, dict):
        df = pd.DataFrame([data])
    elif isinstance(data, list):
        df = pd.DataFrame(data)
    else:
        raise ValueError("Unsupported data format for Excel export")

    df.to_excel(filename, index=False)
    print(f"✅ Invoice data saved to {filename}")    


def main():
    print(" Extracting text from invoice PDF...")
    extracted_text = extract_text_from_pdf(INVOICE_PATH)

    print(" Sending extracted text to Mistral for parsing...")
    invoice_data = run_mistral_prompt(extracted_text)

    print("\n Extracted Invoice Data:\n")
    print(json.dumps(invoice_data, indent=4))

    # Save to Excel
    save_to_excel(invoice_data, "extracted_invoice.xlsx")


if __name__ == "__main__":
    main()


import os

print("Current working directory:", os.getcwd())


