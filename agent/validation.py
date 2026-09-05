#course sections stay within 300-500 word lim
def validate_section(text: str) -> list[str]:
    errors = []
    word_count = len(text.split())
    if word_count < 300:
        errors.append(f"Section is too short: {word_count} words")
    if word_count > 500:
        errors.append(f"Section is too long: {word_count} words")
    return errors

#ensure runnable python and visible checkpoints
def validate_build(text: str) -> list[str]:
    errors = []
    if "```python" not in text:
        errors.append("Build along must contain Python code.")
    if "print" not in text:
        errors.append("Build must contain visible printed checks.")
    return errors