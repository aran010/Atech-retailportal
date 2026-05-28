import re

with open("app.py", "r") as f:
    content = f.read()

# 1. Replace the entire UI block from Registered Pharmacist Details to Rent Agreement
pattern_ui = r"# ── Registered Pharmacist ───────────────────────────────.*?# ── Rent Agreement ──────────────────────────────────────"

replacement_ui = """# ── Registered Pharmacist ───────────────────────────────
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
                    c_reg, c_regd = st.columns(2)
                    with c_reg:
                        rp_reg_no = st.text_input("Reg. Number", key=f"rp_reg_{i}")
                    with c_regd:
                        rp_reg_date = st.date_input("Reg. Date", value=None, min_value=MIN_DATE, max_value=MAX_DATE, key=f"rp_reg_date_{i}")
                    rp_reg_validity = st.date_input("Reg. Valid Upto", value=None, min_value=MIN_DATE, max_value=MAX_DATE, key=f"rp_reg_validity_{i}")
                
                col_e, col_f = st.columns(2)
                with col_e:
                    rp_qualification = st.text_input("Qualification", key=f"rp_qual_{i}")
                    rp_prev_firm_name = st.text_input("Previous Firm Name", key=f"rp_pfn_{i}")
                with col_f:
                    rp_college = st.text_input("College / Institute", key=f"rp_coll_{i}")
                    rp_prev_firm_address = st.text_input("Previous Firm Address", key=f"rp_pfa_{i}")
                
                c_res, _ = st.columns(2)
                with c_res:
                    rp_resign_date = st.date_input("Resignation Date (from previous firm)", value=None, min_value=MIN_DATE, max_value=MAX_DATE, key=f"rp_resign_date_{i}")
                
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
                    "reg_valid_upto": rp_reg_validity.strftime("%d-%m-%Y") if rp_reg_validity else "",
                    "qualification": rp_qualification.strip(),
                    "college": rp_college.strip(),
                    "prev_firm_name": rp_prev_firm_name.strip(),
                    "prev_firm_address": rp_prev_firm_address.strip(),
                    "resign_date": rp_resign_date.strftime("%d-%m-%Y") if rp_resign_date else "",
                })
                st.markdown("---")

        # ── Rent Agreement ──────────────────────────────────────"""

content = re.sub(pattern_ui, replacement_ui, content, flags=re.DOTALL)

# 2. Replace Context dictionary entries
pattern_dict = r"# Registered Pharmacist.*?# Rent Agreement"
replacement_dict = """# Pharmacists
            "pharmacists": pharmacists_data,
            # Rent Agreement"""

content = re.sub(pattern_dict, replacement_dict, content, flags=re.DOTALL)

# 3. Remove "rp_work_history": st.session_state.rp_work_history
content = content.replace('"rp_work_history": st.session_state.rp_work_history,', '')

with open("app.py", "w") as f:
    f.write(content)
