import os
import google.generativeai as genai

class ClinicalScribe:
    def __init__(self):
        # Configure Gemini if API key is present
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None

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
        
        if self.model and raw_text:
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
        response = self.model.generate_content(prompt)
        return response.text.strip()

