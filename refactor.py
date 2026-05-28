import re

with open("app.py", "r") as f:
    content = f.read()

# 1. Update Session State Init
target_1 = """if "doc_type" not in st.session_state:
    st.session_state.doc_type = "new_file"

if "num_partners" not in st.session_state:
    st.session_state.num_partners = 1"""

replacement_1 = """if "action_type" not in st.session_state:
    st.session_state.action_type = "new_file"

if "entity_type" not in st.session_state:
    st.session_state.entity_type = "proprietor"

if "num_entities" not in st.session_state:
    st.session_state.num_entities = 1"""

content = content.replace(target_1, replacement_1)

# 2. Update main() start and Sidebar
target_2 = """def main():
    # Determine which template directory to use
    doc_type = st.session_state.doc_type
    tpl_dir = ADDR_TEMPLATES_DIR if doc_type == "address_change" else TEMPLATES_DIR
    templates = get_template_files(tpl_dir)

    # ────────────────────────────────────────────────────────────
    # SIDEBAR
    # ────────────────────────────────────────────────────────────
    with st.sidebar:
        # Brand strip
        st.markdown(
            '<div class="sidebar-brand-strip">'
            '<h2>ATech Drug File</h2>'
            '</div>',
            unsafe_allow_html=True,
        )

        # Nav label
        st.markdown(
            '<div class="sidebar-nav-label">Navigation</div>',
            unsafe_allow_html=True,
        )

        # Navigation items as buttons
        if st.button(
            "New File (Proprietor)",
            use_container_width=True,
            type="primary" if doc_type == "new_file" else "secondary",
            key="nav_new_file",
        ):
            reset_session()
            st.session_state.doc_type = "new_file"
            st.rerun()

        if st.button(
            "New File (Partner)",
            use_container_width=True,
            type="primary" if doc_type == "new_file_partner" else "secondary",
            key="nav_new_file_partner",
        ):
            reset_session()
            st.session_state.doc_type = "new_file_partner"
            st.session_state.num_partners = 1
            st.rerun()

        if st.button(
            "Address Change",
            use_container_width=True,
            type="primary" if doc_type == "address_change" else "secondary",
            key="nav_address_change",
        ):
            reset_session()
            st.session_state.doc_type = "address_change"
            st.rerun()

    # ────────────────────────────────────────────────────────────
    # MAIN CONTENT
    # ────────────────────────────────────────────────────────────

    # ── Header & Meta Bar ───────────────────────────────────────
    if doc_type == "address_change":
        type_label = "ADDRESS CHANGE"
    elif doc_type == "new_file_partner":
        type_label = "NEW FILE (PARTNER)"
    else:
        type_label = "NEW FILE (PROPRIETOR)"
    st.markdown(
        f\"\"\"
        <div class="portal-header-wrapper">
            <div class="portal-header">
                <h1>ARAN TECHNOLOGIES <span class="accent">-</span> RETAIL PORTAL</h1>
                <span class="rule"></span>
                <p class="subtitle">Automated document generation for new retail drug file processing</p>
            </div>
            <div class="meta-bar">
                <div class="meta-pill">Mode  <span>{type_label}</span></div>
                <div class="meta-pill">Templates  <span>{len(templates)}</span></div>
                <div class="meta-pill">Date  <span>{date.today().strftime("%d %b %Y")}</span></div>
                <div class="meta-pill">Output  <span>ZIP</span></div>
            </div>
        </div>
        \"\"\",
        unsafe_allow_html=True,
    )"""

replacement_2 = """def main():
    # ────────────────────────────────────────────────────────────
    # SIDEBAR
    # ────────────────────────────────────────────────────────────
    with st.sidebar:
        # Brand strip
        st.markdown(
            '<div class="sidebar-brand-strip">'
            '<h2>ATech Drug File</h2>'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown('<div class="sidebar-nav-label">Action</div>', unsafe_allow_html=True)
        action_val = st.radio("Action", ["New File", "Address Change"], label_visibility="collapsed")
        
        st.markdown('<div class="sidebar-nav-label">Entity Type</div>', unsafe_allow_html=True)
        entity_val = st.radio("Entity Type", ["Proprietor", "Partner", "Director"], label_visibility="collapsed")
        
        action_type = "new_file" if action_val == "New File" else "address_change"
        entity_type = entity_val.lower()
        
        if st.session_state.action_type != action_type or st.session_state.entity_type != entity_type:
            st.session_state.action_type = action_type
            st.session_state.entity_type = entity_type

    # Determine which template directory to use
    tpl_dir = ADDR_TEMPLATES_DIR if action_type == "address_change" else TEMPLATES_DIR
    templates = get_template_files(tpl_dir)

    # ────────────────────────────────────────────────────────────
    # MAIN CONTENT
    # ────────────────────────────────────────────────────────────

    # ── Header & Meta Bar ───────────────────────────────────────
    type_label = f"{action_val.upper()} ({entity_val.upper()})"
    st.markdown(
        f\"\"\"
        <div class="portal-header-wrapper">
            <div class="portal-header">
                <h1>ARAN TECHNOLOGIES <span class="accent">-</span> RETAIL PORTAL</h1>
                <span class="rule"></span>
                <p class="subtitle">Automated document generation for new retail drug file processing</p>
            </div>
            <div class="meta-bar">
                <div class="meta-pill">Mode  <span>{type_label}</span></div>
                <div class="meta-pill">Templates  <span>{len(templates)}</span></div>
                <div class="meta-pill">Date  <span>{date.today().strftime("%d %b %Y")}</span></div>
                <div class="meta-pill">Output  <span>ZIP</span></div>
            </div>
        </div>
        \"\"\",
        unsafe_allow_html=True,
    )"""

content = content.replace(target_2, replacement_2)


# 3. Update Work History block
target_3 = """    st.markdown(
        '<div class="section-title">Work History</div>', unsafe_allow_html=True
    )

    if doc_type == "new_file_partner":
        num_partners = st.session_state.get("num_partners", 1)
        for i in range(num_partners):
            state_key = f"partner_work_history_{i}"
            if state_key not in st.session_state:
                st.session_state[state_key] = [
                    {"sr_no": "1", "time_period": "", "occupation": "", "remarks": ""}
                ]
            with st.expander(f"Partner {i+1} Work History", expanded=False):
                render_work_history(f"p_{i}", state_key)
    else:
        with st.expander("Proprietor Work History", expanded=False):
            render_work_history("prop", "prop_work_history")"""

replacement_3 = """    st.markdown(
        '<div class="section-title">Work History</div>', unsafe_allow_html=True
    )

    if entity_type in ["partner", "director"]:
        num_entities = st.session_state.get("num_entities", 1)
        entity_label = "Partner" if entity_type == "partner" else "Director"
        for i in range(num_entities):
            state_key = f"{entity_type}_work_history_{i}"
            if state_key not in st.session_state:
                st.session_state[state_key] = [
                    {"sr_no": "1", "time_period": "", "occupation": "", "remarks": ""}
                ]
            with st.expander(f"{entity_label} {i+1} Work History", expanded=False):
                render_work_history(f"e_{i}", state_key)
    else:
        with st.expander("Proprietor Work History", expanded=False):
            render_work_history("prop", "prop_work_history")"""

content = content.replace(target_3, replacement_3)


# 4. Update Client Details section
target_4 = """    st.markdown(
        '<div class="section-title">Client Details</div>', unsafe_allow_html=True
    )

    if doc_type == "new_file_partner":
        # Streamlit doesn't allow dynamic form fields to rerender without submit inside form,
        # so we place the control outside the form.
        st.number_input("Number of Partners (Press Enter to update form)", min_value=1, value=1, step=1, key="num_partners")

    with st.form("document_form", clear_on_submit=False):

        # ── Document Date ───────────────────────────────────────
        col_dt, col_blank = st.columns([1, 2])
        with col_dt:
            doc_date = st.date_input(
                "Document Date", value=date.today(),
                min_value=MIN_DATE, max_value=MAX_DATE,
            )

        # ── Proprietor / Partner & Firm ───────────────────────────────────
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
                    firm_address = st.text_area("Firm / Shop Address :red[*]", height=80)

        # ── Address Change Fields (shown only for address change) ───
        if doc_type == "address_change":"""

replacement_4 = """    st.markdown(
        '<div class="section-title">Client Details</div>', unsafe_allow_html=True
    )

    if entity_type in ["partner", "director"]:
        entity_label = "Partners" if entity_type == "partner" else "Directors"
        st.number_input(f"Number of {entity_label} (Press Enter to update form)", min_value=1, value=1, step=1, key="num_entities")

    with st.form("document_form", clear_on_submit=False):

        # ── Document Date ───────────────────────────────────────
        col_dt, col_blank = st.columns([1, 2])
        with col_dt:
            doc_date = st.date_input(
                "Document Date", value=date.today(),
                min_value=MIN_DATE, max_value=MAX_DATE,
            )

        # ── Dynamic Entity & Firm ───────────────────────────────────
        if entity_type in ["partner", "director"]:
            entity_label_s = "Partner" if entity_type == "partner" else "Director"
            entity_label_pl = "Partners" if entity_type == "partner" else "Directors"
            
            with st.expander(f"{entity_label_pl} and Firm Details", expanded=True):
                firm_name = st.text_input("Firm Name :red[*]")
                firm_address = st.text_area("Firm / Shop Address :red[*]", height=80)
                st.markdown("---")
                
                entities_data = []
                num_entities = st.session_state.get("num_entities", 1)
                for i in range(num_entities):
                    st.markdown(f"**{entity_label_s} {i+1}**")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        p_name = st.text_input(f"{entity_label_s} Name :red[*]", key=f"e_name_{i}")
                        c_rel, c_father = st.columns(2)
                        with c_rel:
                            p_rel = st.selectbox("Relation", options=["S/o", "D/o", "W/o"], index=0, key=f"e_rel_{i}")
                        with c_father:
                            p_father = st.text_input("Father / Relative", key=f"e_father_{i}")
                    with col_b:
                        p_address = st.text_area(f"{entity_label_s} Address :red[*]", height=80, key=f"e_address_{i}")
                        p_phone = st.text_input("Phone", max_chars=10, key=f"e_phone_{i}")
                    
                    entities_data.append({
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
                    firm_address = st.text_area("Firm / Shop Address :red[*]", height=80)

        # ── Address Change Fields (shown only for address change) ───
        if action_type == "address_change":"""

content = content.replace(target_4, replacement_4)


# 5. Update validation and context builder
target_5 = """    if submitted:
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

replacement_5 = """    if submitted:
        # Validate key fields
        required = {
            "Firm Name": firm_name,
            "Firm Address": firm_address,
            "RP Name": rp_name,
        }
        if entity_type == "proprietor":
            required["Proprietor Name"] = prop_name
        else:
            entity_label_s = "Partner" if entity_type == "partner" else "Director"
            if entities_data:
                required[f"{entity_label_s} 1 Name"] = entities_data[0]["name"]

        missing = [k for k, v in required.items() if not v.strip()]

        if missing:
            st.warning(
                "Please fill in the following required fields: "
                f"**{', '.join(missing)}**"
            )
            st.stop()

        # Default proprietor values if multi-entity mode
        if entity_type in ["partner", "director"]:
            prop_name = entities_data[0]["name"] if entities_data else ""
            prop_relation = entities_data[0]["relation"] if entities_data else ""
            prop_father_name = entities_data[0]["father_name"] if entities_data else ""
            prop_address = entities_data[0]["address"] if entities_data else ""
            prop_phone = entities_data[0]["phone"] if entities_data else ""

        # Build context dictionary
        context = {
            # Proprietor (used as fallback or for main proprietor)
            "prop_name": prop_name.strip(),
            "prop_relation": prop_relation,
            "prop_father_name": prop_father_name.strip(),
            "prop_address": prop_address.strip(),
            "prop_phone": prop_phone.strip(),
            "partners": entities_data if entity_type == "partner" else [],
            "directors": entities_data if entity_type == "director" else [],"""

content = content.replace(target_5, replacement_5)


# 6. Inject Work History to entities_data
target_6 = """        if doc_type == "new_file_partner":
            for i in range(len(partners_data)):
                partners_data[i]["work_history"] = st.session_state.get(f"partner_work_history_{i}", [])

        # Add address-change-specific fields
        if doc_type == "address_change":"""

replacement_6 = """        if entity_type in ["partner", "director"]:
            for i in range(len(entities_data)):
                entities_data[i]["work_history"] = st.session_state.get(f"{entity_type}_work_history_{i}", [])

        # Add address-change-specific fields
        if action_type == "address_change":"""

content = content.replace(target_6, replacement_6)


# 7. Update file name prefix
target_7 = """        safe_name = sanitize_filename(prop_name)
        prefix = "Address_Change" if doc_type == "address_change" else "New_Retail_File"
        zip_filename = f"{prefix}_{safe_name}.zip\"\"\""""

replacement_7 = """        safe_name = sanitize_filename(prop_name)
        prefix = "Address_Change" if action_type == "address_change" else "New_Retail_File"
        zip_filename = f"{prefix}_{safe_name}.zip\"\"\""""

content = content.replace(target_7, replacement_7)

with open("app.py", "w") as f:
    f.write(content)
