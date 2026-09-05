## Build Along: Validate and Repair Structured Output

You already have a pipeline that extracts a JSON blob from a model’s reply (the “clinical note” example).  
Now we will extend that pipeline to:

1. Validate the extracted JSON against a JSON Schema.  
2. Show the validation failure (age is a string, should be an integer).  
3. Build a repair prompt that includes the failed JSON and the validation errors.  
4. Use a cached “repaired” model reply (where age is an integer), re‑validate, and either accept the data or raise a custom exception after a bounded number of attempts.

Each step adds a small, clearly‑marked block of code and prints a visible check so you can see the pipeline progress.

---

### Step 1 – Add imports, schema, and custom exception
**What you add:**  
- Import `json`, `re`, and `jsonschema`.  
- Define the JSON Schema that expects an integer `age`.  
- Define a custom `StructuredOutputError`.  
- Set a constant for the maximum repair attempts.  
- Print a check that the imports and schema are ready.

**Code to add/replace (place at the top of the file, after the existing imports):**

```python
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
```

**Expected terminal output after this step:**  
```
[✓] Step 1: Imports, schema, and StructuredOutputError defined
```

---

### Step 2 – Validate the extracted JSON and show the failure
**What you add:**  
- After you extract `json_text` with the regex (your existing Step 4), try to validate it against the schema.  
- If validation fails, collect the error messages and print them.  
- Print a check indicating that validation failed (as expected).

**Code to add/replace (insert after the line `print("[✓] Step 4: JSON extracted with regex")` and before the final confirmation):**

```python
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
```

**Expected terminal output after this step (note the validation error about `age` being a string):**  
```
[✓] Step 4: JSON extracted with regex

[✗] Step 2: Validation failed
  - 'age' is not of type 'integer'
[✓] Step 2: Validation failure captured
```

---

### Step 3 – Build a repair prompt from the failed JSON and errors
**What you add:**  
- If validation failed, construct a prompt that shows the model its previous output, lists the validation errors, and repeats the schema.  
- Print a snippet of the prompt and a check that the prompt was built.

**Code to add/replace (inside the `except jsonschema.ValidationError` block, right after printing the errors):**

```python
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
```

**Expected terminal output after this step (continuing from the previous step):**  
```
[✓] Step 3: Repair prompt constructed (snippet):
You previously returned the following text:
{
  "visit_type":"follow-up",
  "age":"45",
  "gender":"Male",
  "chief_complaint":"headache",
  "duration":"2 days",
  "tests":"none",
  "rx":"acetaminophen"
}

Your response failed schema validation with these errors:
- 'age' is not of type 'integer'

Please output a valid JSON object that satisfies the schema:
{
  "type": "object",
  "properties": {
...
```

---

### Step 4 – Use a cached repaired response, re‑validate, and handle success or exhaustion
**What you add:**  
- Provide a cached model reply where `age` is an integer (the “repaired” output).  
- Replace `json_text` with this repaired string, re‑run validation, and print success.  
- If validation still fails after the allowed number of attempts, raise `StructuredOutputError`.  
- Print a final check showing the pipeline completed with valid structured data.

**Code to add/replace (still inside the same `except` block, after constructing the repair prompt):**  

```python
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
```

**After the `while` loop, add the final confirmation (replace the existing final confirmation block):**  

```python
# ----- Final confirmation -------------------------------------------------
final_data = json.loads(json_text)
print("\n[✓] Pipeline complete – final structured data:")
print(json.dumps(final_data, indent=2))
```

**Expected terminal output after this step (showing success after the repair):**  
```
[✓] Step 4: Using cached repaired response:
{"visit_type":"follow-up","age":45,"gender":"Male","chief_complaint":"headache","duration":"2 days","tests":"none","rx":"acetaminophen"}

[✓] Step 4: Validation passed after repair

[✓] Pipeline complete – final structured data:
{
  "visit_type": "follow-up",
  "age": 45,
  "gender": "Male",
  "chief_complaint": "headache",
  "duration": "2 days",
  "tests": "none",
  "rx": "acetaminophen"
}
```

If the repaired response were still invalid and you exhausted `MAX_REPAIR_ATTEMPTS`, the program would raise `StructuredOutputError` with a clear message.

---

## Final Program (copy‑paste into `build/lesson-2/pipeline.py`)

```python
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
```

Run the program from the project root with:

```bash
python3 build/lesson-2/pipeline.py
```

You should see the checks and output described above, confirming that the pipeline now validates, repairs, and returns a schema‑compliant JSON object.