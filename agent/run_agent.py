import os
from sections import LESSON_1_SECTIONS, LESSON_2_SECTIONS
from prompt_builder import build_prompt, build_repair_prompt
from extraction import extract_section
# from mock_agent import MockAgentLLM
from openrouter_agent import OpenRouterAgentLLM
from validation import validate_section

ALL_SECTIONS = LESSON_1_SECTIONS + LESSON_2_SECTIONS

def run():
    # llm = MockAgentLLM()
    llm = OpenRouterAgentLLM()
    os.makedirs("course", exist_ok=True)
    #gen each course sec independently so failed sec can be retried w/o regen entire course
    for section in ALL_SECTIONS:
        print(f"Generating Lesson {section['lesson']} Section {section['section_num']}: {section['name']}...")
        prompt = build_prompt(section)

        #retry sec that fail extraction or word count validation
        for attempt in range(3):
            raw_response = llm.generate(prompt)
            try:
                clean_text = extract_section(raw_response)
            except ValueError as e:
                print(f"    attempt {attempt} failed extraction: {e}")
                prompt = build_repair_prompt(section, raw_response, ["Response must include both <<<SECTION>>> and <<<END>>> markers."])
                continue
            errors = validate_section(clean_text)
            if not errors:
                break

            print(f"    attempt {attempt + 1} failed: {errors}")
            prompt = build_repair_prompt(section, clean_text, errors)

        if errors:
            print(f"    failed after 3 attempts")
            continue

        filename = f"course/lesson-{section['lesson']}-section-{section['section_num']}.md"
        with open(filename, "w") as f:
            f.write(clean_text)
        print(f"    saved to {filename}")
    print("\nDone. Check the course/folder for your generated files.")

if __name__ == "__main__":
    run()