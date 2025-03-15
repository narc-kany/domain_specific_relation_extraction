# In models/__init__.py
from transformers import AutoTokenizer, AutoModel, pipeline

def download_models():
    # Healthcare models
    print("Downloading BioBERT...")
    biobert_tokenizer = AutoTokenizer.from_pretrained("dmis-lab/biobert-v1.1")
    biobert_model = AutoModel.from_pretrained("dmis-lab/biobert-v1.1")
    
    # Finance models
    print("Downloading FinBERT...")
    finbert_tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
    finbert_model = AutoModel.from_pretrained("yiyanghkust/finbert-tone")
    
    # NER pipeline
    print("Setting up NER pipeline...")
    ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")
    
    print("All models downloaded successfully!")

if __name__ == "__main__":
    download_models()