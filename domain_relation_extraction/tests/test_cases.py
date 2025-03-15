import json
import sys
import os

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now use absolute imports
from models.healthcare_model import HealthcareModel
from models.finance_model import FinanceModel

def run_test_case(model, text, expected_entities=None, expected_relations=None):
    """Run a test case and check results against expected output."""
    print(f"\nTesting with text: '{text}'")
    
    # Extract entities and relations
    entities, relations = model.extract(text)
    
    # Print results
    print(f"Found {len(entities)} entities:")
    for entity in entities:
        print(f"  - {entity['text']} ({entity['type']})")
    
    print(f"Found {len(relations)} relations:")
    for relation in relations:
        print(f"  - {relation['source']} {relation['type']} {relation['target']}")
    
    # Check against expected results if provided
    if expected_entities is not None:
        # Check if expected_entities is an integer (count) or a list (detailed comparison)
        if isinstance(expected_entities, int):
            # Just compare counts
            entity_success = len(entities) == expected_entities
            if entity_success:
                print(f"✓ Entity count matches expected ({expected_entities})")
            else:
                print(f"✗ Entity count mismatch: got {len(entities)}, expected {expected_entities}")
        else:
            # Detailed comparison (not implemented here)
            print(f"Detailed entity comparison not implemented yet")
    
    if expected_relations is not None:
        # Check if expected_relations is an integer (count) or a list (detailed comparison)
        if isinstance(expected_relations, int):
            # Just compare counts
            relation_success = len(relations) == expected_relations
            if relation_success:
                print(f"✓ Relation count matches expected ({expected_relations})")
            else:
                print(f"✗ Relation count mismatch: got {len(relations)}, expected {expected_relations}")
        else:
            # Detailed comparison (not implemented here)
            print(f"Detailed relation comparison not implemented yet")
    
    print("-" * 50)
    return entities, relations

def test_healthcare():
    """Test the healthcare model with various test cases."""
    print("\n=== HEALTHCARE MODEL TESTS ===\n")
    
    model = HealthcareModel()
    
    # Test case 1: Simple sentence with clear relation
    test1 = "Aspirin treats headache and reduces inflammation."
    run_test_case(model, test1, expected_entities=2, expected_relations=1)
    
    # Test case 2: Multiple relations
    test2 = "Diabetes causes fatigue and excessive thirst. Insulin treats diabetes."
    run_test_case(model, test2, expected_entities=3, expected_relations=2)
    
    # Test case 3: More complex paragraph
    test3 = """
    Patients with hypertension often experience headaches and dizziness.
    Lisinopril is commonly prescribed to treat hypertension.
    Regular exercise and a healthy diet can help prevent hypertension.
    A biopsy is performed to diagnose cancer, which can cause pain and fatigue.
    """
    run_test_case(model, test3)
    
    # Test case 4: Edge case with nested relations
    test4 = "Alzheimer's disease, which causes memory loss, can be treated with therapy that prevents rapid progression."
    run_test_case(model, test4)
    
    # Test case 5: Case with negation (challenging for rule-based systems)
    test5 = "While aspirin does not treat cancer, it may help with pain management."
    run_test_case(model, test5)

def test_finance():
    """Test the finance model with various test cases."""
    print("\n=== FINANCE MODEL TESTS ===\n")
    
    model = FinanceModel()
    
    # Test case 1: Simple sentence with clear relation
    test1 = "Apple launched iPhone in 2007 which increased their revenue."
    run_test_case(model, test1, expected_entities=3, expected_relations=2)
    
    # Test case 2: Multiple relations
    test2 = "Amazon acquired Whole Foods in 2017. This acquisition increased their market share in the grocery sector."
    run_test_case(model, test2, expected_entities=4, expected_relations=2)
    
    # Test case 3: More complex paragraph
    test3 = """
    Microsoft's cloud business has shown significant growth this quarter.
    The company announced a 15% increase in revenue, while their competitors 
    experienced a market share decrease. Google launched a new AI product
    that analysts believe will strengthen their position in the market.
    """
    run_test_case(model, test3)
    
    # Test case 4: Edge case with financial metrics
    test4 = "Tesla's stock price decreased after they announced layoffs, but their revenue increased due to Model S sales."
    run_test_case(model, test4)
    
    # Test case 5: Case with complex relation structure
    test5 = "Bank of America reported that Goldman Sachs plans to invest in fintech startups that have recently launched new loan products."
    run_test_case(model, test5)

def save_test_examples():
    """Save test examples to JSON files for future testing and documentation."""
    healthcare_examples = [
        {
            "text": "Aspirin treats headache and reduces inflammation.",
            "domain": "healthcare"
        },
        {
            "text": "Diabetes causes fatigue and excessive thirst. Insulin treats diabetes.",
            "domain": "healthcare"
        },
        {
            "text": """Patients with hypertension often experience headaches and dizziness.
                    Lisinopril is commonly prescribed to treat hypertension.
                    Regular exercise and a healthy diet can help prevent hypertension.
                    A biopsy is performed to diagnose cancer, which can cause pain and fatigue.""",
            "domain": "healthcare"
        }
    ]
    
    finance_examples = [
        {
            "text": "Apple launched iPhone in 2007 which increased their revenue.",
            "domain": "finance"
        },
        {
            "text": "Amazon acquired Whole Foods in 2017. This acquisition increased their market share in the grocery sector.",
            "domain": "finance"
        },
        {
            "text": """Microsoft's cloud business has shown significant growth this quarter.
                    The company announced a 15% increase in revenue, while their competitors 
                    experienced a market share decrease. Google launched a new AI product
                    that analysts believe will strengthen their position in the market.""",
            "domain": "finance"
        }
    ]
    
    # Ensure directories exist
    import os
    os.makedirs('data/healthcare', exist_ok=True)
    os.makedirs('data/finance', exist_ok=True)
    
    # Save to files
    with open('data/healthcare/test_examples.json', 'w') as f:
        json.dump(healthcare_examples, f, indent=2)
    
    with open('data/finance/test_examples.json', 'w') as f:
        json.dump(finance_examples, f, indent=2)
    
    print("Saved test examples to JSON files in data/healthcare and data/finance directories.")

if __name__ == "__main__":
    # Run healthcare tests
    test_healthcare()
    
    # Run finance tests
    test_finance()
    
    # Save test examples for future use
    save_test_examples()