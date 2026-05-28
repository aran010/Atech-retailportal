import re

with open("app.py", "r") as f:
    content = f.read()

# 1. Add Number of Partners before form
target_1 = """    st.markdown(
        '<div class="section-title">Client Details</div>', unsafe_allow_html=True
    )

    with st.form("document_form", clear_on_submit=False):"""

replacement_1 = """    st.markdown(
        '<div class="section-title">Client Details</div>', unsafe_allow_html=True
    )

    if doc_type == "new_file_partner":
        # Streamlit doesn't allow dynamic form fields to rerender without submit inside form,
        # so we place the control outside the form.
        st.number_input("Number of Partners (Press Enter to update form)", min_value=1, value=1, step=1, key="num_partners")

    with st.form("document_form", clear_on_submit=False):"""
content = content.replace(target_1, replacement_1)

# 2. Update Proprietor & Firm rendering
target_2 = """        # ── Proprietor & Firm ───────────────────────────────────
        with st.expander("Proprietor and Firm Details", expanded=True):
            col_a, col_b = st.columns(2)

            with col_a:
                prop_name = st.text_input(
                    "Proprietor Name :red[*]"
                )
                c_rel, c_father = st.columns(2)
                with c_rel:
                    prop_relation = st.selectbox(
                        "Relation", options=["S/o", "D/o", "W/o"], index=0,
                        key="prop_relation",
                    )
                with c_father:
                    prop_father_name = st.text_input(
                        "Father / Relative"
                    )
                prop_address = st.text_area(
                    "Proprietor Address :red[*]", height=80,
                )
                prop_phone = st.text_input(
                    "Phone", max_chars=10
                )

            with col_b:
                firm_name = st.text_input(
                    "Firm Name :red[*]",
                )
                firm_address = st.text_area(
                    "Firm / Shop Address :red[*]", height=80,
                )"""

replacement_2 = """        # ── Proprietor / Partner & Firm ───────────────────────────────────
        if doc_type == "new_file_partner":
            with st.expander("Partners and Firm Details", expanded=True):
                firm_name = st.text_input("Firm Name :red[*]")
                firm_address = st.text_area("Firm / Shop Address :red[*]", height=80)
                st.markdown("---")
                
                partners_data = []
                num_partners = st.session_state.get("num_partners", 1)
                for i in range(num_partners):
                    st.markdown(f"**Partner {i+1}**")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        p_name = st.text_input("Partner Name :red[*]", key=f"p_name_{i}")
                        c_rel, c_father = st.columns(2)
                        with c_rel:
                            p_rel = st.selectbox("Relation", options=["S/o", "D/o", "W/o"], index=0, key=f"p_rel_{i}")
                        with c_father:
                            p_father = st.text_input("Father / Relative", key=f"p_father_{i}")
                    with col_b:
                        p_address = st.text_area("Partner Address :red[*]", height=80, key=f"p_address_{i}")
                        p_phone = st.text_input("Phone", max_chars=10, key=f"p_phone_{i}")
                    
                    partners_data.append({
                        "name": p_name.strip(),
                        "relation": p_rel,
                        "father_name": p_father.strip(),
                        "address": p_address.strip(),
                        "phone": p_phone.strip()
                    })
                    st.markdown("---")
        else:
            with st.expander("Proprietor and Firm Details", expanded=True):
                col_a, col_b = st.columns(2)

                with col_a:
                    prop_name = st.text_input("Proprietor Name :red[*]")
                    c_rel, c_father = st.columns(2)
                    with c_rel:
                        prop_relation = st.selectbox("Relation", options=["S/o", "D/o", "W/o"], index=0, key="prop_relation")
                    with c_father:
                        prop_father_name = st.text_input("Father / Relative")
                    prop_address = st.text_area("Proprietor Address :red[*]", height=80)
                    prop_phone = st.text_input("Phone", max_chars=10)

                with col_b:
                    firm_name = st.text_input("Firm Name :red[*]")
                    firm_address = st.text_area("Firm / Shop Address :red[*]", height=80)"""
content = content.replace(target_2, replacement_2)

# 3. Update Submission Context
target_3 = """            "prop_name": prop_name.strip(),
            "prop_relation": prop_relation.strip(),
            "prop_father_name": prop_father_name.strip(),
            "prop_address": prop_address.strip(),
            "prop_phone": prop_phone.strip(),"""

replacement_3 = """            "prop_name": prop_name.strip() if doc_type != "new_file_partner" else "",
            "prop_relation": prop_relation.strip() if doc_type != "new_file_partner" else "",
            "prop_father_name": prop_father_name.strip() if doc_type != "new_file_partner" else "",
            "prop_address": prop_address.strip() if doc_type != "new_file_partner" else "",
            "prop_phone": prop_phone.strip() if doc_type != "new_file_partner" else "",
            "partners": partners_data if doc_type == "new_file_partner" else [],"""
content = content.replace(target_3, replacement_3)

with open("app.py", "w") as f:
    f.write(content)
