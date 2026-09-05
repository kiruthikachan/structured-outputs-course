from prompt_builder import PERSONA

def build_build_prompt(build:dict, lesson_content: str, previous_artifact: str = "") -> str:
    previous_artifact_text = ""

    #incl prev learner artifact when build depends on earlier one
    if previous_artifact:
        previous_artifact_text = f"""
The learner already produced this artifact in the previous build along:
PREVIOUS BUILD ARTIFACT:
{previous_artifact}

The new build must extend this artifact rather than starting over.
"""
    required_fields_text = ""
    if build.get("required_fields"):
        required_fields_text = (
            f"Use these fields in the structured data: "
            f"{build['required_fields']}"
        )

    return f"""Audience:{PERSONA}
Generate the build along at the end of Lesson {build['lesson']}.
The learner has just completed the following lesson:
LESSON CONTENT:
{lesson_content}

{previous_artifact_text}
Build name: {build['name']}
Goal: {build['goal']}
Artifact the learner must finish with: {build['artifact']}
Requirements: {build['constraints']}

This is a learner-based build along. Not a conceptual lesson.
Use only concepts taught in the lesson content above.
The learner must build the program incrementally, rather than receiving the completed program immediately.

For each step:
1. Briefly explain what the learner is adding.
2. Show the code they should add or change.
3. Show the visible terminal output/check they should expect.

Provide all code necessary for the final program to run.
The resulting code must run with Python 3.12.
Use fenced Markdown Python code blocks beginning with ```python for all Python code.
At the end of the build along, include the complete final contents of build/lesson-{build['lesson']}/pipeline.py in a single ```python code block.
The final code block must contain the entire runnable program, not only the lines changed in the final step.
The build must work offline using a cached model response.
Do not require an API key for the learner to complete the build.
Do not introduce concepts the learner has not yet learned.
Wrap the entire build along between <<<BUILD>>> and <<<END>>> with nothing outside those markers."""