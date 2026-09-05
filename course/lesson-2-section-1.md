## Lesson 2 – Section 1: Reveal – Run the Pipeline and Watch It Break

Up to now you’ve learned how to coax the model into emitting JSON, how to enable JSON mode, and how to pull a JSON blob out of the raw text. Those steps get you *a* string that parses without error, and you might assume the work is done. In practice, parsing succeeds far more often than the data is useful.

### What “valid JSON” really means
A JSON parser only checks that the text follows the grammar: braces match, quotes are escaped, commas separate items, values are strings, numbers, booleans, null, objects, or arrays. It does **not** verify:

* that every field your code expects is present,
* that the field names are spelled exactly as your code uses,
* that each value has the type you anticipate (e.g., a number vs. a numeric string),
* that the values fall within sensible ranges or follow domain‑specific constraints.

When any of those expectations is violated, the parsed object is still valid JSON, but your downstream logic will fail—often in subtle ways that are hard to spot until the pipeline runs end‑to‑end.

### A concrete failure scenario
Imagine your application asks the model for a user profile and expects this shape:

```json
{
  "id": 123,
  "name": "Ada Lovelace",
  "age": 30,
  "email": "ada@example.com"
}
```

You enable JSON mode, extract the JSON, and call `json.loads`. The model returns:

```json
{
  "id": "123",
  "name": "Ada Lovelace",
  "age": null,
  "email": "ada-at-example-dot-com"
}
```

* The parse succeeds—no JSON error is raised.
* Your code later does `user["id"] + 1` to generate a new identifier. Because `"id"` is a string, Python raises a `TypeError: can only concatenate str (not "int") to str`.
* Elsewhere you try to send a welcome email, but the malformed address causes the SMTP library to reject it.
* Later, a downstream analytics step expects `age` to be an integer for bucketing; receiving `null` skews the statistics or triggers a validation exception further down the chain.

Each of these problems stems from **semantic** mismatches, not syntactic ones. The pipeline appears to work until the moment it touches the data, at which point it crashes, produces incorrect output, or silently corrupts state.

### Why this matters
If you only verify that the response is valid JSON, you gain a false sense of security. The application still needs a mechanism to confirm that the returned data conforms to the *contract* it relies on—otherwise, bugs will surface in production, often after costly downstream effects have already occurred.

The next section will show how to express that contract and check the model’s output against it, turning the hidden failure mode into an explicit, controllable validation step.