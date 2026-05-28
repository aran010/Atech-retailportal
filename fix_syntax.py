with open("create_templates.py", "r") as f:
    content = f.read()

content = content.replace('"Date:-\nPlace: -"', '"Date:-\\nPlace: -"')

with open("create_templates.py", "w") as f:
    f.write(content)
