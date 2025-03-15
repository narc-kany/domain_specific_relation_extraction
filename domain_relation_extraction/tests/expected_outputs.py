"""
This module contains expected outputs for test cases to validate 
the domain-specific relation extraction system.
"""
import sys
import os

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Healthcare domain expected outputs
HEALTHCARE_EXPECTED = {
    "test1": {
        "text": "Aspirin treats headache and reduces inflammation.",
        "entities": [
            {"text": "Aspirin", "type": "MEDICATION"},
            {"text": "headache", "type": "SYMPTOM"}
        ],
        "relations": [
            {"source": "Aspirin", "target": "headache", "type": "treats"}
        ]
    },
    "test2": {
        "text": "Diabetes causes fatigue and excessive thirst. Insulin treats diabetes.",
        "entities": [
            {"text": "Diabetes", "type": "DISEASE"},
            {"text": "fatigue", "type": "SYMPTOM"},
            {"text": "Insulin", "type": "MEDICATION"}
        ],
        "relations": [
            {"source": "Diabetes", "target": "fatigue", "type": "causes"},
            {"source": "Insulin", "target": "Diabetes", "type": "treats"}
        ]
    },
    "test3": {
        "text": """Patients with hypertension often experience headaches and dizziness.
                Lisinopril is commonly prescribed to treat hypertension.
                Regular exercise and a healthy diet can help prevent hypertension.
                A biopsy is performed to diagnose cancer, which can cause pain and fatigue.""",
        "entities": [
            {"text": "hypertension", "type": "DISEASE"},
            {"text": "headaches", "type": "SYMPTOM"},
            {"text": "dizziness", "type": "SYMPTOM"},
            {"text": "Lisinopril", "type": "MEDICATION"},
            {"text": "biopsy", "type": "PROCEDURE"},
            {"text": "cancer", "type": "DISEASE"},
            {"text": "pain", "type": "SYMPTOM"},
            {"text": "fatigue", "type": "SYMPTOM"}
        ],
        "relations": [
            {"source": "hypertension", "target": "headaches", "type": "causes"},
            {"source": "hypertension", "target": "dizziness", "type": "causes"},
            {"source": "Lisinopril", "target": "hypertension", "type": "treats"},
            {"source": "cancer", "target": "pain", "type": "causes"},
            {"source": "cancer", "target": "fatigue", "type": "causes"}
        ]
    }
}

# Finance domain expected outputs
FINANCE_EXPECTED = {
    "test1": {
        "text": "Apple launched iPhone in 2007 which increased their revenue.",
        "entities": [
            {"text": "Apple", "type": "COMPANY"},
            {"text": "iPhone", "type": "PRODUCT"},
            {"text": "revenue", "type": "METRIC"}
        ],
        "relations": [
            {"source": "Apple", "target": "iPhone", "type": "launched"},
            {"source": "iPhone", "target": "revenue", "type": "increased"}
        ]
    },
    "test2": {
        "text": "Amazon acquired Whole Foods in 2017. This acquisition increased their market share in the grocery sector.",
        "entities": [
            {"text": "Amazon", "type": "COMPANY"},
            {"text": "Whole Foods", "type": "COMPANY"},
            {"text": "market share", "type": "METRIC"},
            {"text": "acquisition", "type": "EVENT"}
        ],
        "relations": [
            {"source": "Amazon", "target": "Whole Foods", "type": "acquired"},
            {"source": "acquisition", "target": "market share", "type": "increased"}
        ]
    },
    "test3": {
        "text": """Microsoft's cloud business has shown significant growth this quarter.
                The company announced a 15% increase in revenue, while their competitors 
                experienced a market share decrease. Google launched a new AI product
                that analysts believe will strengthen their position in the market.""",
        "entities": [
            {"text": "Microsoft", "type": "COMPANY"},
            {"text": "cloud", "type": "PRODUCT"},
            {"text": "growth", "type": "METRIC"},
            {"text": "revenue", "type": "METRIC"},
            {"text": "market share", "type": "METRIC"},
            {"text": "Google", "type": "COMPANY"},
            {"text": "AI product", "type": "PRODUCT"}
        ],
        "relations": [
            {"source": "cloud", "target": "growth", "type": "increased"},
            {"source": "Microsoft", "target": "revenue", "type": "increased"},
            {"source": "competitors", "target": "market share", "type": "decreased"},
            {"source": "Google", "target": "AI product", "type": "launched"}
        ]
    }
}

def evaluate_test_results(entities, relations, expected, test_name):
    """
    Evaluate test results against expected outputs.
    
    Args:
        entities (list): List of extracted entities
        relations (list): List of extracted relations
        expected (dict): Dictionary of expected outputs
        test_name (str): Name of the test case
        
    Returns:
        dict: Evaluation results
    """
    if test_name not in expected:
        return {"error": f"No expected output defined for test '{test_name}'"}
    
    expected_data = expected[test_name]
    
    # Check entities
    entity_found = 0
    entity_correct_type = 0
    
    for exp_entity in expected_data["entities"]:
        for entity in entities:
            if exp_entity["text"].lower() == entity["text"].lower():
                entity_found += 1
                if exp_entity["type"] == entity["type"]:
                    entity_correct_type += 1
    
    # Check relations
    relation_found = 0
    relation_correct_type = 0
    
    for exp_relation in expected_data["relations"]:
        for relation in relations:
            if (exp_relation["source"].lower() == relation["source"].lower() and
                exp_relation["target"].lower() == relation["target"].lower()):
                relation_found += 1
                if exp_relation["type"] == relation["type"]:
                    relation_correct_type += 1
    
    # Calculate metrics
    total_expected_entities = len(expected_data["entities"])
    total_expected_relations = len(expected_data["relations"])
    
    entity_recall = entity_found / total_expected_entities if total_expected_entities > 0 else 0
    entity_precision = entity_found / len(entities) if len(entities) > 0 else 0
    entity_f1 = 2 * (entity_precision * entity_recall) / (entity_precision + entity_recall) if (entity_precision + entity_recall) > 0 else 0
    
    entity_type_accuracy = entity_correct_type / entity_found if entity_found > 0 else 0
    
    relation_recall = relation_found / total_expected_relations if total_expected_relations > 0 else 0
    relation_precision = relation_found / len(relations) if len(relations) > 0 else 0
    relation_f1 = 2 * (relation_precision * relation_recall) / (relation_precision + relation_recall) if (relation_precision + relation_recall) > 0 else 0
    
    relation_type_accuracy = relation_correct_type / relation_found if relation_found > 0 else 0
    
    # Return evaluation results
    return {
        "entity_metrics": {
            "expected": total_expected_entities,
            "extracted": len(entities),
            "correctly_identified": entity_found,
            "correctly_typed": entity_correct_type,
            "recall": entity_recall,
            "precision": entity_precision,
            "f1": entity_f1,
            "type_accuracy": entity_type_accuracy
        },
        "relation_metrics": {
            "expected": total_expected_relations,
            "extracted": len(relations),
            "correctly_identified": relation_found,
            "correctly_typed": relation_correct_type,
            "recall": relation_recall,
            "precision": relation_precision,
            "f1": relation_f1,
            "type_accuracy": relation_type_accuracy
        }
    }