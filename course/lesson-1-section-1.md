# Envelope vs Contents

When a language model produces a response, it always sends two things at once: an **envelope** that tells the receiver how to interpret the message, and the **contents** that carry the actual information you care about.

Think of mailing a letter. The envelope has the address, postage, and maybe a stamp — these are the formal rules that let the postal service know where to deliver the letter and how to handle it. Inside the envelope is the letter itself: the story, the request, the poem. If the address is smudged but you can still read the recipient’s name, a human can often figure out where it should go. A machine, however, usually refuses to deliver mail unless the address matches its exact format.

The same principle applies to model output.  
- **Envelope**: the structure or format that packages the response — most commonly JSON, but it could also be plain text, XML, YAML, or even a custom delimiter scheme. The envelope defines *how* the data is organized: keys, braces, commas, quoting rules, etc.  
- **Contents**: the semantic payload — the fields and values that represent the answer, such as `{ "city": "Paris", "temperature": 18 }`. This is what your application ultimately wants to use.

Humans are good at looking past a slightly mangled envelope. If the model wraps JSON in a sentence like “Here is the answer: {\"city\":\"Paris\"}”, a person can still extract the JSON and ignore the surrounding prose. Software, however, typically expects the envelope to be *exactly* as specified. A stray character, a line break, or an extra word can cause a JSON parser to throw an error, breaking the pipeline.

Therefore, when you design a system that consumes model outputs, you must treat the envelope and the contents as separate concerns:
1. **Validate the envelope first** — ensure the response conforms to the expected format (e.g., is valid JSON).  
2. **Only then parse the contents** — pull out the fields you need.

If the envelope is unreliable, you cannot safely skip to the contents; you must either fix the envelope (by asking the model to adhere to a stricter format) or implement tolerant parsing that can recover from minor deviations — knowing that such tolerance is inherently limited compared to human flexibility.

By keeping envelope and contents distinct in your thinking, you avoid the mistake of assuming that “the model will always give me usable data” and instead build pipelines that explicitly check the format before trusting the data inside.