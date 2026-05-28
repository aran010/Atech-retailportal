import re

with open("app.py", "r") as f:
    content = f.read()

# 1. Add Property Ownership UI and wrap Rent Agreement
pattern_ui = r"# ── Rent Agreement ──────────────────────────────────────\n        with st.expander\(\"Rent Agreement\"\):"
replacement_ui = """# ── Property Ownership ──────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        property_ownership = st.radio(
            "Property Ownership",
            options=["Rented", "Owned"],
            horizontal=True,
            index=0
        )

        # Initialize Rent Variables to avoid NameError if Owned
        landlord_name = landlord_relation = landlord_relative_name = landlord_address = ""
        shop_address = rent_amount = lease_months = ""
        rent_start_date = rent_agreement_date = None
        neighbor_right = neighbor_left = neighbor_front = neighbor_back = ""

        # ── Rent Agreement ──────────────────────────────────────
        if property_ownership == "Rented":
            with st.expander("Rent Agreement"):"""

content = re.sub(pattern_ui, replacement_ui, content)

# 2. Fix the indentation of the Rent Agreement block
# I need to indent lines 930 to 990 by 4 spaces.
# It's easier to just find the block and replace.
# But wait, `if property_ownership == "Rented":` is already adding a level.
# Actually, `with st.expander("Rent Agreement"):` is indented at 8 spaces, so `if property_ownership` will be at 8, and `with st.expander` needs to be at 12 spaces.
# Let's write a targeted function to indent the lines.

lines = content.split('\n')
in_rent = False
for i, line in enumerate(lines):
    if 'with st.expander("Rent Agreement"):' in line:
        in_rent = True
        # Indent the 'with' statement
        lines[i] = "    " + line
        continue
    if in_rent:
        if line.strip() == '# ── Equipment Receipts ──────────────────────────────────':
            in_rent = False
        else:
            if line.strip() != "":
                lines[i] = "    " + line

content = '\n'.join(lines)

# 3. Add to context
pattern_ctx = r"# Rent Agreement"
replacement_ctx = """"property_ownership": property_ownership,
            # Rent Agreement"""
content = re.sub(pattern_ctx, replacement_ctx, content)

# 4. Skip Rent Agreement in generate_documents
pattern_gen = r"        for tpl_name in template_files:"
replacement_gen = """        for tpl_name in template_files:
            if context.get("property_ownership") == "Owned" and "Rent Agreement" in tpl_name:
                continue"""
content = re.sub(pattern_gen, replacement_gen, content)

with open("app.py", "w") as f:
    f.write(content)
