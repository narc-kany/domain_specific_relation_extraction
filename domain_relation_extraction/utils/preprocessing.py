import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# Download NLTK resources (uncomment first time)
# nltk.download('punkt')
# nltk.download('stopwords')

def clean_text(text):
    """
    Clean and prepare text for NLP processing.
    
    Args:
        text (str): Input text to clean
        
    Returns:
        str: Cleaned text
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and numbers (keep alphanumeric and spaces)
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def tokenize_sentences(text):
    """
    Split text into sentences.
    
    Args:
        text (str): Input text
        
    Returns:
        list: List of sentences
    """
    return sent_tokenize(text)

def tokenize_words(text, remove_stopwords=False):
    """
    Tokenize text into words, optionally removing stopwords.
    
    Args:
        text (str): Input text
        remove_stopwords (bool): Whether to remove stopwords
        
    Returns:
        list: List of word tokens
    """
    tokens = word_tokenize(text)
    
    if remove_stopwords:
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token.lower() not in stop_words]
    
    return tokens

def identify_domain(text):
    """
    Attempt to identify the likely domain of the text.
    
    Args:
        text (str): Input text
        
    Returns:
        str: Identified domain ('healthcare', 'finance', 'legal', or 'unknown')
    """
    text_lower = text.lower()
    
    # Define domain-specific keywords
    healthcare_keywords = ['patient', 'doctor', 'hospital', 'disease', 'treatment', 
                          'medicine', 'symptom', 'diagnosis', 'therapy', 'medical']
    
    finance_keywords = ['bank', 'stock', 'market', 'investment', 'fund', 'profit', 
                       'revenue', 'financial', 'company', 'business', 'trade']
    
    legal_keywords = ['court', 'law', 'judge', 'legal', 'attorney', 'contract', 
                     'plaintiff', 'defendant', 'case', 'justice', 'rights']
    
    # Count keyword occurrences
    healthcare_count = sum(1 for keyword in healthcare_keywords if keyword in text_lower)
    finance_count = sum(1 for keyword in finance_keywords if keyword in text_lower)
    legal_count = sum(1 for keyword in legal_keywords if keyword in text_lower)
    
    # Determine the domain with the most keyword matches
    counts = {'healthcare': healthcare_count, 'finance': finance_count, 'legal': legal_count}
    max_domain = max(counts, key=counts.get)
    
    # Return the domain if it has at least some matches, otherwise unknown
    if counts[max_domain] > 0:
        return max_domain
    else:
        return 'unknown'

def preprocess_for_ner(text):
    """
    Preprocess text specifically for NER tasks.
    
    Args:
        text (str): Input text
        
    Returns:
        list: List of sentences ready for NER
    """
    # Clean the text but keep capitalization for NER
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Split into sentences
    sentences = sent_tokenize(text)
    
    return sentences