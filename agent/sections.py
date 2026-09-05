LESSON_1_SECTIONS=[
    {
        "lesson": 1,
        "section_num": 1,
        "name": "Envelope vs Contents (framing/context)",
        "previous_summary": "None, this is the first section",
        "next_name": "Prompt Instructions (asking in words)",
        "checkpoint": "Learner understands that response format and response contents are separate concerns, and that"
                        " code cannot reliably ignore conversational prose the way a human can.",
        "core_idea": "The envelope is the representation or format used to package information, "
                    "such as JSON. The contents are the actual fields and values being communicated."
                    "Humans can often recover intended information from inconsistently formatted"
                    " responses, while software generally depends on a predictable format.",
        "avoid": "Do not teach prompt instructions, JSON mode, extraction, schema validation, retries, or exceptions."
    },
    {
        "lesson": 1,
        "section_num": 2,
        "name": "Prompt Instructions (asking in words)",
        "previous_summary": "Envelope vs Contents: The response format is separate from the information inside it"
                            " and software depends on predictable formatting more than humans do.",
        "next_name": "JSON mode (API setting)",
        "core_idea": "A prompt can explicitly tell the model what output shape to return. "
                    "Clear instructions such as returning only JSON and naming the required fields "
                    "can make outputs more predictable, but prompt instructions are still requests"
                    " to the model rather than guarantees.",
        "checkpoint": "Learner can now instruct the model to return output in a fixed shape.",
        "avoid": "Do not teach JSON mode, response format API settings, JSON extraction, regex, "
                "parsing or validating model responses, checking required keys, schema validation, retries, repair loops, or exceptions."
                " Do not give implementation advice for handling failures. Only teach how prompt wording can request a fixed output shape"
                " and why prompt instructions are not guarantees."
    },
    {
        "lesson": 1,
        "section_num": 3,
        "name": "JSON mode (API setting)",
        "previous_summary": "Envelope vs contents (framing/context), and "
                            "prompt instructions (asking in words)",
        "next_name": "Extracting JSON with regex",
        "core_idea": "JSON mode is an API-level setting that provides stronger guarantees "
                    "that a successful response will be valid JSON than prompt instructions"
                    " alone. JSON mode concerns JSON syntax, not whether the response contains"
                    " the exact fields, types, or values the application expects. Explain only"
                    " the observable API behaviour, not how the provider implements it internally.",
        "checkpoint": "Learner can now instruct the model to return output in a fixed shape (prompt instruction + JSON mode).",
        "avoid": "Do not teach JSON extraction, regex, schema validation, Pydantic, checking fields or types, "
                "retries, repair loops, or exceptions. Do not speculate about how a provider internally implements JSON mode, "
                "including claims about internal retries."
                " Do not claim that valid JSON guarantees the correct fields, types, or values."
                " Describe only the observable guarantee of JSON mode."
    },
    {
        "lesson": 1,
        "section_num": 4,
        "name": "Extracting JSON with regex",
        "previous_summary": "Envelope vs contents, prompt instructions, and "
                            "JSON mode for producing structured output",
        "next_name": "None: this is the last section of lesson 1",
        "core_idea": "When a model response contains a simple JSON object surrounded by "
                    "additional prose, a regular expression can be used to locate and"
                    " extract the JSON portion of the response. Keep the example limited"
                    " to a simple JSON object with no nested objects or braces inside string values."
                    " Explain that this regex is intentionally limited and is not a general-purpose JSON parser.",
        "checkpoint": "Learner can now extract the JSON from a response"
                        " using a regular expression",
        "avoid": "Do not teach JSON parsing, schema validation, Pydantic, retries, "
                "repair loops, or exceptions. Do not present regex as a "
                "general purpose JSON parser or claim that it handles nested JSON objects."
                " Do not claim that arrays alone cause the regex to fail. The pattern has "
                " problems with nested braces and braces appearing inside string values."
    },
]
LESSON_2_SECTIONS = [
    {
        "lesson": 2,
        "section_num": 1,
        "name": "Reveal: Run the Pipeline and Watch it Break",
        "previous_summary": "Lesson 1 covered asking for JSON, using JSON mode, and extracting JSON from a response.",
        "next_name": "Validate Against a Schema",
        "core_idea": "A model response can be valid JSON and still be unusable by the application."
                    " It may contain missing fields, incorrect field names, wrong data types, or unexpected values."
                    " Running the pipeline reveals that producing and extracting JSON is not enough."
                    " The application also needs a way to determine whether the returned data"
                    " matches what it expects.",
        "checkpoint": "N/A. This section reveals why valid-looking JSON is not enough for a production pipeline.",
        "avoid": "Do not teach how to validate a response with a schema or Pydantic. Do not teach diagnosis, retries,"
                " repair loops, or exceptions. Only reveal the failure and motivate the need for validation."
    },
    {
        "lesson": 2,
        "section_num": 2,
        "name": "Validate Against a Schema",
        "previous_summary": "The learner ran Lesson 1 pipeline and saw that successfully extracting JSON does not guarantee the data is usable.",
        "next_name": "Diagnose and Retry",
        "core_idea": "A schema defines the structure and constraints the application expects from the model's response."
                    " The extracted response can be checked against that schema to catch problems"
                    " such as missing required fields, incorrect data types, or values that violate defined constraints"
                    " before the data continues through the pipeline.",
        "checkpoint": "Learner can validate the response against a schema.",
        "avoid": "Do not teach diagnosing validation failures, retrying the model, repair loops, or raising exceptions when validation fails."
    },
    {
        "lesson": 2,
        "section_num": 3,
        "name": "Diagnose and Retry",
        "previous_summary": "The learner can extract JSON and validate it against a schema, exposing specific validation errors.",
        "next_name": "Stop and Flag with an Exception",
        "core_idea": "When a parsed JSON response fails schema validation, the validation"
                    " error explains what is wrong with the data. The JSON text must first"
                    " be parsed into a Python value before it is passed to the jsonschema validator."
                    " The failed response and its schema error can then be sent back to the model with instructions"
                    " to correct the structured output, and the corrected response can be parsed and validated again.",
        "checkpoint": "Learner can diagnose a failed response and retry by feeding the response and its schema error back into the model.",
        "avoid": "Do not pass raw JSON text directly to jsonschema validation. Parse it with json.loads first."
                " Do not teach how to handle a response that continues to fail after multiple repair attempts."
                " Do not teach stopping the pipeline or raising an exception for an unrecoverable failure."
                " Cover diagnosis and a single repair attempt only."
    },
    {
        "lesson": 2,
        "section_num": 4,
        "name": "Stop and Flag with an Exception",
        "previous_summary": "The learner can validate model output and attempt repairs by feeding validation errors back into the model.",
        "next_name": "None: this is the last section of lesson 2",
        "core_idea": "A repair process should have a limit. If the model's response still fails validation after the allowed repair attempts, "
                    " the pipeline should stop rather than continue with invalid data. Raising an exception clearly flags the unrecoverable failure"
                    " so it can be handled by the application.",
        "checkpoint": "Learner can stop the pipeline and flag an unrecoverable failure using an exception.",
        "avoid": "Do not introduce new validation techniques, schema rules, or repair strategies. Focus only on limiting repair attempts, stopping"
                " the pipeline when they are exhausted, and raising an exception to flag the failure."
    },
]