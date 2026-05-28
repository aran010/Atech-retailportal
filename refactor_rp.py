import re

with open("app.py", "r") as f:
    content = f.read()

# 1. Init num_pharmacists
target_1 = """if "num_entities" not in st.session_state:
    st.session_state.num_entities = 1"""

replacement_1 = """if "num_entities" not in st.session_state:
    st.session_state.num_entities = 1

if "num_pharmacists" not in st.session_state:
    st.session_state.num_pharmacists = 1"""

content = content.replace(target_1, replacement_1)

# 2. Update Work History block
target_2 = """    with st.expander("Registered Pharmacist Work History", expanded=False):
        render_work_history("rp", "rp_work_history")"""

replacement_2 = """    num_pharmacists = st.session_state.get("num_pharmacists", 1)
    for i in range(num_pharmacists):
        state_key = f"rp_work_history_{i}"
        if state_key not in st.session_state:
            st.session_state[state_key] = [
                {"sr_no": "1", "time_period": "", "occupation": "", "remarks": ""}
            ]
        with st.expander(f"Registered Pharmacist {i+1} Work History", expanded=False):
            render_work_history(f"rp_{i}", state_key)"""

content = content.replace(target_2, replacement_2)


# 3. Add Pharmacists number input
target_3 = """    if entity_type in ["partner", "director"]:
        entity_label = "Partners" if entity_type == "partner" else "Directors"
        st.number_input(f"Number of {entity_label} (Press Enter to update form)", min_value=1, value=1, step=1, key="num_entities")"""

replacement_3 = """    if entity_type in ["partner", "director"]:
        entity_label = "Partners" if entity_type == "partner" else "Directors"
        st.number_input(f"Number of {entity_label} (Press Enter to update form)", min_value=1, value=1, step=1, key="num_entities")
        
    st.number_input("Number of Pharmacists (Press Enter to update form)", min_value=1, value=1, step=1, key="num_pharmacists")"""

content = content.replace(target_3, replacement_3)


# 4. Refactor RP details
target_4 = """        # ── Registered Pharmacist ───────────────────────────────
        with st.expander("Registered Pharmacist Details"):
            col_c, col_d = st.columns(2)

            with col_c:
                rp_name = st.text_input(
                    "RP Name :red[*]"
                )
                c_rp_rel, c_rp_f = st.columns(2)
                with c_rp_rel:
                    rp_relation = st.selectbox(
                        "Relation", options=["S/o", "D/o", "W/o"], index=0,
                        key="rp_relation",
                    )
                with c_rp_f:
                    rp_father_name = st.text_input(
                        "Father / Relative", key="rp_father",
                    )
                rp_address = st.text_area(
                    "RP Address", height=80,
                )
                rp_phone = st.text_input(
                    "RP Phone", max_chars=10
                )

            with col_d:
                rp_salary = st.text_input(
                    "Salary (Rs.)"
                )
                rp_joining_date = st.date_input(
                    "Joining Date", value=None,
                    min_value=MIN_DATE, max_value=MAX_DATE,
                )
                rp_reg_no = st.text_input(
                    "Registration No."
                )
                rp_reg_date = st.date_input(
                    "Registration Date", value=None,
                    min_value=MIN_DATE, max_value=MAX_DATE,
                )
                rp_reg_validity = st.date_input(
                    "Registration Validity", value=None,
                    min_value=MIN_DATE, max_value=MAX_DATE,
                )"""

replacement_4 = """        # ── Registered Pharmacist ───────────────────────────────
        with st.expander("Registered Pharmacist Details", expanded=True):
            pharmacists_data = []
            num_pharmacists = st.session_state.get("num_pharmacists", 1)
            for i in range(num_pharmacists):
                st.markdown(f"**Pharmacist {i+1}**")
                col_c, col_d = st.columns(2)
                with col_c:
                    rp_name = st.text_input("Pharmacist Name :red[*]", key=f"rp_name_{i}")
                    c_rp_rel, c_rp_f = st.columns(2)
                    with c_rp_rel:
                        rp_relation = st.selectbox("Relation", options=["S/o", "D/o", "W/o"], index=0, key=f"rp_relation_{i}")
                    with c_rp_f:
                        rp_father_name = st.text_input("Father / Relative", key=f"rp_father_{i}")
                    rp_address = st.text_area("Pharmacist Address", height=80, key=f"rp_address_{i}")
                    rp_phone = st.text_input("Phone", max_chars=10, key=f"rp_phone_{i}")

                with col_d:
                    rp_salary = st.text_input("Salary (Rs.)", key=f"rp_salary_{i}")
                    rp_joining_date = st.date_input("Joining Date", value=None, min_value=MIN_DATE, max_value=MAX_DATE, key=f"rp_joining_{i}")
                    rp_reg_no = st.text_input("Registration No.", key=f"rp_reg_{i}")
                    rp_reg_date = st.date_input("Registration Date", value=None, min_value=MIN_DATE, max_value=MAX_DATE, key=f"rp_reg_date_{i}")
                    rp_reg_validity = st.date_input("Registration Validity", value=None, min_value=MIN_DATE, max_value=MAX_DATE, key=f"rp_reg_validity_{i}")
                
                pharmacists_data.append({
                    "name": rp_name.strip(),
                    "relation": rp_relation,
                    "father_name": rp_father_name.strip(),
                    "address": rp_address.strip(),
                    "phone": rp_phone.strip(),
                    "salary": rp_salary.strip(),
                    "joining_date": rp_joining_date.strftime("%d-%m-%Y") if rp_joining_date else "",
                    "reg_no": rp_reg_no.strip(),
                    "reg_date": rp_reg_date.strftime("%d-%m-%Y") if rp_reg_date else "",
                    "reg_validity": rp_reg_validity.strftime("%d-%m-%Y") if rp_reg_validity else "",
                })
                st.markdown("---")"""

content = content.replace(target_4, replacement_4)

# 5. Form Validation Update
target_5 = """    if submitted:
        # Validate key fields
        required = {
            "Firm Name": firm_name,
            "Firm Address": firm_address,
            "RP Name": rp_name,
        }"""

replacement_5 = """    if submitted:
        # Validate key fields
        required = {
            "Firm Name": firm_name,
            "Firm Address": firm_address,
        }
        if pharmacists_data:
            required["Pharmacist 1 Name"] = pharmacists_data[0]["name"]"""

content = content.replace(target_5, replacement_5)

# 6. Context dictionary update
target_6 = """            # Registered Pharmacist
            "rp_name": rp_name.strip(),
            "rp_relation": rp_relation,
            "rp_father_name": rp_father_name.strip(),
            "rp_address": rp_address.strip(),
            "rp_phone": rp_phone.strip(),
            "rp_salary": rp_salary.strip(),
            "rp_joining_date": rp_joining_date.strftime("%d-%m-%Y") if rp_joining_date else "",
            "rp_reg_no": rp_reg_no.strip(),
            "rp_reg_date": rp_reg_date.strftime("%d-%m-%Y") if rp_reg_date else "",
            "rp_reg_validity": rp_reg_validity.strftime("%d-%m-%Y") if rp_reg_validity else "",
            "rp_work_history": st.session_state.get("rp_work_history", []),"""

replacement_6 = """            # Pharmacists
            "pharmacists": pharmacists_data,"""

content = content.replace(target_6, replacement_6)

# 7. Inject work history into pharmacists_data
target_7 = """        if entity_type in ["partner", "director"]:
            for i in range(len(entities_data)):
                entities_data[i]["work_history"] = st.session_state.get(f"{entity_type}_work_history_{i}", [])"""

replacement_7 = """        if entity_type in ["partner", "director"]:
            for i in range(len(entities_data)):
                entities_data[i]["work_history"] = st.session_state.get(f"{entity_type}_work_history_{i}", [])
                
        for i in range(len(pharmacists_data)):
            pharmacists_data[i]["work_history"] = st.session_state.get(f"rp_work_history_{i}", [])"""

content = content.replace(target_7, replacement_7)

with open("app.py", "w") as f:
    f.write(content)
