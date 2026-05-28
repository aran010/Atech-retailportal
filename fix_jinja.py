import re

with open("create_templates.py", "r") as f:
    content = f.read()

# Replace {%p with {% and {%p endfor %} with {% endfor %} in the newly added director/auth functions
content = content.replace("{%p for dir in directors_data %}", "{% for dir in directors_data %}")
content = content.replace("{%p endfor %}", "{% endfor %}")

content = content.replace("{%p if property_ownership == 'Owned' %}", "{% if property_ownership == 'Owned' %}")
content = content.replace("{%p else %}", "{% else %}")
content = content.replace("{%p endif %}", "{% endif %}")

content = content.replace("{%p for rp in pharmacists_data %}", "{% for rp in pharmacists_data %}")

with open("create_templates.py", "w") as f:
    f.write(content)
