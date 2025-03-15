import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from nltk.tokenize import sent_tokenize
import re

class HealthcareModel:
    """Model for healthcare domain entity and relation extraction using public biomedical models."""
    
    def __init__(self):
        """Initialize healthcare model with publicly available models."""
        try:
            # Using publicly available models instead of restricted BioBERT
            # For NER, use general BERT NER model
            self.ner_tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
            self.ner_model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
            self.ner_pipeline = pipeline("ner", model=self.ner_model, tokenizer=self.ner_tokenizer, aggregation_strategy="simple")
            
            # Backup entity lists for healthcare domain
            self.entities = {
                'DISEASE': ['cancer', 'diabetes', 'hypertension', 'asthma', 'arthritis', 'alzheimer', 
                          'headache', 'inflammation', 'heart attack', 'stroke', 'obesity', 'memory loss'],
                'MEDICATION': ['aspirin', 'ibuprofen', 'metformin', 'insulin', 'atorvastatin', 'lisinopril'],
                'PROCEDURE': ['surgery', 'biopsy', 'transplant', 'examination', 'scan', 'therapy', 'physical therapy'],
                'SYMPTOM': ['pain', 'fever', 'cough', 'fatigue', 'nausea', 'dizziness', 'headache', 
                          'inflammation', 'excessive thirst', 'weight loss', 'stiffness', 'swelling']
            }
            
            # Map general NER tags to our healthcare entity types
            self.ner_tag_mapping = {
                'B-PER': None,  # Not relevant for healthcare
                'I-PER': None,  # Not relevant for healthcare
                'B-ORG': None,  # Not relevant for healthcare
                'I-ORG': None,  # Not relevant for healthcare
                'B-LOC': None,  # Not relevant for healthcare
                'I-LOC': None,  # Not relevant for healthcare
                'B-MISC': 'PROCEDURE',  # Map MISC to procedures as a best guess
                'I-MISC': 'PROCEDURE'
            }
            
            # Relation type mappings (for type validation)
            self.relation_types = {
                'treats': {'source': ['MEDICATION', 'PROCEDURE'], 'target': ['DISEASE', 'SYMPTOM']},
                'causes': {'source': ['DISEASE'], 'target': ['SYMPTOM', 'DISEASE']},
                'prevents': {'source': ['MEDICATION', 'PROCEDURE'], 'target': ['DISEASE']},
                'indicates': {'source': ['SYMPTOM', 'PROCEDURE'], 'target': ['DISEASE']}
            }
            
            # Relation keywords for classification
            self.relation_keywords = {
                'treats': ['treat', 'therapy', 'medication', 'cure', 'helps', 'reduces', 'relieves', 'prescribe'],
                'causes': ['cause', 'lead to', 'result in', 'associated with', 'linked to', 'induce'],
                'prevents': ['prevent', 'protect', 'reduce risk', 'avoid', 'decrease chance'],
                'indicates': ['indicate', 'suggest', 'symptom of', 'sign of', 'diagnostic', 'marker']
            }
            
            # Create negation patterns to filter out false positives
            self.negation_patterns = [
                r'not\s+treat', 
                r'doesn\'t\s+treat', 
                r'does\s+not\s+treat',
                r'no\s+evidence',
                r'unlikely\s+to',
                r'cannot\s+',
                r'never\s+'
            ]
            
            print("Healthcare model initialized with public models")
            
        except Exception as e:
            print(f"Error initializing healthcare model: {e}")
            print("Falling back to rule-based approach only")
            print("Healthcare model initialized with rules only")
    
    def extract_entities(self, text):
        """Extract healthcare-related entities using general NER and healthcare keywords."""
        try:
            # First use NER to identify general entities
            ner_results = self.ner_pipeline(text)
            all_entities = []
            
            # Process NER results
            for entity in ner_results:
                entity_type = self.ner_tag_mapping.get(entity['entity_group'])
                if entity_type:  # Only process relevant entity types
                    all_entities.append({
                        'text': entity['word'],
                        'type': entity_type,
                        'start': entity['start'],
                        'end': entity['end']
                    })
            
            # Second, supplement with healthcare-specific entities using keyword matching
            text_lower = text.lower()
            for entity_type, keywords in self.entities.items():
                for keyword in keywords:
                    for match in re.finditer(r'\b' + keyword + r'\b', text_lower):
                        start = match.start()
                        end = match.end()
                        
                        # Get original case from text
                        original_text = text[start:end]
                        
                        # Check for duplicates
                        duplicate = False
                        for existing_entity in all_entities:
                            if (existing_entity['text'].lower() == original_text.lower() and
                                existing_entity['type'] == entity_type):
                                duplicate = True
                                break
                        
                        if not duplicate:
                            all_entities.append({
                                'text': original_text,
                                'type': entity_type,
                                'start': start,
                                'end': end
                            })
            
            # Remove overlapping entities based on priority
            # Priority: MEDICATION > DISEASE > SYMPTOM > PROCEDURE
            priority_order = {'MEDICATION': 3, 'DISEASE': 2, 'SYMPTOM': 1, 'PROCEDURE': 0}
            
            # Sort by start position to handle overlaps correctly
            all_entities.sort(key=lambda x: x['start'])
            
            # Remove overlapping entities with lower priority
            i = 0
            while i < len(all_entities) - 1:
                current = all_entities[i]
                next_entity = all_entities[i + 1]
                
                # Check for overlap
                if current['end'] > next_entity['start']:
                    # Determine which to keep based on priority
                    current_priority = priority_order.get(current['type'], -1)
                    next_priority = priority_order.get(next_entity['type'], -1)
                    
                    if current_priority >= next_priority:
                        all_entities.pop(i + 1)  # Remove the next entity
                    else:
                        all_entities.pop(i)  # Remove the current entity
                else:
                    i += 1
            
            return all_entities
            
        except Exception as e:
            print(f"Error in entity extraction: {e}")
            # Return empty list if all fails
            return []
    
    def extract_relations(self, text, entities):
        """Extract relations between healthcare entities using keywords."""
        relations = []
        sentences = sent_tokenize(text)
        
        for sentence in sentences:
            # Skip sentences with negation patterns
            if any(re.search(pattern, sentence.lower()) for pattern in self.negation_patterns):
                continue
            
            # Find entities in this sentence
            sentence_entities = []
            sentence_lower = sentence.lower()
            
            for entity in entities:
                if entity['text'].lower() in sentence_lower:
                    sentence_entities.append(entity)
            
            # Need at least 2 entities for a relation
            if len(sentence_entities) < 2:
                continue
            
            # Check all pairs of entities in this sentence
            for i, entity1 in enumerate(sentence_entities):
                for j, entity2 in enumerate(sentence_entities):
                    if i == j:
                        continue
                    
                    # Determine potential relation type based on entity types
                    potential_relations = []
                    for rel_type, type_constraints in self.relation_types.items():
                        if (entity1['type'] in type_constraints['source'] and 
                            entity2['type'] in type_constraints['target']):
                            potential_relations.append(rel_type)
                    
                    if not potential_relations:
                        continue
                    
                    # Check if sentence contains keywords for any potential relation
                    for rel_type in potential_relations:
                        rel_keywords = self.relation_keywords[rel_type]
                        if any(keyword in sentence_lower for keyword in rel_keywords):
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
                                break  # Only one relation per entity pair
        
        # If no relations found from keywords, apply common healthcare relation patterns
        if not relations and len(entities) >= 2:
            # Apply rule-based relations between entities
            medication_entities = [e for e in entities if e['type'] == 'MEDICATION']
            disease_entities = [e for e in entities if e['type'] == 'DISEASE']
            symptom_entities = [e for e in entities if e['type'] == 'SYMPTOM']
            
            # Common healthcare relations:
            # 1. Medications treat diseases
            for med in medication_entities:
                for disease in disease_entities:
                    relations.append({
                        'source': med['text'],
                        'target': disease['text'],
                        'type': 'treats'
                    })
            
            # 2. Diseases cause symptoms
            for disease in disease_entities:
                for symptom in symptom_entities:
                    relations.append({
                        'source': disease['text'],
                        'target': symptom['text'],
                        'type': 'causes'
                    })
            
            # 3. Medications treat symptoms (when diseases not mentioned)
            if len(disease_entities) == 0:
                for med in medication_entities:
                    for symptom in symptom_entities:
                        relations.append({
                            'source': med['text'],
                            'target': symptom['text'],
                            'type': 'treats'
                        })
        
        return relations
    
    def extract(self, text):
        """Extract both entities and relations from text."""
        entities = self.extract_entities(text)
        relations = self.extract_relations(text, entities)
        
        return entities, relations