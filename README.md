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

Here is a link to the dataset: https://www.kaggle.com/datasets/mirichoi1234/medical-transcriptions


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
├── tests/          # Unit tests for the application
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

### 1. Running the Pipeline
You can run the main processing pipeline directly from the command line. This script loads the data, runs entity extraction, and generates SOAP summaries.

**Basic usage (process 10 records):**
```bash
python main.py --limit 10 --verbose
```

**Full usage options:**
```bash
python main.py --input data/mtsamples.csv --output data/results --limit 50
```

### 2. Running Tests
To verify the system is working correctly, run the unit tests:
```bash
python -m unittest tests/test_basic.py
```

### 3. Jupyter Notebooks
Start the Jupyter notebook server to explore the analysis and visual experiments:
```bash
jupyter notebook
```
Navigate to the `notebooks/` directory and open `01_eda.ipynb` to start.

## Acknowledgments
*   This project was developed with the assistance of LLMs (Google Gemini) for code generation, debugging, and documentation. This collaboration ensured efficient implementation of standard coding patterns while ensuring human oversight on architectural decisions, domain-specific logic, and clinical accuracy.

## Disclaimer
⚠️ **This project is for educational and research purposes only.**
It is not intended for clinical use or medical decision-making. The dataset contains synthetic or anonymized medical transcriptions and may include inaccuracies or incomplete information.