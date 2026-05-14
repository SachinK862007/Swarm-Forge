import streamlit as st
from supabase import create_client

# ==================== REPLACE THESE ====================
SUPABASE_URL = "https://beorvnttfbczhjfkorcp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."  # your anon key
# =======================================================

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def show():
    st.title("🌐 Community Templates")
    tab1, tab2 = st.tabs(["Submit", "Browse"])

    with tab1:
        with st.form("template_form"):
            name = st.text_input("Template Name")
            technique = st.selectbox("MITRE Technique", ["T1595", "T1110", "T1190", "T1001"])
            content = st.text_area("Content (JSON)", '{"service": "nginx", "version": "1.23"}')
            if st.form_submit_button("Submit"):
                supabase.table("templates").insert({
                    "name": name, "technique": technique, "content": content, "rating": 0
                }).execute()
                st.success("Template submitted!")

    with tab2:
        data = supabase.table("templates").select("*").execute()
        if data.data:
            for t in data.data:
                st.markdown(f"**{t['name']}** — {t['technique']} | ⭐ {t['rating']}")
                st.code(t['content'], language="json")
                st.markdown("---")
        else:
            st.info("No templates yet. Be the first!")