import logging
import google.generativeai as genai
from dotenv import load_dotenv
import os
import requests

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class LLMService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not found in .env file.")
        genai.configure(api_key=self.api_key)

    async def stream_llm(self, text: str) -> str:
        """Stream response from Gemini LLM and accumulate it."""
        if not self.api_key:
            raise ValueError("Gemini API key is missing.")

        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            accumulated_response = ""
            stream = model.generate_content(text, stream=True)

            for chunk in stream:
                if chunk.text:
                    accumulated_response += chunk.text
                    print(f"LLM Stream: {accumulated_response}", end="\r")  # Overwrite line

            print()  # New line after completion

            if not accumulated_response:
                raise ValueError("No response from Gemini LLM stream.")

            return accumulated_response

        except genai.APIError as e:
            logger.error(f"Gemini API error during streaming: {str(e)}")
            raise
        except requests.RequestException as e:
            logger.error(f"Network error during LLM streaming: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected LLM streaming error: {str(e)}")
            raise
