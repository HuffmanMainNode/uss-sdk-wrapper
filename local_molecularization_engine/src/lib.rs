use pyo3::prelude::*;
use aes_gcm::{
    aead::{Aead, AeadCore, KeyInit, OsRng},
    Aes256Gcm, Nonce
};
use sha2::{Sha256, Digest};
use serde::{Serialize, Deserialize};
use hex;

/// Represents a single shredded and encapsulated Jibberlink packet.
#[derive(Serialize, Deserialize)]
struct JibberlinkPacket {
    molecule_id: String,
    jibberlink_payload: String,
    auth_tag: String,
    nonce: String,
}

/// The Core Shredder and Encapsulator exposed to Python.
#[pyfunction]
fn edge_molecularizer(raw_data: String, session_seed: String) -> PyResult<String> {
    // 1. Derive a 256-bit key from the session seed using SHA-256
    let mut hasher = Sha256::new();
    hasher.update(session_seed.as_bytes());
    let key_bytes = hasher.finalize();
    
    // Initialize AES-GCM cipher
    let cipher = Aes256Gcm::new_from_slice(&key_bytes)
        .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("Invalid key length: {}", e)))?;

    let mut packets = Vec::new();
    let data_bytes = raw_data.as_bytes();

    // 2. The Shredder: Chunk into 8-byte fragments
    for (i, chunk) in data_bytes.chunks(8).enumerate() {
        // Generate a unique 96-bit nonce for this specific chunk
        let nonce_bytes = Aes256Gcm::generate_nonce(&mut OsRng);
        
        // 3. Encapsulate: Apply AES-GCM encryption
        let ciphertext_with_tag = cipher.encrypt(&nonce_bytes, chunk)
            .map_err(|_| pyo3::exceptions::PyRuntimeError::new_err("Encryption failed"))?;

        // In Rust's aes-gcm, the auth tag is appended to the ciphertext (last 16 bytes)
        let tag_start = ciphertext_with_tag.len().saturating_sub(16);
        let payload = &ciphertext_with_tag[..tag_start];
        let auth_tag = &ciphertext_with_tag[tag_start..];

        // 4. The Jibberlink Formatter
        packets.push(JibberlinkPacket {
            molecule_id: format!("mol_{}", i),
            jibberlink_payload: hex::encode(payload),
            auth_tag: hex::encode(auth_tag),
            nonce: hex::encode(nonce_bytes),
        });
    }

    // Absolute memory safety: Ownership rules mean `raw_data` is explicitly dropped here
    // ensuring no raw PII lingers in the current scope context.
    drop(raw_data);

    // Serialize the packets into a JSON string for Python
    let json_output = serde_json::to_string(&packets)
        .map_err(|_| pyo3::exceptions::PyRuntimeError::new_err("JSON serialization failed"))?;

    Ok(json_output)
}

/// A Python module implemented in Rust.
#[pymodule]
fn local_molecularization_engine(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(edge_molecularizer, m)?)?;
    Ok(())
}
