import re

with open("create_templates.py", "r") as f:
    content = f.read()

# 1. Define _template_affidavit_director
director_template = '''
def _template_affidavit_director(doc: docx.Document):
    _add_para(doc, "AFFIDAVIT (DIRECTOR)", alignment=WD_ALIGN_PARAGRAPH.CENTER, bold=True)
    _add_para(doc,
        "I, {{r prop_name }} {{r prop_relation }} Sh. {{r prop_father_name }} R/o {{r prop_address }}, "
        "do hereby solemnly affirm & declare as under:"
    )
    _add_para(doc,
        "That neither I nor any other director have ever been convicted by any court in India under the Drug & Cosmetics Act 1940 and Rules 1945 framed there under."
    )
    _add_para(doc,
        "That I am director of the firm M/s {{r firm_name }} situated at {{r firm_address }}, and do hereby applying for grant of new retail sale drug Licenses."
    )
    _add_para(doc, "That the other directors of the firm are the following detail:-")
    
    _add_para(doc,
        "{%p for dir in directors_data %}"
        "{{r dir.name }} {{r dir.relation }} Sh. {{r dir.father_name }} R/o {{r dir.address }}."
        "{%p endfor %}"
    )
    
    _add_para(doc,
        "That I myself{% if auth_signatory %} and {{r auth_signatory.name }}{% endif %} will be the overall in-charge and responsible person to our said firm for its day to day conduct & Control of business."
    )
    
    _add_para(doc,
        "{%p if property_ownership == 'Owned' %}"
        "That the sale premises of my said firm is the owned property and the same premise is under my legal possession/occupancy and it is not connected to any residence."
        "{%p else %}"
        "That the sale premises of my said firm is the rented property and the same premise is under my legal possession/occupancy and it is not connected to any residence."
        "{%p endif %}"
    )

    _add_para(doc,
        "That I had never been a proprietor or an active or sleeping partner at any such firm, whose wholesale/retail sale drugs license had ever been cancelled by the licensing authority for any reason whatsoever."
    )
    _add_para(doc, "That the firm has appointed are the following Regd. Pharmacists:-")
    
    _add_para(doc,
        "{%p for rp in pharmacists_data %}"
        "{{r rp.name }} {{r rp.relation }} Sh. {{r rp.father_name }} R/o {{r rp.address }}, to sell by way of retail sale, who has joined my firm as regd. Pharmacist at a salary of Rs. {{r rp.salary }}/- per month w.e.f {{r rp.joining_date }} and {% if rp.relation == 'D/o' or rp.relation == 'W/o' %}she{% else %}he{% endif %} is registered on H.S.P.C vide Regn. No. {{r rp.reg_no }} dated {{r rp.reg_date }} which is valid up to dated {{r rp.reg_valid_upto }}."
        "{%p endfor %}"
    )
    
    _add_para(doc,
        "That I shall pay the salary of the competent person by way of cheque/online transfer in his account."
    )
    _add_para(doc,
        "That I have installed CCTV camera at my shop/premises and I will keep one-month backup recording of CCTV Camera."
    )
    _add_para(doc,
        "That the sale premises of my said firm will not be used/utilized for any other purpose expect for business of those categories of drugs which will include in the License applied for by me or granted to me at my said firm."
    )
    _add_para(doc,
        "That I shall comply with the provisions, rules regulation and conditions of the Drugs & Cosmetics Act 1940 and Rules1945 framed there under for the time being in force or are amended from time to time under the said Act & Rules."
    )
    _add_para(doc,
        "That I shall obtain new Drug License in case of any change in constitution or premises takes place at my firm. I shall inform the Licensing Authorities if any area alterations take place at my firm."
    )
    _add_para(doc,
        "That if in case of resignation of regd. Pharmacist of my firm sale will not done in the absence of regd. Pharmacist and I will appoint new regd. Pharmacist immediately and will give written information to the drugs Dep’t within one month."
    )
    _add_para(doc,
        "That if in case I close my firm I will give written information along with list of drugs laying at my firm unsold."
    )
    
    p_dep = doc.add_paragraph()
    p_dep.add_run("DEPONENT").bold = True
    p_dep.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    _add_para(doc, "Verification:-")
    _add_para(doc,
        "I the above named do hereby solemnly affirm and declare that whatsoever is started above is true and correct the best of my knowledge and belief and nothing has been concealed therein."
    )
    
    _add_para(doc, "Date:-\nPlace: -")
    p_dep2 = doc.add_paragraph()
    p_dep2.add_run("DEPONENT").bold = True
    p_dep2.alignment = WD_ALIGN_PARAGRAPH.RIGHT

def _template_affidavit_auth(doc: docx.Document):
    _add_para(doc, "AFFIDAVIT (Auth. Signatory)", alignment=WD_ALIGN_PARAGRAPH.CENTER, bold=True)
    _add_para(doc,
        "I, {{r prop_name }} {{r prop_relation }} Sh. {{r prop_father_name }} R/o {{r prop_address }}, "
        "do hereby solemnly affirm & declare as under:"
    )
    _add_para(doc,
        "That neither I nor any directors have ever been convicted by any court in India under the Drug & Cosmetics Act 1940 and Rules 1945 framed there under."
    )
    _add_para(doc,
        "That I am auth. Signatory of the firm M/s {{r firm_name }} situated at {{r firm_address }}, and do hereby applying for grant of new retail sale drug Licenses."
    )
    _add_para(doc, "That the directors of the firm are the following detail:-")
    
    _add_para(doc,
        "{%p for dir in directors_data %}"
        "{{r dir.name }} {{r dir.relation }} Sh. {{r dir.father_name }} R/o {{r dir.address }}."
        "{%p endfor %}"
    )
    
    _add_para(doc,
        "That I myself and {% if directors_data %}{{r directors_data[0].name }}{% else %}the Director{% endif %} will be the overall in-charge and responsible person to our said firm for its day to day conduct & Control of business."
    )
    
    _add_para(doc,
        "{%p if property_ownership == 'Owned' %}"
        "That the sale premises of my said firm is the owned property and the same premise is under my legal possession/occupancy and it is not connected to any residence."
        "{%p else %}"
        "That the sale premises of my said firm is the rented property and the same premise is under my legal possession/occupancy and it is not connected to any residence."
        "{%p endif %}"
    )

    _add_para(doc,
        "That I had never been a proprietor or an active or sleeping partner at any such firm, whose wholesale/retail sale drugs license had ever been cancelled by the licensing authority for any reason whatsoever."
    )
    _add_para(doc, "That the firm has appointed are the following Regd. Pharmacists:-")
    
    _add_para(doc,
        "{%p for rp in pharmacists_data %}"
        "{{r rp.name }} {{r rp.relation }} Sh. {{r rp.father_name }} R/o {{r rp.address }}, to sell by way of retail sale, who has joined my firm as regd. Pharmacist at a salary of Rs. {{r rp.salary }}/- per month w.e.f {{r rp.joining_date }} and {% if rp.relation == 'D/o' or rp.relation == 'W/o' %}she{% else %}he{% endif %} is registered on H.S.P.C vide Regn. No. {{r rp.reg_no }} dated {{r rp.reg_date }} which is valid up to dated {{r rp.reg_valid_upto }}."
        "{%p endfor %}"
    )
    
    _add_para(doc,
        "That I shall pay the salary of the competent person by way of cheque/online transfer in his account."
    )
    _add_para(doc,
        "That I have installed CCTV camera at my shop/premises and I will keep one-month backup recording of CCTV Camera."
    )
    _add_para(doc,
        "That the sale premises of my said firm will not be used/utilized for any other purpose expect for business of those categories of drugs which will include in the License applied for by me or granted to me at my said firm."
    )
    _add_para(doc,
        "That I shall comply with the provisions, rules regulation and conditions of the Drugs & Cosmetics Act 1940 and Rules1945 framed there under for the time being in force or are amended from time to time under the said Act & Rules."
    )
    _add_para(doc,
        "That I shall obtain new Drug License in case of any change in constitution or premises takes place at my firm. I shall inform the Licensing Authorities if any area alterations take place at my firm."
    )
    _add_para(doc,
        "That if in case of resignation of regd. Pharmacist of my firm sale will not done in the absence of regd. Pharmacist and I will appoint new regd. Pharmacist immediately and will give written information to the drugs Dep’t within one month."
    )
    _add_para(doc,
        "That if in case I close my firm I will give written information along with list of drugs laying at my firm unsold."
    )
    
    p_dep = doc.add_paragraph()
    p_dep.add_run("DEPONENT").bold = True
    p_dep.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    _add_para(doc, "Verification:-")
    _add_para(doc,
        "I the above named do hereby solemnly affirm and declare that whatsoever is started above is true and correct the best of my knowledge and belief and nothing has been concealed therein."
    )
    
    _add_para(doc, "Date:-\nPlace: -")
    p_dep2 = doc.add_paragraph()
    p_dep2.add_run("DEPONENT").bold = True
    p_dep2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
'''

# We inject the new functions right before `def create_all_templates`
pattern = r'(def create_all_templates)'
content = re.sub(pattern, director_template + r'\n\1', content)

# We also need to add them to the maps
new_file_map_update = """    "AFFIDAVIT (Director).docx":            _template_affidavit_director,
    "AFFIDAVIT (Auth Signatory).docx":      _template_affidavit_auth,"""
# Since _template_affidavit_prop is in the file map:
content = content.replace('"AFFIDAVIT (prop).docx":                _template_affidavit_prop,', 
                          f'"AFFIDAVIT (prop).docx":                _template_affidavit_prop,\n{new_file_map_update}')

addr_change_map_update = """    "AFFIDAVIT (Director).docx":            _template_affidavit_director,
    "AFFIDAVIT (Auth Signatory).docx":      _template_affidavit_auth,"""
content = content.replace('"AFFIDAVIT (prop).docx":                _template_addr_affidavit_prop,', 
                          f'"AFFIDAVIT (prop).docx":                _template_addr_affidavit_prop,\n{addr_change_map_update}')


with open("create_templates.py", "w") as f:
    f.write(content)
