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
