PERSONA = "A learner whose pipeline breaks when the model returns prose instead of JSON"

def build_prompt(section: dict) -> str:
    return f"""Audience: {PERSONA}
Previous sections covered: {section['previous_summary']}
This section: Lesson {section['lesson']} Section {section['section_num']}, {section['name']}
Core idea that must be taught accurately: {section['core_idea']}

Constraints: Word count must be 300 to 500 words, one idea, 2 to 3 minutes of reading time. 
No video, no audio. Primarily prose, with inline HTML/SVG allowed for diagrams.
Use standard Markdown without escaping Markdown formatting characters.
Teach only the concept assigned to this section. 
Do not cover: {section['avoid']}

Builds towards checkpoint: {section['checkpoint']}
Next section (name only): {section['next_name']}

Write this section now, in full, as the actual lesson text a learner would read.
Wrap your entire response between <<<SECTION>>> and <<<END>>>, with nothing outside those markers.
"""
def build_repair_prompt(section: dict, clean_text: str, errors: list[str]) -> str:
    error_list = ""
    for e in errors:
        error_list = error_list + "- " + e + "\n"
    return f"""Audience: {PERSONA}
This section: Lesson {section['lesson']} Section {section['section_num']}, {section['name']}
Builds towards checkpoint: {section['checkpoint']}
Teach only the concept assigned to this section.
Do not cover: {section['avoid']}

Your previous response failed validation for the following reason(s):
Errors:
{error_list}

Previous response:
{clean_text}
Fix the section while preserving its original topic and meaning.
The corrected section must be 300 to 500 words.
Return only the corrected lesson section between <<<SECTION>>> and <<<END>>>.
"""