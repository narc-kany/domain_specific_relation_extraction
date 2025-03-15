import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from nltk.tokenize import sent_tokenize
import re

class FinanceModel:
    """Model for finance domain entity and relation extraction using public models."""
    
    def __init__(self):
        """Initialize finance model with publicly available models."""
        try:
            # For NER, use general NER model
            self.ner_tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
            self.ner_model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
            self.ner_pipeline = pipeline("ner", model=self.ner_model, tokenizer=self.ner_tokenizer, aggregation_strategy="simple")
            
            # Finance-specific entity lists
            self.entities = {
                'COMPANY': ['apple', 'amazon', 'google', 'microsoft', 'tesla', 'bank of america', 'jpmorgan', 
                            'goldman sachs', 'morgan stanley', 'wells fargo', 'walmart', 'meta', 'facebook', 
                            'netflix', 'alibaba', 'tencent', 'samsung', 'ibm', 'intel', 'amd', 'whole foods'],
                'PRODUCT': ['iphone', 'aws', 'cloud', 'windows', 'model s', 'model 3', 'azure', 'office 365',
                            'loan', 'mortgage', 'bond', 'credit card', 'investment', 'ai product', 'fintech'],
                'METRIC': ['revenue', 'profit', 'loss', 'earnings', 'market share', 'stock price', 'growth', 
                          'dividend', 'sales', 'margin', 'income', 'debt', 'cash flow', 'eps', 'p/e ratio'],
                'EVENT': ['merger', 'acquisition', 'ipo', 'bankruptcy', 'investment', 'layoff', 'restructuring',
                         'product launch', 'earnings report', 'quarterly report', 'share buyback', 'stock split']
            }
            
            # Map general NER tags to finance entity types
            self.ner_tag_mapping = {
                'B-ORG': 'COMPANY',
                'I-ORG': 'COMPANY',
                'B-MISC': 'PRODUCT',
                'I-MISC': 'PRODUCT'
            }
            
            # Finance-specific relation types
            self.relation_types = {
                'acquired': {'source': ['COMPANY'], 'target': ['COMPANY']},
                'launched': {'source': ['COMPANY'], 'target': ['PRODUCT']},
                'increased': {'source': ['COMPANY', 'PRODUCT'], 'target': ['METRIC']},
                'decreased': {'source': ['COMPANY', 'PRODUCT'], 'target': ['METRIC']},
                'invested_in': {'source': ['COMPANY'], 'target': ['COMPANY', 'PRODUCT']}
            }
            
            # Keywords for relation extraction
            self.relation_keywords = {
                'acquired': ['acquire', 'acquisition', 'buy', 'purchase', 'takeover', 'merge'],
                'launched': ['launch', 'release', 'introduce', 'unveil', 'announce', 'debut'],
                'increased': ['increase', 'grow', 'rise', 'boost', 'improve', 'expand', 'gain', 'up'],
                'decreased': ['decrease', 'reduce', 'drop', 'decline', 'fall', 'lower', 'cut', 'down'],
                'invested_in': ['invest', 'funding', 'stake', 'share', 'partner']
            }
            
            # Create negation patterns
            self.negation_patterns = [
                r'did\s+not\s+', 
                r'didn\'t\s+', 
                r'not\s+',
                r'no\s+',
                r'failed\s+to\s+',
                r'declined\s+to\s+',
                r'unable\s+to\s+'
            ]
            
            # Sentiment indicators will be used to determine increase/decrease relations
            self.positive_indicators = ['growth', 'profit', 'success', 'positive', 'strong', 'higher', 
                                      'better', 'exceeded', 'improvement', 'outperform']
            self.negative_indicators = ['loss', 'decline', 'negative', 'weak', 'lower', 'below', 
                                      'disappointment', 'missed', 'underperform']
            
            print("Finance model initialized with public models")
            
        except Exception as e:
            print(f"Error initializing finance model: {e}")
            print("Finance model initialized with rules only")
    
    def extract_entities(self, text):
        """Extract finance-related entities using general NER and finance keywords."""
        try:
            # First use NER to identify organizations and misc entities
            ner_results = self.ner_pipeline(text)
            
            # Process NER results
            entities = []
            for entity in ner_results:
                entity_type = self.ner_tag_mapping.get(entity['entity_group'])
                if entity_type:  # Only process relevant entity types
                    # For organizations, check if they're likely finance-related
                    if entity_type == 'COMPANY':
                        # Companies often have specific suffixes
                        company_indicators = ['inc', 'corp', 'ltd', 'llc', 'plc', 'group', 'bank', 'holdings']
                        is_finance_company = any(indicator in entity['word'].lower() for indicator in company_indicators)
                        
                        # Known companies from our list
                        is_known_company = any(company.lower() in entity['word'].lower() 
                                              for company in self.entities['COMPANY'])
                        
                        if not (is_finance_company or is_known_company):
                            continue  # Skip if not likely a finance company
                    
                    # Check for duplicates
                    duplicate = False
                    for existing_entity in entities:
                        if (existing_entity['text'].lower() == entity['word'].lower() and
                            existing_entity['type'] == entity_type):
                            duplicate = True
                            break
                    
                    if not duplicate:
                        entities.append({
                            'text': entity['word'],
                            'type': entity_type,
                            'start': entity['start'],
                            'end': entity['end']
                        })
            
            # Second, supplement with finance-specific entities using keyword matching
            text_lower = text.lower()
            for entity_type in ['METRIC', 'EVENT']:  # Only add metrics and events from keywords
                for keyword in self.entities[entity_type]:
                    for match in re.finditer(r'\b' + keyword + r'\b', text_lower):
                        start = match.start()
                        end = match.end()
                        
                        # Get original case from text
                        original_text = text[start:end]
                        
                        # Check for duplicates
                        duplicate = False
                        for existing_entity in entities:
                            if (existing_entity['text'].lower() == original_text.lower() and
                                existing_entity['type'] == entity_type):
                                duplicate = True
                                break
                        
                        if not duplicate:
                            entities.append({
                                'text': original_text,
                                'type': entity_type,
                                'start': start,
                                'end': end
                            })
            
            # Remove overlapping entities (keep the longer one)
            entities.sort(key=lambda x: x['start'])
            i = 0
            while i < len(entities) - 1:
                curr = entities[i]
                next_entity = entities[i+1]
                
                if curr['end'] > next_entity['start']:  # Overlap
                    # Keep the longer entity
                    if (curr['end'] - curr['start']) >= (next_entity['end'] - next_entity['start']):
                        entities.pop(i+1)
                    else:
                        entities.pop(i)
                else:
                    i += 1
            
            return entities
            
        except Exception as e:
            print(f"Error in entity extraction: {e}")
            # Return empty list if all fails
            return []
    
    def determine_sentiment(self, sentence):
        """Simple rule-based sentiment detection for finance text."""
        sentence_lower = sentence.lower()
        
        # Count positive and negative indicators
        positive_count = sum(1 for word in self.positive_indicators if word in sentence_lower)
        negative_count = sum(1 for word in self.negative_indicators if word in sentence_lower)
        
        # Check for negations that might flip sentiment
        negation_count = sum(1 for pattern in self.negation_patterns if re.search(pattern, sentence_lower))
        
        # Simple sentiment logic
        if negation_count > 0:
            # Negations flip the sentiment
            if positive_count > negative_count:
                return 'negative'
            elif negative_count > positive_count:
                return 'positive'
            else:
                return 'neutral'
        else:
            # No negations
            if positive_count > negative_count:
                return 'positive'
            elif negative_count > positive_count:
                return 'negative'
            else:
                return 'neutral'
    
    def extract_relations(self, text, entities):
        """Extract relations between finance entities using keywords and sentiment."""
        relations = []
        sentences = sent_tokenize(text)
        
        for sentence in sentences:
            # Skip sentences with negation patterns (for relation patterns, not sentiment)
            skip_relation_patterns = False
            for neg_pattern in self.negation_patterns:
                if re.search(neg_pattern, sentence.lower()):
                    skip_relation_patterns = True
                    break
            
            # Find entities in this sentence
            sentence_entities = []
            sentence_lower = sentence.lower()
            
            for entity in entities:
                if entity['text'].lower() in sentence_lower:
                    sentence_entities.append(entity)
            
            # Need at least 2 entities for a relation
            if len(sentence_entities) < 2:
                continue
            
            # Determine sentiment of the sentence
            sentiment = self.determine_sentiment(sentence)
            
            # Check all pairs of entities in this sentence
            for i, entity1 in enumerate(sentence_entities):
                for j, entity2 in enumerate(sentence_entities):
                    if i == j:
                        continue
                    
                    # Determine potential relation types based on entity types
                    potential_relations = []
                    for rel_type, type_constraints in self.relation_types.items():
                        if (entity1['type'] in type_constraints['source'] and 
                            entity2['type'] in type_constraints['target']):
                            potential_relations.append(rel_type)
                    
                    if not potential_relations:
                        continue
                    
                    # First check explicit relation keywords if not skipping
                    relation_found = False
                    if not skip_relation_patterns:
                        for rel_type in potential_relations:
                            # Skip increase/decrease check based on keywords and check sentiment later
                            if rel_type in ['increased', 'decreased']:
                                continue
                                
                            # Check for relation keywords
                            keywords = self.relation_keywords[rel_type]
                            if any(keyword in sentence_lower for keyword in keywords):
                                # Check for duplicates
                                duplicate = False
                                for rel in relations:
                                    if (rel['source'] == entity1['text'] and 
                                        rel['target'] == entity2['text']):
                                        duplicate = True
                                        break
                                        
                                if not duplicate:
                                    relations.append({
                                        'source': entity1['text'],
                                        'target': entity2['text'],
                                        'type': rel_type
                                    })
                                    relation_found = True
                                    break  # Only one relation per entity pair
                    
                    # For metrics, use sentiment to determine increased/decreased
                    if not relation_found and 'increased' in potential_relations and 'decreased' in potential_relations:
                        # Company-Metric relation or Product-Metric relation
                        if entity2['type'] == 'METRIC':
                            rel_type = 'increased' if sentiment == 'positive' else 'decreased'
                            
                            # Check for duplicates
                            duplicate = False
                            for rel in relations:
                                if (rel['source'] == entity1['text'] and 
                                    rel['target'] == entity2['text']):
                                    duplicate = True
                                    break
                                    
                            if not duplicate:
                                relations.append({
                                    'source': entity1['text'],
                                    'target': entity2['text'],
                                    'type': rel_type
                                })
        
        # If no relations found but we have companies and products, infer company-product relations
        if not relations:
            company_entities = [e for e in entities if e['type'] == 'COMPANY']
            product_entities = [e for e in entities if e['type'] == 'PRODUCT']
            
            if company_entities and product_entities:
                for company in company_entities:
                    for product in product_entities:
                        relations.append({
                            'source': company['text'],
                            'target': product['text'],
                            'type': 'launched'
                        })
            
            # If we have companies and metrics, infer company-metric relations
            metric_entities = [e for e in entities if e['type'] == 'METRIC']
            if company_entities and metric_entities:
                for company in company_entities:
                    for metric in metric_entities:
                        # Default to increased relationship
                        relations.append({
                            'source': company['text'],
                            'target': metric['text'],
                            'type': 'increased'
                        })
        
        # Limit to the most confident relations if we have too many
        if len(relations) > 5:
            # Priority: acquired > launched > increased/decreased > others
            priority = {'acquired': 4, 'launched': 3, 'increased': 2, 'decreased': 2, 'invested_in': 1}
            relations.sort(key=lambda x: priority.get(x['type'], 0), reverse=True)
            relations = relations[:5]
        
        return relations
    
    def extract(self, text):
        """Extract both entities and relations from text."""
        entities = self.extract_entities(text)
        relations = self.extract_relations(text, entities)
        
        return entities, relations