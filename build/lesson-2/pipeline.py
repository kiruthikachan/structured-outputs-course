import json
import re
import jsonschema
from jsonschema import Draft7Validator

# ---- Schema definition -------------------------------------------------
SCHEMA = {
    "type": "object",
    "properties": {
        "visit_type": {"type": "string"},
        "age":        {"type": "integer"},
        "gender":     {"type": "string"},
        "chief_complaint": {"type": "string"},
        "duration":   {"type": "string"},
        "tests":      {"type": "string"},
        "rx":         {"type": "string"},
    },
    "required": ["visit_type", "age", "gender", "chief_complaint", "duration", "tests", "rx"],
    "additionalProperties": False
}

# ---- Custom exception --------------------------------------------------
class StructuredOutputError(Exception):
    """Raised when the model cannot produce valid JSON after all repair attempts."""
    pass

MAX_REPAIR_ATTEMPTS = 3

print("[✓] Step 1: Imports, schema, and StructuredOutputError defined")

# Step 1: define and show the clinical note
clinical_note = (
    "Patient is a 45‑year‑old male presenting with a 2‑day headache. "
    "No prior tests ordered. Prescribed acetaminophen."
)

print("Clinical note:")
print(clinical_note)
print("[✓] Step 1: Clinical note loaded and printed")

# Step 2: build the prompt requesting JSON
prompt = (
    "You are a medical assistant. Extract the following information from the clinical note "
    "and return ONLY a JSON object with the keys: visit_type, age, gender, chief_complaint, "
    "duration, tests, rx. Do not add any extra text.\n\n"
    f"Clinical note: {clinical_note}"
)

print("\nPrompt sent to the model:")
print(prompt)
print("[✓] Step 2: Prompt constructed")

# Step 3: cached model response (prose + JSON)
model_reply = (
    "Based on the note, here is the structured data:\n"
    '{"visit_type":"follow-up","age":"45","gender":"Male","chief_complaint":"headache",'
    '"duration":"2 days","tests":"none","rx":"acetaminophen"}\n'
    "Let me know if you need anything else."
)

print("\nModel reply (cached):")
print(model_reply)
print("[✓] Step 3: Cached model response ready")

# Step 4: extract JSON using regex (flat object only)
match = re.search(r'\{[^{}]+\}', model_reply)

if match:
    json_text = match.group(0)
    print("\nExtracted JSON string:")
    print(json_text)
    print("[✓] Step 4: JSON extracted with regex")
else:
    print("\nNo JSON object found.")
    print("[✗] Step 4: Extraction failed")
    # Exit early if we cannot extract JSON
    raise SystemExit("Extraction failed – nothing to validate.")

# ----- Step 2: Validate extracted JSON ---------------------------------
instance = json.loads(json_text)   # may raise json.JSONDecodeError if not valid JSON
try:
    Draft7Validator(SCHEMA).validate(instance)
    print("[✓] Step 2: Validation passed")
except jsonschema.ValidationError as ve:
    # Gather all validation errors
    errors = [error.message for error in Draft7Validator(SCHEMA).iter_errors(instance)]
    print("\n[✗] Step 2: Validation failed")
    for err in errors:
        print(f"  - {err}")
    print("[✓] Step 2: Validation failure captured")

    # ----- Step 3: Build repair prompt ---------------------------
    repair_prompt = (
        "You previously returned the following text:\n"
        f"{json_text}\n\n"
        "Your response failed schema validation with these errors:\n"
        + "\n".join([f"- {e}" for e in errors])
        + f"\n\nPlease output a valid JSON object that satisfies the schema:\n"
        + json.dumps(SCHEMA, indent=2)
        + "\nReturn only the JSON."
    )
    print("\n[✓] Step 3: Repair prompt constructed (snippet):")
    print(repair_prompt[:250] + ("..." if len(repair_prompt) > 250 else ""))

    # ----- Step 4: Use cached repaired response ------------------
    # This simulates the model's reply after seeing the repair prompt.
    # The only change: age is now an integer.
    repaired_reply = '{"visit_type":"follow-up","age":45,"gender":"Male","chief_complaint":"headache","duration":"2 days","tests":"none","rx":"acetaminophen"}'
    json_text = repaired_reply   # use the repaired JSON for next validation attempt
    print("\n[✓] Step 4: Using cached repaired response:")
    print(json_text)

    # Increment attempt counter and try validation again
    attempt = 1   # we have already tried once
    while attempt < MAX_REPAIR_ATTEMPTS:
        try:
            Draft7Validator(SCHEMA).validate(json.loads(json_text))
            print("[✓] Step 4: Validation passed after repair")
            break
        except jsonschema.ValidationError as ve2:
            errors2 = [error.message for error in Draft7Validator(SCHEMA).iter_errors(json.loads(json_text))]
            print(f"\n[✗] Step 4: Validation attempt {attempt+1} failed")
            for err in errors2:
                print(f"  - {err}")
            attempt += 1
            if attempt >= MAX_REPAIR_ATTEMPTS:
                raise StructuredOutputError(
                    f"Failed to obtain valid JSON after {MAX_REPAIR_ATTEMPTS} attempts."
                )
    else:
        # This block runs only if the while loop didn't break (should not happen here)
        raise StructuredOutputError(
            f"Failed to obtain valid JSON after {MAX_REPAIR_ATTEMPTS} attempts."
            )

# ----- Final confirmation -------------------------------------------------
final_data = json.loads(json_text)
print("\n[✓] Pipeline complete – final structured data:")
print(json.dumps(final_data, indent=2))