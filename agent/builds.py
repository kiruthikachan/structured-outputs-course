BUILD_1 = {
    "lesson": 1,
    "name": "Extract Structured Data from a Clinical Note",
    "goal": "Build a small Python CLI pipeline that starts with a short clinical note,"
            " constructs a prompt requesting a fixed JSON shape, receives a cached model "
            "response containing prose around JSON, extracts the JSON with regex, and"
            " prints a visible check after each step.",
    "artifact": "A Python pipeline that produces an extracted JSON string. This exact"
                " artifact will be extended in Lesson 2 with schema validation and repair.",
    "required_fields": "visit_type, age, gender, chief_complaint, duration, tests, rx."
                        " Keep every value simple and flat. Do not use nested objects or arrays.",
    "constraints": "The build must take less than 20 minutes. Build it incrementally rather"
                    " than dropping in finished code. Every major step must print a visible"
                    " check. Use only concepts taught in Lesson 1. Do not add schema validation,"
                    " repair loops, retries, or custom exceptions. The learner is always located in the"
                    " project root directory when running terminal commands. The learner's Python file"
                    " must be created at build/lesson-1/pipeline.py. "
                    "Every run command must be exactly: python3 build/lesson-1/pipeline.py. "
                    "Never instruct the learner to run python main.py, python pipeline.py, or to cd into"
                    " build/lesson-1."
}
BUILD_2 = {
    "lesson": 2,
    "name": "Validate and Repair Structured Output",
    "goal": "Extend the exact Lesson 1 pipeline instead of starting over. "
            "Parse the extracted JSON, validate it against a JSON schema,"
            " show the validation failure, repair the invalid response using a cached"
            " repair response, validate again, and raise a custom exception if repair"
            " attempts are exhausted.",
    "artifact": "A schema validated structured output pipeline with a bounded repair loop."
                " This will complete the course capstone.",
    "constraints": "The build must take less than 20 mins and use no more than 4 incremental steps."
                    " Every major step must print a visible check."
                    " Use only concepts taught in Lesson 2."
                    " Use jsonschema for validation."
                    " The initial cached response must fail because age is a string instead of an integer."
                    " The learner must construct a repair prompt containing the failed response and validation error,"
                    " then use a cached repair response that corrects age to an integer."
                    " Revalidate the repaired response."
                    " Do not duplicate validation logic unnecessarily."
                    " Limit repair attempts and raise StructuredOutputError if a valid output can't be produced."
                    " Keep the final program concise and focused."
                    " The build must work offline and require no API key."
                    " The learner runs the commands from the project root."
                    " The learner's file must be build/lesson-2/pipeline.py. "
                    "Every run command must be exactly: python3 build/lesson-2/pipeline.py"
}