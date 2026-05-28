import re

with open("create_templates.py", "r") as f:
    content = f.read()

partner_templates = '''
def _template_affidavit_partner(doc: docx.Document):
    _add_para(doc, "AFFIDAVIT (PARTNER)", alignment=WD_ALIGN_PARAGRAPH.CENTER, bold=True)
    _add_para(doc,
        "I, {{r prop_name }} {{r prop_relation }} Sh. {{r prop_father_name }} R/o {{r prop_address }}, do hereby solemnly affirm & declare as under: -"
    )
    _add_para(doc,
        "That I have never been convicted by any court in India under the Drug & Cosmetics Act 1940 and Rules 1945 framed there under."
    )
    _add_para(doc,
        "That I am active partner of the firm M/s {{r firm_name }} Situated at {{r firm_address }}, and hereby applying for grant of new retail sale drug license. "
    )
    _add_para(doc, "That the other partner of the firm are the following detail:-")
    _add_para(doc,
        "{% for p in partners_data %}"
        "Mr./Ms. {{r p.name }} {{r p.relation }} Sh. {{r p.father_name }} R/o {{r p.address }}."
        "{% endfor %}"
    )
    _add_para(doc,
        "That I myself and {% if partners_data %}{{r partners_data[0].name }}{% else %}the Partner{% endif %} will be the overall in-charge and responsible person to our said firm for its day to day conduct and control of business."
    )
    _add_para(doc,
        "{% if property_ownership == 'Owned' %}"
        "That the sale premises of my said firm is the owned property and the same premises is under my legal possession/occupancy and it is not connected to any residence."
        "{% else %}"
        "That the sale premises of my said firm is the rented property and the same premises is under my legal possession/occupancy as a tenant and it is not connected to any residence."
        "{% endif %}"
    )
    _add_para(doc,
        "That I had never been a partner or an active or sleeping partner at any such firm, whose whole sale/retail sale Drug license had ever been cancelled by the licensing authority for any reason, whatsoever."
    )
    _add_para(doc, "That the firm has appointed are the following Regd. Pharmacists:-")
    _add_para(doc,
        "{% for rp in pharmacists_data %}"
        "{{r rp.name }} {{r rp.relation }} Sh. {{r rp.father_name }} R/o {{r rp.address }}, to sell by way of retail sale, who has joined my firm as regd. Pharmacist and {% if rp.relation == 'D/o' or rp.relation == 'W/o' %}she{% else %}he{% endif %} is regd. Pharmacist from H.S.P.C vide Regn. No. {{r rp.reg_no }} dated {{r rp.reg_date }} which is valid up {{r rp.reg_valid_upto }}."
        "{% endfor %}"
    )
    _add_para(doc,
        "That I would keep all records of sale & purchase etc. of drugs in cash memos / bills / invoices of my said firm, which shall be maintained properly and in legible manner."
    )
    _add_para(doc,
        "That the sale premises of my said firm will not be used / utilized for any other purpose expect for business of those categories of drugs which include in the license applied for by me or granted to me at my said firm."
    )
    _add_para(doc,
        "That I shall comply with the provision, rules, regulation and condition of the Drugs & Cosmetics Act 1940 and Rules 1945 framed there under for the time being in force or are amended from time to time under the said Acts and Rules."
    )
    _add_para(doc,
        "That I shall obtain new Drug License in case of any change in constitution or premises takes place at my firm. I shall inform the Licensing Authority, if any area alteration takes place at my firm."
    )
    _add_para(doc,
        "That the sale will not be done in the absence of Regd. Pharmacist in case of his resignation and I will appoint new Regd. Pharmacist immediately under written Intimation to the Licensing authority, within one month of such change."
    )
    _add_para(doc,
        "That if in case, I close my firm I will give written information along with list lying at my firm unsold."
    )
    p_dep = doc.add_paragraph()
    p_dep.add_run("Deponent").bold = True
    p_dep.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    _add_para(doc, "Verification:")
    _add_para(doc,
        "I, the above named do hereby solemnly affirm and declare that whatever is started above is true and correct to the best of my knowledge and belief and nothing cancelled therein."
    )
    _add_para(doc, "Place: \nDated: ")
    p_dep2 = doc.add_paragraph()
    p_dep2.add_run("Deponent").bold = True
    p_dep2.alignment = WD_ALIGN_PARAGRAPH.RIGHT

def _template_partner_working_report(doc: docx.Document):
    _add_para(doc, "To whom soever it may concern", alignment=WD_ALIGN_PARAGRAPH.CENTER, bold=True)
    _add_para(doc,
        "I, {{r prop_name }} {{r prop_relation }} Sh. {{r prop_father_name }} R/o {{r prop_address }}, do hereby certify that during the last three years my working details are as follows:  "
    )
    _add_para(doc, "Phone no-({{r prop_phone }})")
    
    p = doc.add_paragraph("Date: -……………\t\t\t\t\t\t")
    p.add_run("(Partner Signature)").bold = True

    _add_para(doc, "Verification", alignment=WD_ALIGN_PARAGRAPH.CENTER, bold=True)
    _add_para(doc,
        "I Know, Mr./Ms. {{r prop_name }} {{r prop_relation }} Sh. {{r prop_father_name }} having personally for the last three years and as per best of my knowledge, the above-mentioned details are correct and he/she has never been prosecuted/convicted by any Court in India."
    )
    _add_para(doc, "Name: - ………………………………………        Name: -..............................................................")
    _add_para(doc, "Add. /Designation: - ……………………….….     Add. /Designation: -……………….………….")
    _add_para(doc, "Date: - ………………………………………….     Date: -..........................................................")

def _template_partnership_deed(doc: docx.Document):
    _add_para(doc, "PARTNERSHIP DEED", alignment=WD_ALIGN_PARAGRAPH.CENTER, bold=True)
    _add_para(doc, "This deed of partnership is made by between the following parties: -")
    
    _add_para(doc,
        "Mr./Ms. {{r prop_name }} {{r prop_relation }} Sh. {{r prop_father_name }} R/o {{r prop_address }}. (Hereinafter called the party of the first part). Active Partner"
    )
    _add_para(doc,
        "{% for p in partners_data %}"
        "Mr./Ms. {{r p.name }} {{r p.relation }} Sh. {{r p.father_name }} R/o {{r p.address }}. (Hereinafter called the party of the second part). Active Partner"
        "{% endfor %}"
    )
    
    _add_para(doc,
        "WHEREAS both the above parties have been decided to carrying on the Business of Pharmaceutical, veterinary and sanitary preparation, dietetic substances adapted for medical use, food for babies. Plaster, Materials for dressing materials for stoping teeth, dental wax, disinfectants preparation for destroying vermin, fungicide’s, herbicide under the name and style of M/s {{r firm_name }} on the following terms and conditions: -"
    )
    _add_para(doc, "NOW THIS DEED OF PARTNERSHIP WITNESSETH AS FOLLOWS: -")
    _add_para(doc,
        "That the business of partnership shall be carried on under the name and styles of M/s {{r firm_name }} Situated at {{r firm_address }}."
    )
    _add_para(doc,
        "The partners with their mutual consent and determination may also start business under any other name and style and also at any other place as mutually decided by the partner."
    )
    _add_para(doc,
        "That the business of the partnership firm shall be of carrying on the Business of pharmaceutical, veterinary and sanitary preparation, dietetic substances adapted for medical use, food for babies. Plaster, Materials for dressing materials for stoping teeth, dental wax, disinfectants preparation for destroying vermin, fungicides, herbicide. The partners with their mutual consent and determination may also start any other business which they may deem profitable."
    )
    _add_para(doc,
        "That the business of the partnership firm shall be deemed to have commenced w.e.f as shall {{r partnership_start_date }}."
    )
    _add_para(doc, "That the partnership firm shall be at will.")
    _add_para(doc, "That the both partner contribute the capital of the Partnership firm agreed between them.")
    _add_para(doc,
        "The net profit of the partnership firm as per the account maintained by the firm after deducting of all expenses relating to trading activities or business of the partnership including rent. Salaries and other establishment expenses as well as interest and remuneration payable to the partners in accordance with the deed of partnership, year in the following proportion: -"
    )
    _add_para(doc, "The loss, if any, including loss of capital suffered in any year shall also is apportioned in the above proportion.")
    _add_para(doc,
        "Necessary capital as well as further funds required for the purpose of the partnership business shall be contributed or arranged by the partners in such manner as may be mutually agreed upon by and between the partners from the time to time. Interest at the rate of 12% annum or as may be prescribed under section 40 (B) (iv) of the income tax Act, 1961 or any other applicable provision as may be in force in income Tax assessment of the partners on the amount standing to the credit of the amount of the partners such interest shall be calculated and credited to the account of each partners at the close of the accounting year."
    )
    _add_para(doc,
        "All the parties of the partnership have agreed to keep themselves actively engaged in conduction the affairs of the business of the partnership firm, as working partners. It is hereby agreed that in consideration of all the parties working in the partnership, will be entitled to remuneration."
    )
    _add_para(doc,
        "The remuneration payable to the above said working partner shall be computed in the manner laid down in explanation 3 to section 40 (B) of the income tax act, 1961 or any other applicable provision as may be in force in the income tax assessment of the partnership firm for the relevant accounting year. Such remuneration shall be calculated at the close of the accounting year and shall be credited to the account of each working partner. The working partner shall be entitled to withdraw out of remuneration for their personal needs from time to time. The partners shall be entitled to increase or reduce the above remuneration and may agree to pay remuneration to other working partners or partners as the case may be. The parties hereto may also agree to revise the mode of calculating the above said remuneration as may be agreed to by the between the partners from time to time."
    )
    _add_para(doc, "That the accounting year of the firm shall be 31st March of every year.")
    _add_para(doc, "That once the balance sheet and profit and loss account prepared, checked and signed by all the partners and the same cannot be questioned by any of the partners thereafter.")
    _add_para(doc, "That the partnership firms open an account with any bank as the both partners here to may mutually agree shall be operated by.")
    _add_para(doc, "That the partners may be mutual consent introduce any other person in to partnership on such terms and conditions the existing partners may decide.")
    _add_para(doc,
        "That it will be open to any partner to retire from the partnership at any time after giving three months’ notice in writing, but will be liable to the partnership, according to his share for the firms, liabilities, if any as on the date of his expiry of his notice."
    )
    _add_para(doc,
        "That the death, insolvency, or retirement of the partner will not have the effect of disclosing the partnership so far as other partners are concerned. In the case of death, his legal heirs may if they so close, come in as partners subject to the terms and conditions thereof, by a notice, in writing given within three months of the death of the firm, in absence of such notice it will be taken that the legal heirs do not want to join the partnership in place of the deceased partner."
    )
    _add_para(doc, "That in the matters not hereby specifically agreed to the partnership will be governed by the provisions of the Indian Partnership Act 1932.")
    _add_para(doc,
        "In the event of any dispute between the partners with regard to anything Related to the partnership business, the matter should be refereed to Arbitration under the provision of the Indian Arbitration Act, 1932. "
    )
    _add_para(doc, "In WITNESS WHEREOF the parties here into have set their respective hands and seals, to these presents the day, month and year above written.")
    _add_para(doc, "WITNESSES")
    
    _add_para(doc,
        "\t\t\t\t\t\t{{r prop_name }}\n"
        "\t\t\t\t\t\t(Party of the First Part)\n"
        "{% for p in partners_data %}"
        "\t\t\t\t\t\t{{r p.name }}\n"
        "\t\t\t\t\t\t(Party of the Second Part)\n"
        "{% endfor %}"
    )

'''

pattern = r'(# ── Registry: filename → builder function ───────────────────────────────)'
content = re.sub(pattern, partner_templates + r'\n\1', content)

new_file_map_update = """    "AFFIDAVIT (Partner).docx":             _template_affidavit_partner,
    "Partner WORKING REPORT.docx":          _template_partner_working_report,
    "Partnership Deed.docx":                _template_partnership_deed,"""
content = content.replace('"AFFIDAVIT (prop).docx":                _template_affidavit_prop,', 
                          f'"AFFIDAVIT (prop).docx":                _template_affidavit_prop,\n{new_file_map_update}')

addr_change_map_update = """    "AFFIDAVIT (Partner).docx":             _template_affidavit_partner,
    "Partner WORKING REPORT.docx":          _template_partner_working_report,
    "Partnership Deed.docx":                _template_partnership_deed,"""
content = content.replace('"AFFIDAVIT (prop).docx":                _template_addr_affidavit_prop,', 
                          f'"AFFIDAVIT (prop).docx":                _template_addr_affidavit_prop,\n{addr_change_map_update}')

with open("create_templates.py", "w") as f:
    f.write(content)
