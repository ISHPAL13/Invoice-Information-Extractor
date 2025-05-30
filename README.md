# Invoice-Information-Extractor
This tool automatically extracts key invoice fields from PDF files, including GST details, consignor/consignee info, and invoice value. It uses OCR (Tesseract) to read scanned invoices, sends the extracted text to Mistral AI for parsing, and exports the structured data to an Excel file — streamlining invoice processing for businesses.

Installation Steps
1. Clone or Download the Repository
git clone https://github.com/yourusername/invoice-extractor.git
cd invoice-extractor
Or just download the invoicetool.py file if not using Git.

2. Install Required Python Libraries
pip install pytesseract pdf2image mistralai pandas openpyxl

4. Download & Install Tesseract OCR
Download: https://github.com/tesseract-ocr/tesseract

On Windows, download the installer directly:
https://github.com/UB-Mannheim/tesseract/wiki

After installing, note the path (e.g. C:\Program Files\Tesseract-OCR\tesseract.exe) and update this line in the script:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

4. Download Poppler for PDF Rendering
📥 Windows: https://github.com/oschwartz10612/poppler-windows/releases

Extract the ZIP and copy the path to the bin folder (e.g. C:\poppler-24.08.0\Library\bin)

Update this line in the script:
POPPLER_PATH = r'C:\poppler-24.08.0\Library\bin'

5. Set Mistral API Key
Get your API key from https://console.mistral.ai.
set MISTRAL_API_KEY=your_actual_key
PowerShell
powershell
$env:MISTRAL_API_KEY="your_actual_key"
macOS/Linux
export MISTRAL_API_KEY=your_actual_key

7. Update Invoice PDF Path
Modify this line in the script to point to your local invoice:

INVOICE_PATH = r'C:\Users\YourName\Documents\invoice.pdf'
Run the Script
python invoicetool.py
