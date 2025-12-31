class ClinicalScribe:
    def __init__(self):
        pass

    def generate_soap(self, entities, metadata=None):
        """
        Generate a structured SOAP note from extracted entities and metadata.
        
        Args:
            entities (dict): Dictionary with keys 'PROBLEM', 'TREATMENT', 'TEST'.
            metadata (dict, optional): Context like {'specialty': 'Cardiology'}.
        """
        if metadata is None:
            metadata = {}

        specialty = metadata.get('specialty', 'General Practice')
        
        # Helper to format lists
        def fmt(lst):
            return ", ".join(lst) if lst else "None detected"

        problems = fmt(entities.get('PROBLEM', []))
        treatments = fmt(entities.get('TREATMENT', []))
        tests = fmt(entities.get('TEST', []))
        
        # Construct the summary
        summary = (
            f"**SUBJECTIVE / HISTORY**:\n"
            f"Patient presented for {specialty}. (See full transcription for details)\n\n"
            
            f"**OBJECTIVE / TESTS**:\n"
            f"{tests}\n\n"
            
            f"**ASSESSMENT / PROBLEMS**:\n"
            f"{problems}\n\n"
            
            f"**PLAN / TREATMENTS**:\n"
            f"{treatments}"
        )
        return summary
