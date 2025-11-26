import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()

class LLMClient:
    def __init__(self):
        if GOOGLE_API_KEY:
            genai.configure(api_key=GOOGLE_API_KEY)
            self.client = genai.GenerativeModel("gemini-2.0-flash")
        else:
            self.client = None
            self.fallback = LocalLLMClient()

    def call(self, prompt: str, max_tokens: int = 256):
        if self.client:
            try:
                response = self.client.generate_content(
                    prompt,
                    generation_config={"max_output_tokens": max_tokens}
                )
                return response.text.strip()
            except Exception as e:
                return f"[ERROR calling Gemini API] {str(e)}"
        else:
            return self.fallback.call(prompt)


class LocalLLMClient:
    """Fallback responder when no API key is present."""
    def call(self, prompt: str):
        if "Summarize" in prompt:
            return (
                "Summary: The debate highlights both advantages and disadvantages. "
                "Key insights include productivity differences, human collaboration, "
                "and personal flexibility needs."
            )

        if "Opening statement" in prompt:
            return (
                "Opening: I will outline my position, focusing on the most important "
                "aspects relevant to the topic."
            )

        if "Closing" in prompt:
            return (
                "Closing: In summary, my analysis leads me to highlight the key "
                "benefits, risks, and overall balance of the topic."
            )

        # Generic fallback response
        return (
            f"I am responding to this prompt with a local fallback model. "
            f"Prompt summary: {prompt[:200]}..."
        )
