import unittest
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.fhir_mapper import CodeMapper

class TestCodeMapper(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.mapper = CodeMapper()

    def test_icd10_mapping(self):
        """Test mapping of diagnosis terms to ICD-10 codes."""
        # Exact match logic (fuzzy lookup checks if key is IN text)
        
        # "pneumonia" -> J18.9
        result = self.mapper.map_entity("Severe Pneumonia", "PROBLEM")
        self.assertEqual(result['code'], "J18.9")
        self.assertEqual(result['system'], "ICD-10-CM")
        
        # "hypertension" -> I10
        result = self.mapper.map_entity("History of hypertension", "PROBLEM")
        self.assertEqual(result['code'], "I10")

    def test_cpt_mapping(self):
        """Test mapping of procedures/tests to CPT/HCPCS codes."""
        
        # "surgery" -> 10021
        result = self.mapper.map_entity("Elective surgery", "TREATMENT")
        self.assertEqual(result['code'], "10021")
        self.assertEqual(result['system'], "CPT/HCPCS")
        
        # "x-ray" -> 70010
        result = self.mapper.map_entity("chest x-ray", "TEST")
        self.assertEqual(result['code'], "70010")

    def test_unmapped(self):
        """Test that unknown entities return UNMAPPED."""
        result = self.mapper.map_entity("Mysterious Alien Virus", "PROBLEM")
        self.assertEqual(result['code'], "UNMAPPED")
        self.assertEqual(result['system'], "N/A")

if __name__ == '__main__':
    unittest.main()
