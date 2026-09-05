## Stop and Flag with an Exception

When you build a pipeline that repeatedly asks the model to fix its JSON output, you need a safety net: a maximum number of repair attempts. Continuing to feed the model after it has repeatedly failed wastes time, obscures the real problem, and may let bad data slip downstream.

### Why a limit matters
* **Predictable behavior** – The pipeline’s execution time becomes bounded, making it easier to reason about performance and to schedule work.
* **Clear failure signal** – If the model cannot produce valid JSON after the allotted tries, the issue is likely not a transient glitch but a deeper mismatch (e.g., the prompt is ambiguous, the schema is impossible, or the model lacks the needed capability). Continuing would only mask that root cause.
* **Resource protection** – Unlimited loops can consume API quotas, compute cycles, or memory, especially in batch jobs.

### Implementing the limit
1. **Set a constant** – Choose a small integer, e.g., `MAX_REPAIR_ATTEMPTS = 3`. This value should reflect how many chances you think the model needs to correct a simple formatting mistake.
2. **Track attempts** – Keep a counter that increments each time you send the model’s output back for repair.
3. **Check after each attempt** – After the model returns a candidate, run your validator. If it passes, break out of the loop and continue with the valid data.
4. **Exhausted attempts** – When the counter reaches `MAX_REPAIR_ATTEMPTS` **and** the validator still fails, you have an unrecoverable situation.

### Raising an exception
Instead of returning the malformed text or silently aborting, raise a dedicated exception that the surrounding application can catch and handle. In Python‑like pseudocode:

```python
class UnrecoverableParseError(Exception):
    """Raised when the model fails to produce valid JSON after all repair attempts."""
    pass

def get_valid_json(prompt, max_attempts=3):
    attempt = 0
    while attempt < max_attempts:
        response = model.generate(prompt)
        if validator.is_valid(response):
            return response  # success
        # otherwise, prepare a repair prompt and try again
        prompt = build_repair_prompt(response, validator.errors)
        attempt += 1
    # If we exit the loop, validation never succeeded
    raise UnrecoverableParseError(
        f"Failed to obtain valid JSON after {max_attempts} attempts."
    )
```

The exception does three things:
* **Stops the pipeline** – Control leaves the repair loop immediately.
* **Flags the failure** – The error type and message make it clear why the stop happened.
* **Enables graceful handling** – The caller can log the issue, alert an operator, fallback to a default schema, or trigger a manual review, depending on the application’s needs.

By imposing a finite number of repair attempts and raising an exception when they are exhausted, you turn an ambiguous, potentially endless retry into a deterministic, observable failure mode that the rest of your system can act upon. This practice keeps your data flow reliable and your debugging process straightforward.