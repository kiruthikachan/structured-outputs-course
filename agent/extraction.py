#extract only content btwn the markers requested in prompt
def extract_section(raw_response: str) -> str:
    if "<<<SECTION>>>" not in raw_response or "<<<END>>>" not in raw_response:
        raise ValueError(
            "Could not find <<<SECTION>>>...<<<END>>> markers in the response."
            f"Raw response was in:\n{raw_response}"
        )
    content = raw_response.split("<<<SECTION>>>", 1)[1]
    content = content.split("<<<END>>>", 1)[0]
    return content.strip()

def extract_build(raw_response: str) -> str:
    if "<<<BUILD>>>" not in raw_response or "<<<END>>>" not in raw_response:
        raise ValueError(
            "Could not find <<<BUILD>>>...<<<END>>> markers in the response."
            f"Raw response was in:\n{raw_response}"
        )
    content = raw_response.split("<<<BUILD>>>", 1)[1]
    content = content.split("<<<END>>>", 1)[0]
    return content.strip()