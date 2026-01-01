import os
import time
import re
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

class ClinicalScribe:
    def __init__(self):
        # Configure Gemini if API key is present
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
            self.model_id = 'gemini-2.5-flash'
            print("  [INFO] Gemini AI: ENABLED")
        else:
            self.client = None
            print("  [INFO] Gemini AI: DISABLED (No API Key found)")

    def generate_soap(self, entities, metadata=None):
        """
        Generate a structured SOAP note from extracted entities and metadata.
        Uses AI for the Subjective section if configured, otherwise uses a template.
        """
        if metadata is None:
            metadata = {}

        specialty = metadata.get('specialty', 'General Practice')
        raw_text = metadata.get('raw_text', '') # Expect raw text in metadata for AI
        
        # Helper to format lists
        def fmt(lst):
            return ", ".join(lst) if lst else "None detected"

        problems = fmt(entities.get('PROBLEM', []))
        treatments = fmt(entities.get('TREATMENT', []))
        tests = fmt(entities.get('TEST', []))
        
        # 1. Generate Subjective Section
        subjective_text = f"Patient presented for {specialty}. (See full transcription for details)"
        
        if self.client and raw_text:
            try:
                subjective_text = self._generate_ai_summary(raw_text)
            except Exception as e:
                print(f"Warning: AI Summarization failed ({e}), using fallback.")
        
        # 2. Construct the full SOAP Note
        summary = (
            f"**SUBJECTIVE / HISTORY**:\n"
            f"{subjective_text}\n\n"
            
            f"**OBJECTIVE / TESTS**:\n"
            f"{tests}\n\n"
            
            f"**ASSESSMENT / PROBLEMS**:\n"
            f"{problems}\n\n"
            
            f"**PLAN / TREATMENTS**:\n"
            f"{treatments}"
        )
        return summary

    def _generate_ai_summary(self, text):
        """Uses Gemini to generate a concise clinical summary."""
        prompt = (
            f"You are a medical scribe. Summarize the following clinical transcription "
            f"into a concise, professional 'Subjective' section for a SOAP note. "
            f"Focus on the history of present illness and chief complaint.\n\n"
            f"Transcription:\n{text}"
        )
        # Retry logic for Rate Limits (429)
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_id,
                    contents=prompt
                )
                return response.text.strip()
            except Exception as e:
                error_str = str(e)
                if "429" in error_str:
                    print(f"  [WARNING] Rate Limit hit. Attempt {attempt+1}/{max_retries}.")
                    # Try to extract wait time from error message
                    wait_time = 30 # Default wait
                    match = re.search(r"retry in (\d+(\.\d+)?)s", error_str)
                    if match:
                        wait_time = float(match.group(1)) + 1 # Add buffer
                    
                    if attempt < max_retries - 1:
                        print(f"            Waiting {wait_time:.1f} seconds...")
                        time.sleep(wait_time)
                    else:
                        print("            Max retries exceeded.")
                        raise # Re-raise to trigger fallback
                else:
                    raise e # Re-raise other errors immediately

