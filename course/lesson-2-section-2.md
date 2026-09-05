## Lesson 2 Section 2 – Validate Against a Schema

When a language model returns text, you often try to pull a JSON object out of that text. Even if you succeed in extracting something that looks like JSON, the data may still be unsuitable for the rest of your application. A **schema** solves this problem by describing exactly what the application expects: which fields must be present, what type each field should have, and any extra rules those values must obey.

### What a schema contains
A schema (commonly expressed as JSON Schema) is itself a JSON document that declares constraints:

- **Required fields** – lists properties that must appear; missing any of them makes the payload invalid.  
- **Data types** – specifies whether a value should be a string, number, boolean, array, or object.  
- **Value constraints** – can enforce ranges (`minimum`, `maximum`), patterns (`pattern` for regex), enumerations (`enum`), or formats (`format` for email, date‑time, etc.).  
- **Structure rules** – defines how arrays (`items`) or nested objects (`properties`) should be shaped.

By comparing the extracted JSON against this declaration, you can automatically detect problems such as a missing `user_id`, a `price` that is a string instead of a number, or a `status` that is not one of the allowed `"pending"`, `"approved"`, `"rejected"`.

### How validation fits into the pipeline
1. **Extract** – Pull the JSON substring from the model’s raw output.  
2. **Validate** – Run a schema validator (many libraries exist for Python, JavaScript, etc.) that returns a clear pass/fail result.  
3. **Gate** – If validation passes, let the data continue downstream; if it fails, halt further processing (the handling of failures is covered later).

### Why this step matters
- **Early detection** – Catches structural mismatches before they propagate to downstream logic, databases, or UI components.  
- **Predictability** – Guarantees that every piece of data reaching the next stage conforms to the contract your code assumes.  
- **Simplicity** – Shifts the burden of reasoning about correctness from custom ad‑hoc checks to a declarative, reusable schema.

### A quick example
Suppose your application expects a user record:

```json
{
  "type": "object",
  "properties": {
    "user_id": { "type": "integer", "minimum": 1 },
    "email":   { "type": "string", "format": "email" },
    "role":    { "type": "string", "enum": ["admin", "user", "guest"] }
  },
  "required": ["user_id", "email", "role"],
  "additionalProperties": false
}
```

If the model returns `{ "user_id": "42", "email": "alice@example.com" }`, validation will flag two issues: `user_id` is a string (should be integer) and the required `role` field is missing. The pipeline stops here, preventing a malformed record from corrupting later steps.

By making schema validation a routine checkpoint, you turn an unreliable prose‑heavy model output into a dependable stream of structured data that your application can safely consume.