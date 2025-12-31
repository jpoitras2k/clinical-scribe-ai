# clinical_note_nlp
### Entity Extraction and Structured Summarization of Medical Transcriptions

*RoboGarden Applied ML Project*

## Project Context
This project was developed as part of an applied machine learning program at RoboGarden. While completed within an academic context, the project emphasizes industry-relevant NLP workflows, evaluation practices, and system-level thinking.

## Overview
This project explores natural language processing techniques applied to real-world medical transcription data. Using the **Medical Transcriptions** dataset from Kaggle, the project focuses on:
1.  **Cleaning** raw medical dictations.
2.  **Extracting** key medical entities (conditions, treatments) using spaCy.
3.  **Generating** structured SOAP-style summaries.

The dataset (`mtsamples.csv`) contains thousands of de-identified transcriptions across various medical specialties.

The emphasis is on data understanding, domain-aware NLP tools, evaluation, and limitations, rather than production deployment or clinical use.

## Planing to use SpaCy for text processing and extraction.
Link to SpaCy https://spacy.io/   Course Link https://course.spacy.io/en/

## Project Structure

```text
├── data/           # Dataset storage (raw and processed)
├── notebooks/      # Jupyter notebooks for exploration and prototyping
│   ├── 01_eda.ipynb        # Exploratory Data Analysis
│   ├── 02_extraction.ipynb # Entity Extraction logic
│   └── 03_summary.ipynb    # Summarization experiments
├── src/            # Source code for the application
│   ├── extractor.py    # Entity extraction module
│   ├── fhir_mapper.py  # Mapping entities to FHIR standards
│   ├── preprocessor.py # Text cleaning and preprocessing
│   └── summarizer.py   # Summarization logic
├── requirements.txt # Project dependencies
└── README.md       # Project documentation
```

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd clinical-scribe-ai
    ```

2.  **Create and activate a virtual environment** (recommended):
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Download Spacy Model**:
    ```bash
    python -m spacy download en_core_web_sm
    # OR for biomedical models (if using scispacy)
    # pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.1/en_core_sci_sm-0.5.1.tar.gz
    ```

## Usage

### Running Notebooks
Start the Jupyter notebook server to explore the analysis:
```bash
jupyter notebook
```
Navigate to the `notebooks/` directory and open `01_eda.ipynb` to start.

### Using the Python Modules (Future)
Once implemented, you can use the modules in `src/` to process text programmatically:
```python
from src.extractor import extract_entities
# Example usage (TBD)
```

## Disclaimer
⚠️ **This project is for educational and research purposes only.**
It is not intended for clinical use or medical decision-making. The dataset contains synthetic or anonymized medical transcriptions and may include inaccuracies or incomplete information.