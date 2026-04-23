import os
import sys
import json

# Ensure the current directory is in the path to find the .so file
sys.path.append(os.path.dirname(__file__))
import local_molecularization_engine

def verify_integration():
    raw_data = "Verification-Test-Payload"
    session_seed = os.urandom(16).hex()

    print("--- VERIFYING RUST INTEGRATION ---")
    print(f"Target Data: {raw_data}")
    print(f"Session Seed: {session_seed}\n")

    try:
        # Pass data to the Rust shredder
        result_json = local_molecularization_engine.edge_molecularizer(raw_data, session_seed)
        
        # Parse and print the Jibberlink structure
        parsed_result = json.loads(result_json)
        print("--- JIBBERLINK PACKETS ---")
        print(json.dumps(parsed_result, indent=2))
        print("\n[SYSTEM] SUCCESS: Rust library imported and executed correctly.")
    except Exception as e:
        print(f"[SYSTEM] ERROR: {e}")

if __name__ == "__main__":
    verify_integration()
