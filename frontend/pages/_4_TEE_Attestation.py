import os

import streamlit as st


def show():
    st.markdown("## TEE attestation (demo)")
    st.caption(
        "Static demo: left side is what a defender sees inside a trusted enclave; "
        "right side is what a root attacker still cannot read."
    )

    st.markdown("### Side‑by‑side story")
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("##### Defender (inside enclave)")
        st.success("Enclave running")
        st.success("Memory encryption on")
        st.markdown("Structured honeypot state (what you *intend* to expose):")
        st.json(
            {
                "honeypot_id": "hp_01",
                "status": "isolated",
                "secret": "admin:FakePass2024!",
            }
        )

    with col2:
        st.markdown("##### Attacker (root on host)")
        st.error("Cannot read enclave memory — only ciphertext / noise.")
        st.code(os.urandom(128).hex(), language="text")
        st.caption("What you see here is not the real secret; it is encrypted or random-looking bytes.")

    st.divider()
    st.markdown("##### Simulated hardware quote (for judges)")
    st.json(
        {
            "quote": "SGX_QUOTE_SIMULATED",
            "mr_enclave": os.urandom(32).hex(),
            "attributes": "DEBUG=OFF, MODE=64BIT",
        }
    )
