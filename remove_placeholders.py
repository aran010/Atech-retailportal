import re

with open("app.py", "r") as f:
    content = f.read()

# Remove placeholder="something"
# This regex handles cases where it's a kwarg: placeholder="..."
# We remove , placeholder="..." or placeholder="...", 
content = re.sub(r',?\s*placeholder="[^"]+"', '', content)
content = re.sub(r"options=\['S/o', 'D/o', 'W/o'\]", 'options=["S/o", "D/o", "W/o"], index=0', content)
content = re.sub(r'options=\["S/o", "D/o", "W/o"\]', 'options=["S/o", "D/o", "W/o"], index=0', content)

with open("app.py", "w") as f:
    f.write(content)
