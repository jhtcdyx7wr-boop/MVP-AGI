import json
import sys

def score_probe(model_output, expected_output, probe_id):
    # Simple isomorphism check: structure and key science terms match
    model_json = json.loads(model_output)
    expected_json = json.loads(expected_output)
    
    # Check structure (keys match)
    if set(model_json.keys()) != set(expected_json.keys()):
        return 0
    
    # Check science convergence (key phrases match 100%)
    science_terms = ['energy conservation', 'zero tension', 'leak-proof slope']  # Probe-specific
    model_terms = ' '.join(model_json['explanation'].lower().split())
    match_score = sum(1 for term in science_terms if term in model_terms) / len(science_terms)
    
    return 100 if match_score == 1 else 0

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python score.py --model [name] --probe [id]")
        sys.exit(1)
    
    model_name = sys.argv[2]
    probe_id = int(sys.argv[4])
    
    # Load expected output (from expected_outputs.json)
    with open('expected_outputs.json', 'r') as f:
        expected = json.load(f)[str(probe_id)]
    
    # Assume model_output is piped in or from file
    model_output = sys.stdin.read()
    
    score = score_probe(model_output, json.dumps(expected), probe_id)
    print(f"Model: {model_name}, Probe {probe_id}: {score}% Convergence")
