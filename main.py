import pandas as pd
import os
import argparse
from src.extractor import ClinicalExtractor
from src.summarizer import ClinicalScribe

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Medical Clinic Scribe AI - Production Pipeline")
    parser.add_argument("--input", default="data/mtsamples.csv", help="Path to input CSV file")
    parser.add_argument("--output", default="data/output", help="Directory to save results")
    parser.add_argument("--limit", type=int, default=50, help="Number of notes to process (for Speed)")
    
    args = parser.parse_args()
    
    # Validate Input
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found.")
        return

    # Ensure output directory exists
    os.makedirs(args.output, exist_ok=True)
    
    # 1. Initialize Components
    print("Initializing System Components...")
    extractor = ClinicalExtractor()
    scribe = ClinicalScribe()
    
    # 2. Load Data
    print(f"Loading data from {args.input}...")
    df = pd.read_csv(args.input)
    df = df.dropna(subset=['transcription'])
    
    # Process a subset or all
    if args.limit > 0:
        print(f"Limiting processing to first {args.limit} records.")
        df = df.head(args.limit).copy()
    
    # 3. Processing Loop
    print("Starting processing loop...")
    
    results = []
    
    for idx, row in df.iterrows():
        text = row['transcription']
        specialty = row.get('medical_specialty', 'Unknown')
        
        # A. Extract Entities
        entities = extractor.extract(text)
        
        # B. Generate Summary
        summary = scribe.generate_soap(entities, metadata={'specialty': specialty})
        
        # Store result
        results.append({
            'original_id': idx,
            'specialty': specialty,
            'generated_soap': summary,
            'problems_found': entities['PROBLEM'],
            'treatments_found': entities['TREATMENT'],
            'tests_found': entities['TEST']
        })
        
        if len(results) % 10 == 0:
            print(f"Processed {len(results)} records...")

    # 4. Save Results
    output_df = pd.DataFrame(results)
    output_path = os.path.join(args.output, "production_results.csv")
    output_df.to_csv(output_path, index=False)
    
    print(f"Done! Results saved to {output_path}")

if __name__ == "__main__":
    main()
