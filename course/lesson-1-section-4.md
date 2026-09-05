## Extracting JSON with a Regular Expression

When a language model returns a mixture of explanatory text and a JSON object, you often need only the JSON part. A simple regular expression can locate that JSON snippet as long as the object is *flat*—no nested braces and no brace characters appearing inside string values. This approach is deliberately limited; it is **not** a general‑purpose JSON parser and will break if the JSON becomes more complex.

### The pattern

```regex
{[\s\S]*?}
```

* `\{` and `\}` match the literal opening and closing curly braces.
* `[\s\S]*?` is a “lazy” quantifier that matches any character, including newlines (`\s` for whitespace, `\S` for non‑whitespace), the smallest number of times needed to reach the next `}`.

Because the quantifier is lazy, the pattern stops at the first closing brace it sees after the opening brace. This works when the JSON object contains only top‑level key‑value pairs, such as:

```json
{ "name": "Ada", "age": 28, "city": "London" }
```

If the response looks like:

```
The model thinks the answer is:
{ "name": "Ada", "age": 28, "city": "London" }
Hope that helps!
```

applying the regex yields the substring `{ "name": "Ada", "age": 28, "city": "London" }`, which you can then feed to `json.loads` (or your language’s equivalent) to obtain a usable data structure.

### Why this regex is limited

* **Nested objects** – If a value itself is an object (`{ "info": { "role": "engineer" } }`), the pattern will stop at the first inner `}`, returning `{ "info": {` which is invalid JSON.
* **Braces inside strings** – A string value like `"note": "Use { } to denote placeholders"` contains literal braces. The regex will treat the first `}` inside the string as the object’s end, truncating the JSON prematurely.
* **Arrays** – While an array at the top level (`[1,2,3]`) is not matched by this pattern, the failure mode is not because arrays are inherently problematic; it’s simply that the pattern looks for curly braces only.

### When to use it

Use this regex only when you control the prompt and can guarantee that the model will output a *single*, flat JSON object possibly wrapped in prose. If there is any chance of nesting, escaped braces, or more complex structures, switch to a proper JSON parser or a more robust extraction strategy (which will be covered in later lessons).

By mastering this limited regex, you now have a quick tool to pull out simple JSON snippets from model outputs, paving the way for more advanced handling in subsequent sections.