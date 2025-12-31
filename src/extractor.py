import spacy
from spacy.pipeline import EntityRuler

class ClinicalExtractor:
    def __init__(self, model_name="en_core_web_sm"):
        """
        Initialize the spaCy model and add the medical EntityRuler.
        """
        print(f"Loading spaCy model: {model_name}...")
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            print(f"Model '{model_name}' not found. Please run: python -m spacy download {model_name}")
            raise

        # Add EntityRuler for rule-based matching
        if "entity_ruler" not in self.nlp.pipe_names:
            ruler = self.nlp.add_pipe("entity_ruler", before="ner")
        else:
            ruler = self.nlp.get_pipe("entity_ruler")
        
        # Define Medical Patterns
        # Combining standard terms and specific medical vocabulary
        patterns = [
            # PROBLEMS
            {"label": "PROBLEM", "pattern": [{"LOWER": "pain"}]},
            {"label": "PROBLEM", "pattern": [{"LOWER": "fracture"}]},
            {"label": "PROBLEM", "pattern": [{"LOWER": "disease"}]},
            {"label": "PROBLEM", "pattern": [{"LOWER": "disorder"}]},
            {"label": "PROBLEM", "pattern": [{"LOWER": "syndrome"}]},
            {"label": "PROBLEM", "pattern": [{"LOWER": "pneumonia"}]},
            {"label": "PROBLEM", "pattern": [{"LOWER": "fibrillation"}]},
            {"label": "PROBLEM", "pattern": [{"LOWER": "hypertension"}]},
            {"label": "PROBLEM", "pattern": [{"LOWER": "diabetes"}]},
            {"label": "PROBLEM", "pattern": [{"LOWER": "asthma"}]},
            {"label": "PROBLEM", "pattern": [{"LOWER": "infection"}]},
            
            # TREATMENTS
            {"label": "TREATMENT", "pattern": [{"LOWER": "surgery"}]},
            {"label": "TREATMENT", "pattern": [{"LOWER": "incision"}]},
            {"label": "TREATMENT", "pattern": [{"LOWER": "excision"}]},
            {"label": "TREATMENT", "pattern": [{"LOWER": "therapy"}]},
            {"label": "TREATMENT", "pattern": [{"LOWER": "medication"}]},
            {"label": "TREATMENT", "pattern": [{"LOWER": "aspirin"}]},
            {"label": "TREATMENT", "pattern": [{"LOWER": "mg"}]},
            {"label": "TREATMENT", "pattern": [{"LOWER": "tablet"}]},
            {"label": "TREATMENT", "pattern": [{"LOWER": "procedure"}]},
            
            # TESTS
            {"label": "TEST", "pattern": [{"LOWER": "x-ray"}]},
            {"label": "TEST", "pattern": [{"LOWER": "scan"}]},
            {"label": "TEST", "pattern": [{"LOWER": "mri"}]},
            {"label": "TEST", "pattern": [{"LOWER": "ct"}]},
            {"label": "TEST", "pattern": [{"LOWER": "ultrasound"}]},
            {"label": "TEST", "pattern": [{"LOWER": "exam"}]},
            {"label": "TEST", "pattern": [{"LOWER": "labs"}]},
            {"label": "TEST", "pattern": [{"LOWER": "bloodwork"}]}
        ]
        
        ruler.add_patterns(patterns)
        print("ClinicalExtractor initialized with EntityRuler.")

    def extract(self, text):
        """
        Process text and return unique entities for each category.
        """
        if not text or not isinstance(text, str):
            return {"PROBLEM": [], "TREATMENT": [], "TEST": []}

        doc = self.nlp(text)
        entities = {
            "PROBLEM": [],
            "TREATMENT": [],
            "TEST": []
        }
        
        for ent in doc.ents:
            if ent.label_ in entities:
                entities[ent.label_].append(ent.text)
        
        # Deduplicate
        for k in entities:
            entities[k] = list(set(entities[k]))
            
        return entities
