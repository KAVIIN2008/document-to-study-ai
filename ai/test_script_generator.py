import json

from document_processor import extract_text_from_pdf
from content_analyzer import analyze_content
from script_generator import generate_script


pdf_path = "data/uploads/sample.pdf"


text = extract_text_from_pdf(pdf_path)

analysis = analyze_content(text)

script = generate_script(analysis)


print("\n===== GENERATED EDUCATIONAL SCRIPT =====\n")

print(
    json.dumps(
        script,
        indent=4,
        ensure_ascii=False
    )
)