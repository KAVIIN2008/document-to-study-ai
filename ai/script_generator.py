import json
import ollama


MODEL_NAME = "qwen3:8b"


REQUIRED_FIELDS = {
    "title": str,
    "introduction": str,
    "sections": list,
    "recap": str,
    "final_summary": str,
}


def validate_script(data):
    if not isinstance(data, dict):
        raise ValueError("AI response must be a JSON object.")

    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

        if not isinstance(data[field], expected_type):
            raise ValueError(
                f"Field '{field}' must be {expected_type.__name__}."
            )

    for index, section in enumerate(data["sections"]):
        if not isinstance(section, dict):
            raise ValueError(
                f"Section {index + 1} must be a JSON object."
            )

        if "heading" not in section:
            raise ValueError(
                f"Section {index + 1} is missing 'heading'."
            )

        if "explanation" not in section:
            raise ValueError(
                f"Section {index + 1} is missing 'explanation'."
            )

        if not isinstance(section["heading"], str):
            raise ValueError(
                f"Section {index + 1} 'heading' must be a string."
            )

        if not isinstance(section["explanation"], str):
            raise ValueError(
                f"Section {index + 1} 'explanation' must be a string."
            )

    return data


def generate_script(analysis):
    analysis_json = json.dumps(
        analysis,
        indent=4,
        ensure_ascii=False
    )

    prompt = f"""
You are an expert educational script writer.

Your task is to transform the COMPLETE structured content analysis
into ONE coherent educational lesson script.

The lesson must teach the entire document from beginning to end.

Return ONLY valid JSON using exactly this structure:

{{
    "title": "",
    "introduction": "",
    "sections": [
        {{
            "heading": "",
            "explanation": ""
        }}
    ],
    "recap": "",
    "final_summary": ""
}}

Rules:

- Use the COMPLETE structured content provided below.
- Preserve the important information from the source document.
- Organize the lesson in a logical teaching sequence.
- Explain concepts clearly and progressively.
- Write for a student who is learning the topic.
- Use simple and natural educational language.
- Include important definitions and terminology where appropriate.
- Explain important processes in the correct order.
- Include why the topic matters when relevant.
- Do not invent facts that are not supported by the structured content.
- Do not create video scenes.
- Do not describe camera shots or visuals.
- Do not include stage directions.
- Do not include sound effects.
- Do not create scene numbers.
- Do not create timestamps.
- Do not write Markdown.
- Return ONLY valid JSON.
- Do not put JSON inside code fences.

STRUCTURED CONTENT:

{analysis_json}
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

    return validate_script(data)