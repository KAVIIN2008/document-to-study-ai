import json
import ollama


MODEL_NAME = "qwen3:8b"


REQUIRED_SCENE_FIELDS = {
    "scene_number": int,
    "purpose": str,
    "narration": str,
    "visual_type": str,
}


def validate_scene_plan(data):
    if not isinstance(data, dict):
        raise ValueError("AI response must be a JSON object.")

    if "scenes" not in data:
        raise ValueError("Missing required field: scenes.")

    if not isinstance(data["scenes"], list):
        raise ValueError("'scenes' must be a list.")

    for index, scene in enumerate(data["scenes"]):

        if not isinstance(scene, dict):
            raise ValueError(
                f"Scene {index + 1} must be a JSON object."
            )

        for field, expected_type in REQUIRED_SCENE_FIELDS.items():

            if field not in scene:
                raise ValueError(
                    f"Scene {index + 1} is missing '{field}'."
                )

            if not isinstance(scene[field], expected_type):
                raise ValueError(
                    f"Scene {index + 1} '{field}' must be "
                    f"{expected_type.__name__}."
                )

    return data


def plan_scenes(script):
    script_json = json.dumps(
        script,
        indent=4,
        ensure_ascii=False
    )

    prompt = f"""
You are an expert educational video scene planner.

Your task is to transform the COMPLETE educational script below
into a sequence of production scenes.

The script has already been created from the source document.
Do not rewrite or reinterpret the lesson.

Your job is to divide the complete lesson into logical scenes
that can later be used for educational video generation.

Return ONLY valid JSON using exactly this structure:

{{
    "scenes": [
        {{
            "scene_number": 1,
            "purpose": "",
            "narration": "",
            "visual_type": ""
        }}
    ]
}}

Rules:

- Use the COMPLETE educational script.
- Preserve the meaning and information of the script.
- Do not omit important educational content.
- Divide the lesson into logical teaching units.
- Each scene must have one clear and distinct educational purpose.
- Arrange scenes in a natural teaching progression.
- Do not introduce a concept before the script explains it.
- Do not move information into a scene where it does not logically belong.
- Avoid repeating the same concept across multiple scenes.
- If two pieces of information belong to the same concept, keep them together.
- If a concept introduces a new process or structure, give it its own scene when appropriate.
- Keep related information together.
- Do not create scenes that are too short to be educationally useful.
- Do not create unnecessarily long scenes containing several unrelated concepts.
- Do not invent facts.
- Do not add scientific information that is not present in the script.
- Do not strengthen or exaggerate claims from the script.
- Do not reinterpret scientific statements.
- The narration should preserve the meaning of the original script.
- The narration should be suitable for spoken educational video.
- Scene numbers must start at 1 and increase sequentially.
- "purpose" should briefly describe the unique teaching objective of the scene.
- "narration" should contain the narration for that scene.
- "visual_type" should identify the most appropriate visual presentation for that scene.
- Prefer "process" for sequential processes.
- Prefer "diagram" for relationships or equations.
- Prefer "labeled_structure" for physical structures or components.
- Prefer "comparison" only when two or more things are explicitly being contrasted.
- Prefer "text_highlight" for short definitions or key statements.
- Use "recap" only for recap content.
- Use "title" only for the opening/title scene.

{script_json}
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

    return validate_scene_plan(data)