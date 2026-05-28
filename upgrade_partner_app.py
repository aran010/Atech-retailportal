import re

with open("app.py", "r") as f:
    content = f.read()

# 1. Update boldify_context
boldify_pattern = r'(def boldify_context\(ctx\):\s*bolded = \{\}\s*)(for k, v in ctx\.items\(\):)'
boldify_replace = r'\1skip_keys = {"entity_val", "property_ownership", "auth_signatory"}\n    for k, v in ctx.items():\n        if k in skip_keys:\n            bolded[k] = v\n        el'
content = re.sub(boldify_pattern, boldify_replace, content)

# 2. Add Partners UI Block
partner_ui = """        # ── Partners ──
        partners_data = []
        partnership_start_date = ""
        if entity_val == "Partner":
            st.markdown("---")
            st.markdown("### Partnership Details")
            partnership_start_date = st.text_input("Partnership Start Date (e.g. 20-02-2026)")
            num_partners = st.number_input("Number of OTHER Partners", min_value=0, max_value=20, value=1)
            for i in range(num_partners):
                with st.expander(f"Other Partner {i+1}", expanded=False):
                    c1, c2 = st.columns(2)
                    with c1:
                        p_name = st.text_input("Name", key=f"p_name_{i}")
                        p_rel = st.selectbox("Relation", ["S/o", "D/o", "W/o"], key=f"p_rel_{i}")
                    with c2:
                        p_father = st.text_input("Father/Relative Name", key=f"p_father_{i}")
                        p_address = st.text_area("Address", height=80, key=f"p_addr_{i}")
                    if p_name:
                        partners_data.append({
                            "name": p_name.strip(),
                            "relation": p_rel,
                            "father_name": p_father.strip(),
                            "address": p_address.strip()
                        })
"""
content = content.replace('st.markdown("---")\n        # ── Registered Pharmacist', partner_ui + '\n        st.markdown("---")\n        # ── Registered Pharmacist')

# 3. Add to context
context_update = """"partners_data": partners_data,
            "partnership_start_date": partnership_start_date,"""
content = content.replace('"directors_data": directors_data,', f'"directors_data": directors_data,\n            {context_update}')

# 4. Modify generate_documents filtering logic
filter_pattern = r'(            # Exclude irrelevant applicant affidavits\s*)is_prop = context\.get\("entity_val", "Proprietor"\) in \["Proprietor", "Partner"\](.*?)(            if tpl_name == "AFFIDAVIT \(prop\)\.docx" and not is_prop:\s*continue\s*if tpl_name == "AFFIDAVIT \(Director\)\.docx" and not is_dir:\s*continue\s*if tpl_name == "AFFIDAVIT \(Auth Signatory\)\.docx" and not is_auth:\s*continue)'
filter_replace = r"""\1is_prop = context.get("entity_val", "Proprietor") == "Proprietor"
            is_partner = context.get("entity_val") == "Partner"\2            if tpl_name == "AFFIDAVIT (prop).docx" and not is_prop:
                continue
            if tpl_name == "AFFIDAVIT (Partner).docx" and not is_partner:
                continue
            if tpl_name == "Partner WORKING REPORT.docx" and not is_partner:
                continue
            if tpl_name == "Partnership Deed.docx" and not is_partner:
                continue
            if tpl_name == "PROP WORKING REPORT.docx" and not is_prop:
                continue
            if tpl_name == "AFFIDAVIT (Director).docx" and not is_dir:
                continue
            if tpl_name == "AFFIDAVIT (Auth Signatory).docx" and not is_auth:
                continue"""
content = re.sub(filter_pattern, filter_replace, content, flags=re.DOTALL)

with open("app.py", "w") as f:
    f.write(content)
