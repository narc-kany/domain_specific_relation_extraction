# Domain-Specific Relation Extraction System

This project implements a web-based system for extracting domain-specific entities and relations from unstructured text. The system supports multiple domains including healthcare and finance.

## Features

- Extract domain-specific entities and relationships
- Support for multiple domains (Healthcare, Finance)
- Interactive visualization of extracted relations
- Simple and intuitive user interface

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd domain_relation_extraction
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Download required NLTK resources:
   ```python
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```

### Running the Application

1. Start the Flask development server:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## Usage Instructions

1. Enter your domain-specific text in the input field
2. Select the appropriate domain from the dropdown menu
3. Click "Extract Relations" button
4. View the results in the table view or graph visualization

## Project Structure

```
domain_relation_extraction/
│
├── app.py                  # Main Flask application
├── models/                 # Model implementations
│   ├── __init__.py
│   ├── healthcare_model.py # Healthcare domain models
│   └── finance_model.py    # Finance domain models
│
├── utils/                  # Utility functions
│   ├── __init__.py
│   ├── preprocessing.py    # Text preprocessing functions
│   └── visualization.py    # Visualization utilities
│
├── static/                 # Static files (CSS, JS)
│   ├── css/
│   └── js/
│
├── templates/              # HTML templates
│   └── index.html          # Main application page
│
├── data/                   # Sample data and model files
│   ├── healthcare/
│   └── finance/
│
└── requirements.txt        # Project dependencies
```

## Example Inputs

### Healthcare Domain
```
Aspirin treats headache and reduces inflammation. Diabetes causes fatigue and excessive thirst. Regular exercise prevents obesity and improves cardiovascular health.
```

### Finance Domain
```
Apple launched iPhone 15 last quarter. Amazon acquired Whole Foods in 2017. Tesla's stock price increased after earnings report. Bank of America reported decreased revenue in Q3.
```

## Future Improvements

- Add support for Legal domain
- Implement more advanced NLP models
- Improve visualization with filtering options
- Add document upload functionality
- Implement batch processing for multiple texts