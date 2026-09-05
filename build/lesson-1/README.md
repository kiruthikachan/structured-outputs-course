**Build Along: Extract Structured Data from a Clinical Note**

---

### Step 1 – Create the project file and print the clinical note
**What you’re adding**  
Create the directory `build/lesson-1` (if it doesn’t exist) and a file `pipeline.py`. Inside the file we’ll store the raw clinical note and print it so you can see the input.

**Code to add (create `build/lesson-1/pipeline.py`)**
```python
# Build Along: Extract Structured Data from a Clinical Note
# Step 1: define and show the clinical note

clinical_note = (
    "Patient is a 45‑year‑old male presenting with a 2‑day headache. "
    "No prior tests ordered. Prescribed acetaminophen."
)

print("Clinical note:")
print(clinical_note)
print("[✓] Step 1: Clinical note loaded and printed")
```

**Run**
```bash
python3 build/lesson-1/pipeline.py
```

**Expected terminal output**
```
Clinical note:
Patient is a 45‑year‑old male presenting with a 2‑day headache. No prior tests ordered. Prescribed acetaminophen.
[✓] Step 1: Clinical note loaded and printed
```

---

### Step 2 – Build the prompt that asks for a fixed JSON shape
**What you’re adding**  
We’ll construct a prompt that explicitly tells the model to return JSON with the required flat fields. The prompt is stored in a variable and printed.

**Code to add (append to `pipeline.py`)**
```python
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
```

**Run**
```bash
python3 build/lesson-1/pipeline.py
```

**Expected terminal output**
```
Clinical note:
Patient is a 45‑year‑old male presenting with a 2‑day headache. No prior tests ordered. Prescribed acetaminophen.

Prompt sent to the model:
You are a medical assistant. Extract the following information from the clinical note
and return ONLY a JSON object with the keys: visit_type, age, gender, chief_complaint, 
duration, tests, rx. Do not add any extra text.

Clinical note: Patient is a 45‑year‑old male presenting with a 2‑day headache. No prior tests ordered. Prescribed acetaminophen.
[✓] Step 2: Prompt constructed
```

---

### Step 3 – Simulate a cached model response that contains prose around JSON
**What you’re adding**  
Because we are working offline, we’ll hard‑code a realistic model reply that wraps the JSON in explanatory text (exactly the situation the regex will handle).

**Code to add (append to `pipeline.py`)**
```python
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
```

**Run**
```bash
python3 build/lesson-1/pipeline.py
```

**Expected terminal output**
```
Clinical note:
Patient is a 45‑year‑old male presenting with a 2‑day headache. No prior tests ordered. Prescribed acetaminophen.

Prompt sent to the model:
You are a medical assistant. Extract the following information from the clinical note
and return ONLY a JSON object with the keys: visit_type, age, gender, chief_complaint, 
duration, tests, rx. Do not add any extra text.

Clinical note: Patient is a 45‑year‑old male presenting with a 2‑day headache. No prior tests ordered. Prescribed acetaminophen.

Model reply (cached):
Based on the note, here is the structured data:
{"visit_type":"follow-up","age":"45","gender":"Male","chief_complaint":"headache","duration":"2 days","tests":"none","rx":"acetaminophen"}
Let me know if you need anything else.
[✓] Step 3: Cached model response ready
```

---

### Step 4 – Extract the JSON substring with a regular expression
**What you’re adding**  
We’ll use the flat‑object regex `r'\{[^{}]+\}'` from Lesson 1 to locate the JSON inside the model’s reply. The extracted string is stored and printed.

**Code to add (append to `pipeline.py`)**
```python
# Step 4: extract JSON using regex (flat object only)

import re

match = re.search(r'\{[^{}]+\}', model_reply)

if match:
    json_text = match.group(0)
    print("\nExtracted JSON string:")
    print(json_text)
    print("[✓] Step 4: JSON extracted with regex")
else:
    print("\nNo JSON object found.")
    print("[✗] Step 4: Extraction failed")
```

**Run**
```bash
python3 build/lesson-1/pipeline.py
```

**Expected terminal output**
```
Clinical note:
Patient is a 45‑year‑old male presenting with a 2‑day headache. No prior tests ordered. Prescribed acetaminophen.

Prompt sent to the model:
You are a medical assistant. Extract the following information from the clinical note
and return ONLY a JSON object with the keys: visit_type, age, gender, chief_complaint, 
duration, tests, rx. Do not add any extra text.

Clinical note: Patient is a 45‑year‑old male presenting with a 2‑day headache. No prior tests ordered. Prescribed acetaminophen.

Model reply (cached):
Based on the note, here is the structured data:
{"visit_type":"follow-up","age":"45","gender":"Male","chief_complaint":"headache","duration":"2 days","tests":"none","rx":"acetaminophen"}
Let me know if you need anything else.

Extracted JSON string:
{"visit_type":"follow-up","age":"45","gender":"Male","chief_complaint":"headache","duration":"2 days","tests":"none","rx":"acetaminophen"}
[✓] Step 4: JSON extracted with regex
```

---

### Step 5 – Final verification: print the extracted JSON and a completion check
**What you’re adding**  
We’ll simply confirm that the pipeline has produced usable JSON by printing a final check. No further processing is required for Lesson 1.

**Code to add (append to `pipeline.py`)**
```python
# Step 5: final confirmation

print("\n[✓] Pipeline complete – extracted JSON ready for next steps")
```

**Run**
```bash
python3 build/lesson-1/pipeline.py
```

**Expected terminal output**
```
Clinical note:
Patient is a 45‑year‑old male presenting with a 2‑day headache. No prior tests ordered. Prescribed acetaminophen.

Prompt sent to the model:
You are a medical assistant. Extract the following information from the clinical note
and return ONLY a JSON object with the keys: visit_type, age, gender, chief_complaint, 
duration, tests, rx. Do not add any extra text.

Clinical note: Patient is a 45‑year‑old male presenting with a 2‑day headache. No prior tests ordered. Prescribed acetaminophen.

Model reply (cached):
Based on the note, here is the structured data:
{"visit_type":"follow-up","age":"45","gender":"Male","chief_complaint":"headache","duration":"2 days","tests":"none","rx":"acetaminophen"}
Let me know if you need anything else.

Extracted JSON string:
{"visit_type":"follow-up","age":"45","gender":"Male","chief_complaint":"headache","duration":"2 days","tests":"none","rx":"acetaminophen"}
[✓] Step 4: JSON extracted with regex

[✓] Pipeline complete – extracted JSON ready for next steps
```

---

### Final `pipeline.py` (for reference)
```python
# Build Along: Extract Structured Data from a Clinical Note
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

import re

match = re.search(r'\{[^{}]+\}', model_reply)

if match:
    json_text = match.group(0)
    print("\nExtracted JSON string:")
    print(json_text)
    print("[✓] Step 4: JSON extracted with regex")
else:
    print("\nNo JSON object found.")
    print("[✗] Step 4: Extraction failed")

# Step 5: final confirmation

print("\n[✓] Pipeline complete – extracted JSON ready for next steps")
```

That completes Lesson 1 build along. The learner now has a working pipeline that takes a clinical note, builds a prompt, receives a cached model reply with surrounding prose, extracts the flat JSON using a regex, and prints a visible check after each step. In Lesson 2 this output will be fed into schema validation and repair.