import json

from document_processor import extract_text_from_pdf
from content_analyzer import analyze_content


pdf_path = "data/uploads/sample.pdf"

text = extract_text_from_pdf(pdf_path)

analysis = analyze_content(text)

print("\n===== STRUCTURED AI CONTENT =====\n")
print(json.dumps(analysis, indent=4, ensure_ascii=False))