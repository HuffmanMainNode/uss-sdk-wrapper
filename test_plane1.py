import os
import json
import sys

# Ensure the current directory is in the path to find the .so file
sys.path.append(os.path.dirname(__file__))
import local_molecularization_engine

def test_molecularizer():
    raw_data = "Sovereign-Test-Data-Denver-CO"
    
    # Generate a random 16-byte session seed (represented as hex string)
    session_seed = os.urandom(16).hex()
    
    print(f"--- INIT PLANE 1: LOCAL MOLECULARIZATION ENGINE ---")
    print(f"Raw Data (Target): {raw_data}")
    print(f"Session Seed (Local): {session_seed}\n")
    
    try:
        # Pass data to the Rust shredder
        result_json = local_molecularization_engine.edge_molecularizer(raw_data, session_seed)
        
        # Parse and print the Jibberlink structure
        parsed_result = json.loads(result_json)
        print("--- JIBBERLINK PACKETS (OUTPUT) ---")
        print(json.dumps(parsed_result, indent=2))
        print("\n[SYSTEM] SUCCESS: Data shredded, encrypted (AES-GCM), and packetized.")
    except Exception as e:
        print(f"[SYSTEM] ERROR during processing: {e}")

if __name__ == "__main__":
    test_molecularizer()
