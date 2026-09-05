import os
from builds import BUILD_1, BUILD_2
from build_prompt_builder import build_build_prompt
from extraction import extract_build
from validation import validate_build
from openrouter_agent import OpenRouterAgentLLM

def load_lesson(lesson_num: int):
    lesson_files=[
        f"course/lesson-{lesson_num}-section-1.md",
        f"course/lesson-{lesson_num}-section-2.md",
        f"course/lesson-{lesson_num}-section-3.md",
        f"course/lesson-{lesson_num}-section-4.md"
    ]
    lesson_content = ""

    for path in lesson_files:
        with open(path, "r") as f:
            lesson_content += f.read() + "\n\n"
    return lesson_content

#B2 uses learner artifact prod by B1
def load_prev_artifact() -> str:
    with open("build/lesson-1/pipeline.py", "r") as f:
        return f.read()

def generate_build(llm, build : dict, lesson_content: str, previous_artifact: str = ""):
    lesson_num = build["lesson"]
    print(f"\nGenerating lesson {lesson_num} build along....")
    prompt = build_build_prompt(build,lesson_content, previous_artifact)
    raw_response = llm.generate(prompt)
    try:
        clean_text = extract_build(raw_response)
    except ValueError as e:
        print(e)
        return False
    errors = validate_build(clean_text)
    if errors:
        print(f"Build failed validation with error(s): {errors}")
        return False
    folder = f"build/lesson-{lesson_num}"
    os.makedirs(folder, exist_ok=True)

    filename = f"{folder}/README.md"

    with open(filename, "w") as f:
        f.write(clean_text)
    print(f"Saved to {filename}")

    return True

def run():
    llm = OpenRouterAgentLLM()
    #build 1 reuse so b2 extends the same artifact learner created
    if os.path.exists("build/lesson-1/README.md") and os.path.exists("build/lesson-1/pipeline.py"):
        print("Build 1 already exists. Reusing it.")
    else:
        print("Loading Lesson 1...")
        lesson_1_content = load_lesson(1)
        build_1_success = generate_build(llm, BUILD_1, lesson_1_content)

        if not build_1_success:
            print("Build 1 failed. Stopping.")
            return
    if not os.path.exists("build/lesson-1/pipeline.py"):
        print("\nBuild 1 README was generated, but build/lesson-1/pipeline.py does not exist yet.")
        print("Copy the AI-generated final pipeline.py from the Build 1 README into build/lesson-1/pipeline.py, then run this script again.")
        return

    #build 2
    print("\nLoading lesson 2...")
    lesson_2_content = load_lesson(2)

    #pass completed B1 pipeline into B2 generation prompt
    print("Loading Build 1 artifact..")
    previous_artifact = load_prev_artifact()

    build_2_success = generate_build(llm, BUILD_2, lesson_2_content, previous_artifact)

    if not build_2_success:
        print("Build 2 failed.")
        return
    print("\nBoth build alongs generated successfully.")

if __name__ == "__main__":
    run()