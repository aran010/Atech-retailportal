with open("app.py", "r") as f:
    lines = f.readlines()

for i in range(len(lines)):
    if 'with st.expander("Rent Agreement"):' in lines[i]:
        lines[i] = "            with st.expander(\"Rent Agreement\"):\n"
    elif 'if property_ownership == "Rented":' in lines[i]:
        lines[i] = "        if property_ownership == \"Rented\":\n"

with open("app.py", "w") as f:
    f.writelines(lines)
