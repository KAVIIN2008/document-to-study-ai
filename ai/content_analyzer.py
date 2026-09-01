import json
import ollama


MODEL_NAME = "qwen3:8b"

REQUIRED_FIELDS = {
    "topic": str,
    "learning_objectives": list,
    "core_concepts": list,
    "definitions": list,
    "key_terminology": list,
    "processes": list,
    "important_facts": list,
    "why_it_matters": list,
    "summary": str,
}


def validate_analysis(data):
    if not isinstance(data, dict):
        raise ValueError("AI response must be a JSON object.")

    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

        if not isinstance(data[field], expected_type):
            raise ValueError(
                f"Field '{field}' must be {expected_type.__name__}."
            )

    return data


def analyze_content(text):
    prompt = f"""
You are an educational content analyzer.

Analyze the COMPLETE document below and return ONLY valid JSON.

Use exactly this structure:

{{
    "topic": "",
    "learning_objectives": [],
    "core_concepts": [],
    "definitions": [],
    "key_terminology": [],
    "processes": [],
    "important_facts": [],
    "why_it_matters": [],
    "summary": ""
}}

Rules:
- Analyze the entire document as one lesson.
- Do not create video scenes.
- Do not create narration.
- Do not invent information.
- Use only information supported by the document.
- Return ONLY valid JSON.
- Do not use Markdown.
- Do not put JSON inside code fences.

DOCUMENT:

{text}
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    raw_output = response["message"]["content"]

    try:
        data = json.loads(raw_output)
    except json.JSONDecodeError as error:
        raise ValueError(
            "Qwen returned invalid JSON."
        ) from error

    return validate_analysis(data)