import unittest
import sys
import os

# Add the project root to the sys.path so we can import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.extractor import ClinicalExtractor
from src.summarizer import ClinicalScribe

class TestClinicalPipeline(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("\nSetting up ClinicalExtractor (this might take a moment to load spacy)...")
        cls.extractor = ClinicalExtractor()
        cls.scribe = ClinicalScribe()

    def test_extraction_basic(self):
        """Test that the extractor correctly identifies simple entities."""
        text = "Patient complains of severe pain and was given aspirin."
        results = self.extractor.extract(text)
        
        # Check standard lists are returned
        self.assertIn("PROBLEM", results)
        self.assertIn("TREATMENT", results)
        self.assertIn("TEST", results)
        
        # Check specific entities
        # Note: 'pain' is lowercased in the patterns logic
        self.assertIn("pain", results["PROBLEM"], "Should detect 'pain' as a PROBLEM")
        self.assertIn("aspirin", results["TREATMENT"], "Should detect 'aspirin' as a TREATMENT")

    def test_scribe_generation(self):
        """Test that the scribe generates a formatted SOAP note."""
        entities = {
            "PROBLEM": ["migraine"],
            "TREATMENT": ["ibuprofen"],
            "TEST": ["mri scan"]
        }
        metadata = {"specialty": "Neurology"}
        
        summary = self.scribe.generate_soap(entities, metadata)
        
        # Check for key headers
        self.assertIn("**SUBJECTIVE / HISTORY**", summary)
        self.assertIn("Neurology", summary)
        self.assertIn("migraine", summary)
        self.assertIn("ibuprofen", summary)

if __name__ == '__main__':
    unittest.main()
