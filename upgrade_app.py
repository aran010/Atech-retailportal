import re

with open("app.py", "r") as f:
    content = f.read()

# 1. Update Applicant Label
content = content.replace('prop_name = st.text_input("Proprietor Name :red[*]")',
                          'applicant_label = "Director / Auth Signatory Name" if entity_val == "Director" else "Proprietor Name"\n                    prop_name = st.text_input(f"{applicant_label} :red[*]")')

# 2. Add Auth Signatory and Directors List
directors_ui = """
        # ── Directors and Auth Signatory ──
        auth_signatory = False
        directors_data = []
        if entity_val == "Director":
            st.markdown("---")
            auth_signatory = st.checkbox("Is the Applicant an Authorized Signatory?", value=False)
            st.markdown("### Other Directors Details")
            num_directors = st.number_input("Number of OTHER Directors", min_value=0, max_value=20, value=1)
            for i in range(num_directors):
                with st.expander(f"Other Director {i+1}", expanded=False):
                    c1, c2 = st.columns(2)
                    with c1:
                        d_name = st.text_input("Name", key=f"d_name_{i}")
                        d_rel = st.selectbox("Relation", ["S/o", "D/o", "W/o"], key=f"d_rel_{i}")
                    with c2:
                        d_father = st.text_input("Father/Relative Name", key=f"d_father_{i}")
                        d_address = st.text_area("Address", height=80, key=f"d_addr_{i}")
                    if d_name:
                        directors_data.append({
                            "name": d_name.strip(),
                            "relation": d_rel,
                            "father_name": d_father.strip(),
                            "address": d_address.strip()
                        })
        st.markdown("---")
"""
content = re.sub(r'(\s*# ── Registered Pharmacist ───────────────)', directors_ui + r'\1', content)

# 3. Add to context
context_update = """"auth_signatory": auth_signatory,
            "directors_data": directors_data,
            "entity_val": entity_val,"""
content = content.replace('"property_ownership": property_ownership,', f'"property_ownership": property_ownership,\n            {context_update}')

# 4. Modify generate_documents
gen_doc_pattern = r"""(        for tpl_name in template_files:
            if context\.get\("property_ownership"\) == "Owned" and "Rent Agreement" in tpl_name:
                continue)(.*?)(\s*tpl = DocxTemplate\(tpl_path\)\s*tpl\.render\(bold_context\)\s*doc_buffer = io\.BytesIO\(\)\s*tpl\.save\(doc_buffer\)\s*doc_buffer\.seek\(0\)\s*out_name = f"Filled_\{tpl_name\}"\s*zf\.writestr\(out_name, doc_buffer\.read\(\)\))"""

gen_replacement = r"""\1

            # Exclude irrelevant applicant affidavits
            is_prop = context.get("entity_val", "Proprietor") in ["Proprietor", "Partner"]
            is_dir = context.get("entity_val") == "Director" and not context.get("auth_signatory")
            is_auth = context.get("entity_val") == "Director" and context.get("auth_signatory")

            if tpl_name == "AFFIDAVIT (prop).docx" and not is_prop:
                continue
            if tpl_name == "AFFIDAVIT (Director).docx" and not is_dir:
                continue
            if tpl_name == "AFFIDAVIT (Auth Signatory).docx" and not is_auth:
                continue

            tpl_path = os.path.join(template_dir, tpl_name)

            if tpl_name == "AFFIDAVIT(Regd. Pharmacist).docx":
                # Render one for each pharmacist
                ph_data_list = context.get("pharmacists_data", [])
                bold_ph_list = bold_context.get("pharmacists_data", [])
                for idx, ph in enumerate(ph_data_list):
                    ctx_copy = dict(bold_context)
                    # Inject current pharmacist fields to the top-level rp_ variables
                    if idx < len(bold_ph_list):
                        ph_b = bold_ph_list[idx]
                        for k, v in ph_b.items():
                            ctx_copy[f"rp_{k}"] = v
                    
                    tpl = DocxTemplate(tpl_path)
                    tpl.render(ctx_copy)
                    doc_buffer = io.BytesIO()
                    tpl.save(doc_buffer)
                    doc_buffer.seek(0)
                    
                    # Sanitize pharmacist name for filename
                    safe_rp = "".join(c for c in ph["name"] if c.isalnum() or c in (" ", "-", "_")).strip()
                    if not safe_rp:
                        safe_rp = f"Pharmacist_{idx+1}"
                    out_name = f"Filled_AFFIDAVIT(Regd. Pharmacist) {safe_rp}.docx"
                    zf.writestr(out_name, doc_buffer.read())
                continue
\3"""

content = re.sub(gen_doc_pattern, gen_replacement, content, flags=re.DOTALL)

with open("app.py", "w") as f:
    f.write(content)
