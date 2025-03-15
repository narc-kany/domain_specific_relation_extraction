"""
Integration tests for the web application.
This script tests the Flask API endpoints with sample data.
"""
import json
import requests
import time
import sys
import os
import subprocess
import threading

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Constants
APP_URL = "http://127.0.0.1:5000"
EXTRACT_ENDPOINT = f"{APP_URL}/extract"

def load_samples(domain):
    """Load sample data for testing."""
    try:
        with open(f"data/{domain}/samples.json", 'r') as f:
            return json.load(f)["samples"]
    except Exception as e:
        print(f"Error loading {domain} samples: {e}")
        return []

def run_flask_app():
    """Run the Flask app in a separate process."""
    try:
        # Get the path to the app.py file
        app_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app.py')
        process = subprocess.Popen([sys.executable, app_path])
        return process
    except Exception as e:
        print(f"Error starting Flask app: {e}")
        return None

def wait_for_server(url, max_retries=10, retry_delay=1):
    """Wait for the server to start."""
    print("Waiting for server to start...")
    for i in range(max_retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("Server is up and running!")
                return True
        except requests.exceptions.ConnectionError:
            pass
        
        time.sleep(retry_delay)
        print(f"Retrying... ({i+1}/{max_retries})")
    
    print("Failed to connect to server")
    return False

def test_extract_endpoint(domain, samples):
    """Test the extract endpoint with sample data."""
    results = []
    
    for sample in samples:
        sample_id = sample["id"]
        text = sample["text"]
        expected_entities = sample.get("expected_entities", [])
        expected_relations = sample.get("expected_relations", [])
        
        print(f"\nTesting sample {sample_id}...")
        
        # Prepare request data
        data = {
            "text": text,
            "domain": domain
        }
        
        try:
            # Send request to the API
            response = requests.post(EXTRACT_ENDPOINT, data=data)
            
            if response.status_code != 200:
                print(f"Error: {response.status_code}")
                continue
            
            # Parse response
            result = response.json()
            
            if "error" in result:
                print(f"API Error: {result['error']}")
                continue
            
            entities = result.get("entities", [])
            relations = result.get("relations", [])
            
            # Display results
            print(f"Found {len(entities)} entities and {len(relations)} relations")
            
            # Compare with expected results
            entity_match = len(entities) == len(expected_entities)
            relation_match = len(relations) == len(expected_relations)
            
            # Add to results
            results.append({
                "Sample ID": sample_id,
                "Domain": domain,
                "Entities Found": len(entities),
                "Entities Expected": len(expected_entities),
                "Entities Match": "✓" if entity_match else "✗",
                "Relations Found": len(relations),
                "Relations Expected": len(expected_relations),
                "Relations Match": "✓" if relation_match else "✗"
            })
            
        except Exception as e:
            print(f"Error during API call: {e}")
    
    return results

def display_results(results):
    """Display test results in a table."""
    if not results:
        print("No results to display")
        return
    
    print("\n" + "=" * 80)
    print("API INTEGRATION TEST RESULTS")
    print("=" * 80 + "\n")
    
    try:
        from tabulate import tabulate
        print(tabulate(results, headers="keys", tablefmt="grid"))
    except ImportError:
        # Fallback if tabulate is not installed
        for r in results:
            print(f"Sample: {r['Sample ID']} ({r['Domain']})")
            print(f"  Entities: {r['Entities Found']}/{r['Entities Expected']} {r['Entities Match']}")
            print(f"  Relations: {r['Relations Found']}/{r['Relations Expected']} {r['Relations Match']}")
    
    # Count successes
    entity_successes = sum(1 for r in results if r["Entities Match"] == "✓")
    relation_successes = sum(1 for r in results if r["Relations Match"] == "✓")
    total_tests = len(results)
    
    print(f"\nEntity Success Rate: {entity_successes}/{total_tests} ({entity_successes/total_tests:.0%})")
    print(f"Relation Success Rate: {relation_successes}/{total_tests} ({relation_successes/total_tests:.0%})")
    print(f"Overall Success: {(entity_successes + relation_successes)/(total_tests*2):.0%}")

def main():
    """Run integration tests."""
    # Start the Flask app
    flask_process = run_flask_app()
    
    if not flask_process:
        print("Failed to start Flask app")
        return
    
    try:
        # Wait for server to start
        if not wait_for_server(APP_URL):
            return
        
        # Load test samples
        healthcare_samples = load_samples("healthcare")
        finance_samples = load_samples("finance")
        
        print(f"Loaded {len(healthcare_samples)} healthcare samples and {len(finance_samples)} finance samples")
        
        # Run healthcare tests
        print("\n" + "=" * 80)
        print("TESTING HEALTHCARE DOMAIN")
        print("=" * 80)
        healthcare_results = test_extract_endpoint("healthcare", healthcare_samples)
        
        # Run finance tests
        print("\n" + "=" * 80)
        print("TESTING FINANCE DOMAIN")
        print("=" * 80)
        finance_results = test_extract_endpoint("finance", finance_samples)
        
        # Combine and display results
        all_results = healthcare_results + finance_results
        display_results(all_results)
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    finally:
        # Terminate the Flask app
        if flask_process:
            flask_process.terminate()
            print("\nFlask app terminated")

if __name__ == "__main__":
    main()