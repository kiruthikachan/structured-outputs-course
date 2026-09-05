## JSON mode: an API‑level guarantee of syntactically valid output

When you call a language‑model API you usually shape the answer by writing a prompt that tells the model “return JSON”. Prompt instructions work, but they rely on the model’s ability to follow natural‑language guidance, and occasional slips can produce text that is not parsable JSON (missing braces, stray commentary, etc.). JSON mode is a separate switch you flip in the request that tells the service: *whatever the model decides to emit, wrap it in a contract that the returned payload must be valid JSON*.

### What you observe when JSON mode is on
1. **Response format field** – you add a parameter such as `response_format: {type: "json_object"}` (or the provider‑specific equivalent).  
2. **Successful HTTP 200 response** – the body contains a field (often `choices[0].message.content`) that holds a string.  
3. **Parsability test** – if you take that string and feed it to a standard JSON parser (`JSON.parse`, `json.loads`, etc.) the operation will **never** throw a syntax error. The parser will produce a value—either an object, an array, a string, number, boolean, or null—depending on what the model generated.  
4. **No guarantee about shape** – the parser may return `{}` or `["hello", 42]`. The content could be missing the fields you hoped for, have wrong types, or contain unexpected keys. JSON mode only assures that *what you get can be read as JSON*; it does not promise that the JSON matches any schema you have in mind.

### What you do not see
- The service does **not** inspect the model’s output and rewrite it to fit a particular structure.  
- There is no hidden retry loop that keeps asking the model until it produces a specific key‑value pair; the guarantee stops at syntactic validity.  
- Errors about missing or incorrect fields are **not** prevented by JSON mode; they must be handled later by your application code.

### When to use it
Enable JSON mode whenever your downstream code expects to parse the model’s reply with a JSON parser and you want to eliminate the chance of a parse failure caused by stray prose. Combine it with clear prompt instructions that describe the *desired* shape (fields, types, values) so that, when the model complies, the JSON you receive is both syntactically correct and semantically useful.

By treating JSON mode as an API‑level switch that guarantees only valid JSON syntax, you separate the concern of “can I read this?” from “does it contain what I need?”—making the overall pipeline more predictable.