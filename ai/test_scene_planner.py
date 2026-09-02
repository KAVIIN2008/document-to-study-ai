import json

from document_processor import extract_text_from_pdf
from content_analyzer import analyze_content
from script_generator import generate_script
from scene_planner import plan_scenes


pdf_path = "data/uploads/sample.pdf"


# Step 1: Extract the document text
text = extract_text_from_pdf(pdf_path)


# Step 2: Understand the complete document
analysis = analyze_content(text)


# Step 3: Generate the complete educational script
script = generate_script(analysis)


# Step 4: Convert the complete script into production scenes
scene_plan = plan_scenes(script)


print("\n===== GENERATED SCENE PLAN =====\n")

print(
    json.dumps(
        scene_plan,
        indent=4,
        ensure_ascii=False
    )
)