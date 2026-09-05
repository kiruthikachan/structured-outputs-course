## Diagnose and Retry a Structured Output

When the model returns prose instead of the JSON you asked for, your pipeline can still recover by using the validation error as diagnostic feedback. The process has three clear stages: **parse**, **validate**, and **repair**.

1. **Parse the raw text**  
   First convert the model’s string output into a Python object with `json.loads`. This step is essential because the `jsonschema` library works on native Python data structures, not on the original JSON text. If `json.loads` raises a `JSONDecodeError`, the response is not valid JSON at all and you must treat it as a repair case (see below). Assuming parsing succeeds, you now have a Python value—usually a dict or list—that can be handed to the validator.

2. **Validate against the schema**  
   Feed the parsed value to `jsonschema.validate(instance=parsed, schema=my_schema)`. When the data conforms, the call returns silently and you can proceed. If the data violates the schema, the validator raises a `jsonschema.exceptions.ValidationError`. This exception carries a detailed message that pinpoints exactly what is wrong: missing required fields, wrong type, extra properties, or failed constraints. Importantly, the error object also provides the path to the offending element (`error.path`) and the failing validator (`error.validator`). This information is the diagnosis you need to tell the model how to fix its output.

3. **Construct a repair prompt**  
   Build a new prompt that includes:  
   * The original user request (or the system instruction that asked for JSON).  
   * The model’s failed response, quoted as plain text.  
   * The validation error message (or a concise summary derived from it).  
   * An explicit instruction to output only valid JSON that satisfies the schema, optionally restating the schema in plain language.  

   Example prompt snippet:  
   ```
   You previously returned:
   {{failed_response}}
   
   The validator reported: {{error_message}}.
   Please correct the output so that it conforms to the required JSON schema and return only the JSON object.
   ```

   Send this prompt back to the same model (or a fallback model) and obtain a new completion.

4. **Parse and validate the retry**  
   Apply the same `json.loads` → `jsonschema.validate` sequence to the fresh response. If validation now passes, you have successfully recovered from the initial mistake and can continue downstream. If it still fails, further attempts are outside the scope of this section.

**Key points to remember**  
* Always parse with `json.loads` before calling the validator; never feed raw text directly to `jsonschema`.  
* The validation error is not just a failure flag—it contains actionable details that guide the model’s correction.  
* A single repair attempt consists of feeding back the failed response and its error message, then re‑parsing and validating the model’s revised output.  

By treating the schema error as diagnostic information, you turn a broken structured output into a cue for the model to self‑correct, keeping your pipeline robust without aborting on the first mistake.