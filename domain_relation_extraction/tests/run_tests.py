"""
Run evaluation tests for the domain-specific relation extraction system.
"""
import json
import sys
import os

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.healthcare_model import HealthcareModel
from models.finance_model import FinanceModel
from tests.expected_outputs import HEALTHCARE_EXPECTED, FINANCE_EXPECTED, evaluate_test_results

def format_metrics(metrics):
    """Format metrics for display."""
    return {
        "Recall": f"{metrics['recall']:.2f}",
        "Precision": f"{metrics['precision']:.2f}",
        "F1 Score": f"{metrics['f1']:.2f}",
        "Type Accuracy": f"{metrics['type_accuracy']:.2f}"
    }

def run_healthcare_tests():
    """Run tests on the healthcare model."""
    print("=" * 80)
    print("HEALTHCARE MODEL EVALUATION")
    print("=" * 80)
    
    model = HealthcareModel()
    results = {}
    
    # Run tests and evaluate
    for test_name, test_data in HEALTHCARE_EXPECTED.items():
        print(f"\nRunning test: {test_name}")
        print(f"Text: {test_data['text']}")
        
        entities, relations = model.extract(test_data['text'])
        evaluation = evaluate_test_results(entities, relations, HEALTHCARE_EXPECTED, test_name)
        
        # Store results
        results[test_name] = evaluation
        
        # Display entity results
        entity_metrics = evaluation["entity_metrics"]
        print(f"\nEntity Results:")
        print(f"Found {entity_metrics['extracted']} entities, expected {entity_metrics['expected']}")
        print(f"Correctly identified: {entity_metrics['correctly_identified']}")
        print(f"Correctly typed: {entity_metrics['correctly_typed']}")
        
        # Display relation results
        relation_metrics = evaluation["relation_metrics"]
        print(f"\nRelation Results:")
        print(f"Found {relation_metrics['extracted']} relations, expected {relation_metrics['expected']}")
        print(f"Correctly identified: {relation_metrics['correctly_identified']}")
        print(f"Correctly typed: {relation_metrics['correctly_typed']}")
        
        print("-" * 80)
    
    # Create summary table
    entity_summary = []
    relation_summary = []
    
    for test_name, eval_results in results.items():
        entity_metrics = format_metrics(eval_results["entity_metrics"])
        entity_metrics["Test"] = test_name
        entity_summary.append(entity_metrics)
        
        relation_metrics = format_metrics(eval_results["relation_metrics"])
        relation_metrics["Test"] = test_name
        relation_summary.append(relation_metrics)
    
    try:
        from tabulate import tabulate
        # Print summary tables
        print("\nEntity Metrics Summary:")
        print(tabulate(entity_summary, headers="keys", tablefmt="grid"))
        
        print("\nRelation Metrics Summary:")
        print(tabulate(relation_summary, headers="keys", tablefmt="grid"))
    except ImportError:
        print("Install tabulate for better formatted tables: pip install tabulate")
        print("\nEntity Metrics Summary:")
        for item in entity_summary:
            print(item)
        
        print("\nRelation Metrics Summary:")
        for item in relation_summary:
            print(item)
    
    # Calculate averages
    avg_entity_recall = sum(float(item["Recall"]) for item in entity_summary) / len(entity_summary)
    avg_entity_precision = sum(float(item["Precision"]) for item in entity_summary) / len(entity_summary)
    avg_entity_f1 = sum(float(item["F1 Score"]) for item in entity_summary) / len(entity_summary)
    
    avg_relation_recall = sum(float(item["Recall"]) for item in relation_summary) / len(relation_summary)
    avg_relation_precision = sum(float(item["Precision"]) for item in relation_summary) / len(relation_summary)
    avg_relation_f1 = sum(float(item["F1 Score"]) for item in relation_summary) / len(relation_summary)
    
    print("\nAverage Metrics:")
    print(f"Entity: Recall={avg_entity_recall:.2f}, Precision={avg_entity_precision:.2f}, F1={avg_entity_f1:.2f}")
    print(f"Relation: Recall={avg_relation_recall:.2f}, Precision={avg_relation_precision:.2f}, F1={avg_relation_f1:.2f}")
    
    return results

def run_finance_tests():
    """Run tests on the finance model."""
    print("\n\n" + "=" * 80)
    print("FINANCE MODEL EVALUATION")
    print("=" * 80)
    
    model = FinanceModel()
    results = {}
    
    # Run tests and evaluate
    for test_name, test_data in FINANCE_EXPECTED.items():
        print(f"\nRunning test: {test_name}")
        print(f"Text: {test_data['text']}")
        
        entities, relations = model.extract(test_data['text'])
        evaluation = evaluate_test_results(entities, relations, FINANCE_EXPECTED, test_name)
        
        # Store results
        results[test_name] = evaluation
        
        # Display entity results
        entity_metrics = evaluation["entity_metrics"]
        print(f"\nEntity Results:")
        print(f"Found {entity_metrics['extracted']} entities, expected {entity_metrics['expected']}")
        print(f"Correctly identified: {entity_metrics['correctly_identified']}")
        print(f"Correctly typed: {entity_metrics['correctly_typed']}")
        
        # Display relation results
        relation_metrics = evaluation["relation_metrics"]
        print(f"\nRelation Results:")
        print(f"Found {relation_metrics['extracted']} relations, expected {relation_metrics['expected']}")
        print(f"Correctly identified: {relation_metrics['correctly_identified']}")
        print(f"Correctly typed: {relation_metrics['correctly_typed']}")
        
        print("-" * 80)
    
    # Create summary table
    entity_summary = []
    relation_summary = []
    
    for test_name, eval_results in results.items():
        entity_metrics = format_metrics(eval_results["entity_metrics"])
        entity_metrics["Test"] = test_name
        entity_summary.append(entity_metrics)
        
        relation_metrics = format_metrics(eval_results["relation_metrics"])
        relation_metrics["Test"] = test_name
        relation_summary.append(relation_metrics)
    
    try:
        from tabulate import tabulate
        # Print summary tables
        print("\nEntity Metrics Summary:")
        print(tabulate(entity_summary, headers="keys", tablefmt="grid"))
        
        print("\nRelation Metrics Summary:")
        print(tabulate(relation_summary, headers="keys", tablefmt="grid"))
    except ImportError:
        print("Install tabulate for better formatted tables: pip install tabulate")
        print("\nEntity Metrics Summary:")
        for item in entity_summary:
            print(item)
        
        print("\nRelation Metrics Summary:")
        for item in relation_summary:
            print(item)
    
    # Calculate averages
    avg_entity_recall = sum(float(item["Recall"]) for item in entity_summary) / len(entity_summary)
    avg_entity_precision = sum(float(item["Precision"]) for item in entity_summary) / len(entity_summary)
    avg_entity_f1 = sum(float(item["F1 Score"]) for item in entity_summary) / len(entity_summary)
    
    avg_relation_recall = sum(float(item["Recall"]) for item in relation_summary) / len(relation_summary)
    avg_relation_precision = sum(float(item["Precision"]) for item in relation_summary) / len(relation_summary)
    avg_relation_f1 = sum(float(item["F1 Score"]) for item in relation_summary) / len(relation_summary)
    
    print("\nAverage Metrics:")
    print(f"Entity: Recall={avg_entity_recall:.2f}, Precision={avg_entity_precision:.2f}, F1={avg_entity_f1:.2f}")
    print(f"Relation: Recall={avg_relation_recall:.2f}, Precision={avg_relation_precision:.2f}, F1={avg_relation_f1:.2f}")
    
    return results

def save_results(healthcare_results, finance_results):
    """Save evaluation results to a file."""
    all_results = {
        "healthcare": healthcare_results,
        "finance": finance_results
    }
    
    with open('evaluation_results.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print("\nResults saved to evaluation_results.json")

if __name__ == "__main__":
    # Run healthcare tests
    healthcare_results = run_healthcare_tests()
    
    # Run finance tests
    finance_results = run_finance_tests()
    
    # Save results
    save_results(healthcare_results, finance_results)