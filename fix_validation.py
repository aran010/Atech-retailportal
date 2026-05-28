import re

with open("app.py", "r") as f:
    content = f.read()

target = """    if submitted:
        # Validate key fields
        required = {
            "Proprietor Name": prop_name,
            "Firm Name": firm_name,
            "Firm Address": firm_address,
            "RP Name": rp_name,
        }
        missing = [k for k, v in required.items() if not v.strip()]

        if missing:
            st.warning(
                "Please fill in the following required fields: "
                f"**{', '.join(missing)}**"
            )
            st.stop()

        # Build context dictionary
        context = {
            # Proprietor
            "prop_name": prop_name.strip(),
            "prop_relation": prop_relation,
            "prop_father_name": prop_father_name.strip(),
            "prop_address": prop_address.strip(),
            "prop_phone": prop_phone.strip(),"""

replacement = """    if submitted:
        # Validate key fields
        required = {
            "Firm Name": firm_name,
            "Firm Address": firm_address,
            "RP Name": rp_name,
        }
        if doc_type != "new_file_partner":
            required["Proprietor Name"] = prop_name
        else:
            if partners_data:
                required["Partner 1 Name"] = partners_data[0]["name"]

        missing = [k for k, v in required.items() if not v.strip()]

        if missing:
            st.warning(
                "Please fill in the following required fields: "
                f"**{', '.join(missing)}**"
            )
            st.stop()

        # Default proprietor values if partner mode
        if doc_type == "new_file_partner":
            prop_name = partners_data[0]["name"] if partners_data else ""
            prop_relation = partners_data[0]["relation"] if partners_data else ""
            prop_father_name = partners_data[0]["father_name"] if partners_data else ""
            prop_address = partners_data[0]["address"] if partners_data else ""
            prop_phone = partners_data[0]["phone"] if partners_data else ""

        # Build context dictionary
        context = {
            # Proprietor (used as fallback or for main proprietor)
            "prop_name": prop_name.strip(),
            "prop_relation": prop_relation,
            "prop_father_name": prop_father_name.strip(),
            "prop_address": prop_address.strip(),
            "prop_phone": prop_phone.strip(),
            "partners": partners_data if doc_type == "new_file_partner" else [],"""

content = content.replace(target, replacement)

with open("app.py", "w") as f:
    f.write(content)
