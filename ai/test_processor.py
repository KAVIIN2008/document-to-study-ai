from document_processor import extract_text_from_pdf

pdf_path = "data/uploads/sample.pdf"

text = extract_text_from_pdf(pdf_path)

print(text)