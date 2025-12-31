class CodeMapper:
    def __init__(self):
        # Simplified Dictionary Mapping for Demonstration
        # In a real system, this would be a database or API lookup
        
        self.icd10_registry = {
            "pain": {"code": "R52", "desc": "Pain, unspecified"},
            "fracture": {"code": "T14.8", "desc": "Fracture of unspecified body region"},
            "disease": {"code": "R69", "desc": "Illness, unspecified"},
            "disorder": {"code": "R69", "desc": "Illness, unspecified"},
            "syndrome": {"code": "R69", "desc": "Illness, unspecified"},
            "pneumonia": {"code": "J18.9", "desc": "Pneumonia, unspecified organism"},
            "fibrillation": {"code": "I48.91", "desc": "Unspecified atrial fibrillation"},
            "hypertension": {"code": "I10", "desc": "Essential (primary) hypertension"},
            "diabetes": {"code": "E11.9", "desc": "Type 2 diabetes mellitus without complications"},
            "asthma": {"code": "J45.909", "desc": "Unspecified asthma, uncomplicated"},
            "infection": {"code": "B99.9", "desc": "Unspecified infectious disease"},
        }
        
        self.cpt_registry = {
            "surgery": {"code": "10021", "desc": "Fine needle aspiration biopsy, without imaging guidance"}, # Placeholder generic
            "incision": {"code": "10060", "desc": "Incision and drainage of abscess"},
            "excision": {"code": "11400", "desc": "Excision, benign lesion including margins"},
            "therapy": {"code": "97110", "desc": "Therapeutic procedure, 1 or more areas"},
            "medication": {"code": "99605", "desc": "Medication therapy management service(s)"},
            "aspirin": {"code": "J7604", "desc": "Acetylsalicylic acid, oral"}, # HCPCS
            "mg": {"code": "N/A", "desc": "Dosage Unit"}, 
            "tablet": {"code": "N/A", "desc": "Form"},
            "procedure": {"code": "99213", "desc": "Office or other outpatient visit"}, # Generic Eval/Mgmt
            "x-ray": {"code": "70010", "desc": "Myelography, posterior fossa, radiological supervision and interpretation"}, # Generic
            "scan": {"code": "70450", "desc": "Computed tomography, head or brain; without contrast material"}, # Generic CT
            "mri": {"code": "70551", "desc": "Magnetic resonance (eg, proton) imaging, brain; without contrast material"},
            "ct": {"code": "70450", "desc": "Computed tomography, head or brain; without contrast material"},
            "ultrasound": {"code": "76700", "desc": "Ultrasound, abdominal, real time with image documentation"},
            "exam": {"code": "99213", "desc": "Office or other outpatient visit"},
            "labs": {"code": "80050", "desc": "General health panel"},
            "bloodwork": {"code": "36415", "desc": "Collection of venous blood by venipuncture"},
        }

    def map_entity(self, text, category):
        """
        Maps a text entity to a code based on its category.
        Returns a dict with code, system, and description.
        """
        text_lower = text.lower()
        
        if category == "PROBLEM":
            # Lookup ICD-10
            match = self._fuzzy_lookup(text_lower, self.icd10_registry)
            if match:
                return {
                    "text": text,
                    "code": match['code'],
                    "system": "ICD-10-CM",
                    "description": match['desc']
                }
        
        elif category in ["TREATMENT", "TEST"]:
            # Lookup CPT/HCPCS
            match = self._fuzzy_lookup(text_lower, self.cpt_registry)
            if match:
                return {
                    "text": text,
                    "code": match['code'],
                    "system": "CPT/HCPCS",
                    "description": match['desc']
                }
        
        # Fallback if no code found
        return {
            "text": text,
            "code": "UNMAPPED",
            "system": "N/A",
            "description": "No Helper mapping found"
        }

    def _fuzzy_lookup(self, text, registry):
        # A simple keyword match - if registry key is IN the text
        # e.g. "acute pneumonia" matches key "pneumonia"
        for key, val in registry.items():
            if key in text:
                return val
        return None
