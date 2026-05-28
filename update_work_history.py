import re

with open("app.py", "r") as f:
    content = f.read()

# 1. Update Work History block
target_1 = """    st.markdown(
        '<div class="section-title">Work History</div>', unsafe_allow_html=True
    )

    with st.expander("Proprietor Work History", expanded=False):
        render_work_history("prop", "prop_work_history")"""

replacement_1 = """    st.markdown(
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

content = content.replace(target_1, replacement_1)


# 2. Update Context generation to inject work history into partners
target_2 = """            # Working Reports
            "prop_work_history": st.session_state.prop_work_history,
            "rp_work_history": st.session_state.rp_work_history,
            # Common"""

replacement_2 = """            # Working Reports
            "prop_work_history": st.session_state.prop_work_history,
            "rp_work_history": st.session_state.rp_work_history,
            # Common"""

# Let's inject partner work history mapping right before context generation finishes
target_3 = """        # Add address-change-specific fields"""
replacement_3 = """        if doc_type == "new_file_partner":
            for i in range(len(partners_data)):
                partners_data[i]["work_history"] = st.session_state.get(f"partner_work_history_{i}", [])

        # Add address-change-specific fields"""

content = content.replace(target_3, replacement_3)

with open("app.py", "w") as f:
    f.write(content)
