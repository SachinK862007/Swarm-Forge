import streamlit as st
from supabase import create_client

# --- REPLACE WITH YOUR REAL CREDENTIALS (Supabase project URL + anon key) ---
SUPABASE_URL = "REPLACE_WITH_YOUR_SUPABASE_URL"
SUPABASE_KEY = "REPLACE_WITH_YOUR_SUPABASE_ANON_KEY"
# -----------------------------------------------------------------------------


def _client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def show():
    st.markdown("## Community templates")
    st.caption(
        "Share JSON deception snippets tagged with a MITRE technique. "
        "Requires a `templates` table in Supabase (name, technique, content, rating)."
    )

    tab1, tab2 = st.tabs(["Submit a template", "Browse library"])

    with tab1:
        st.markdown("##### What to submit")
        st.markdown(
            "- **Name** — short label jurors can read.\n"
            "- **MITRE** — pick the closest technique ID.\n"
            "- **JSON** — valid JSON describing the deception (service, ports, banners, etc.)."
        )
        with st.form("template_form", clear_on_submit=True):
            name = st.text_input("Template name", placeholder="e.g. Fake Jenkins 2.401")
            technique = st.selectbox(
                "MITRE technique",
                ["T1595", "T1110", "T1190", "T1001"],
                help="T1595 Active Scanning · T1110 Brute Force · T1190 Exploit Public-Facing · T1001 Data Obfuscation",
            )
            content = st.text_area(
                "Content (JSON)",
                height=160,
                placeholder='{\n  "service": "nginx",\n  "banner": "nginx/1.23"\n}',
            )
            submitted = st.form_submit_button("Submit", type="primary")
            if submitted:
                if not name.strip():
                    st.error("Please enter a template name.")
                else:
                    try:
                        supabase = _client()
                        supabase.table("templates").insert(
                            {
                                "name": name.strip(),
                                "technique": technique,
                                "content": content or "{}",
                                "rating": 0,
                            }
                        ).execute()
                        st.success("Saved. Open **Browse library** to see it.")
                    except Exception as e:
                        st.error(f"Could not submit: {e}")

    with tab2:
        try:
            supabase = _client()
            data = supabase.table("templates").select("*").execute()
        except Exception as e:
            st.error(f"Could not load templates: {e}")
            return

        if not data.data:
            st.info("No templates yet — add one in the **Submit** tab.")
            return

        st.markdown(f"##### {len(data.data)} template(s)")
        for t in data.data:
            title = t.get("name", "Untitled")
            tech = t.get("technique", "—")
            rating = t.get("rating", 0)
            st.markdown(f"**{title}** · `{tech}` · rating **{rating}**")
            st.code(t.get("content", ""), language="json")
            st.divider()
