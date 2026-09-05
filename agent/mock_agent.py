#testing ONLY (swapped for OpenRouter)
class MockAgentLLM:
    def generate(self, prompt: str, attempt: int) -> str:
        if attempt < 2:
            return(
                "Sure here's that section for you\n"
                "<<<SECTION>>>\n"
                "Too short.\n"
                "<<<END>>>\n"
            )
        fake_lesson = "Placeholder content for testing. " * 80
        return(
                "<<<SECTION>>>\n"
                + fake_lesson +
                "This is now long enough for the validator to accept during testing.\n"
                "It represents a corrected version returned after the first attempt failed\n"
                "<<<END>>>\n"
        )