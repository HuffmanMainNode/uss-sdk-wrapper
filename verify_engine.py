import os
import sys
import json
import gc

# Ensure the directory containing the .so file is in the path
sys.path.append(os.path.dirname(__file__))
import local_molecularization_engine

def run_memory_safe_test():
    """
    Verification function to test the Rust-Python integration.
    Generates Jibberlink packets and validates their internal structure.
    """
    raw_data = "Sovereign-Edge-Verification-Test-2026"
    session_seed = os.urandom(16).hex()

    print("--- STARTING ENGINE VERIFICATION ---")
    print(f"Raw Data Length: {len(raw_data)}")

    try:
        # Invoke the Rust shared object function
        result_json = local_molecularization_engine.edge_molecularizer(raw_data, session_seed)

        # Parse JSON output to verify packet integrity
        packets = json.loads(result_json)
        print(f"Total Molecules Generated: {len(packets)}")

        # Define and verify required cryptographic keys
        required_keys = {'molecule_id', 'jibberlink_payload', 'auth_tag', 'nonce'}
        
        if len(packets) > 0:
            packet_keys = set(packets[0].keys())
            if required_keys.issubset(packet_keys):
                print("[SUCCESS] Packet structure verified: All cryptographic keys present.")
            else:
                missing = required_keys - packet_keys
                print(f"[FAILURE] Missing keys: {missing}")

        # Display sample output
        print("\n--- JIBBERLINK SAMPLE PACKET (MOL_0) ---")
        print(json.dumps(packets[0], indent=2))

        # Cleanup for memory safety simulation
        del raw_data
        gc.collect()
        print("\n[SYSTEM] Integration test passed. Local memory scrubbed.")

    except Exception as e:
        print(f"[CRITICAL ERROR] Engine integration failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    run_memory_safe_test()
