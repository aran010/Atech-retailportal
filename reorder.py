import re

with open("create_templates.py", "r") as f:
    content = f.read()

# I will find the definitions of both functions and move them up.
func_pattern = r"(def _template_affidavit_director\(doc: docx\.Document\):.*)(def create_all_templates)"
match = re.search(func_pattern, content, flags=re.DOTALL)
if match:
    funcs = match.group(1)
    content = content.replace(funcs, "")
    # Place them before `# ── Registry: filename → builder function`
    content = content.replace("# ── Registry: filename → builder function ───────────────────────────────", 
                              funcs + "\n# ── Registry: filename → builder function ───────────────────────────────")

with open("create_templates.py", "w") as f:
    f.write(content)
