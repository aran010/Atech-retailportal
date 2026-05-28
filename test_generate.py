"""
test_generate.py
────────────────
Fill sample data and generate the ZIP to verify all 9 templates render.
"""

import os
import sys
import zipfile
from datetime import date

# Ensure we can import from the project
sys.path.insert(0, os.path.dirname(__file__))
from app import generate_documents

SAMPLE_CONTEXT = {
    # ── Proprietor ──────────────────────────────────────────
    "entity_val": "Director",
    "auth_signatory": True,
    "directors_data": [
        {"name": "Director One", "relation": "S/o", "father_name": "Father One", "address": "Address One"},
        {"name": "Director Two", "relation": "D/o", "father_name": "Father Two", "address": "Address Two"}
    ],
    "property_ownership": "Owned",
    "prop_name": "Himanshu Kumar",
    "prop_relation": "S/o",
    "prop_father_name": "Kashee Prasad",
    "prop_address": "House No. 445, Sector-21C, Faridabad, Haryana - 121001",
    "prop_phone": "9876543210",

    # ── Firm ────────────────────────────────────────────────
    "firm_name": "Pradhan Mantri Bhartiya Janaushadhi Kendra",
    "firm_address": "Shop No. 73, Ground Floor, Sector-21C, Faridabad, Haryana - 121001",

    # ── Registered Pharmacist ───────────────────────────────
    "rp_name": "Parveen Kumar",
    "rp_relation": "S/o",
    "rp_father_name": "Shiv Charan",
    "rp_address": "Village Kondal, Tehsil Hathin, District Palwal, Haryana - 121102",
    "rp_salary": "18,000",
    "rp_salary_words": "Eighteen Thousand",
    "rp_joining_date": "01-05-2026",
    "rp_reg_number": "24756",
    "rp_reg_date": "15-06-2020",
    "rp_reg_valid_upto": "14-06-2025",
    "rp_pharmacy_council": "Haryana State Pharmacy Council",
    "rp_qualification": "Bachelor in Pharmacy",
    "rp_college": "BS Anangpuria Institute of Pharmacy, Faridabad",
    "rp_phone": "8765432109",
    "rp_prev_firm_name": "Ankar Life Care LLP",
    "rp_prev_firm_address": "Shop G-14, Varun Tower, NIT-5, Faridabad",
    "rp_resign_date": "20-04-2026",
    
    "pharmacists_data": [
        {
            "name": "Parveen Kumar",
            "relation": "S/o",
            "father_name": "Shiv Charan",
            "address": "Village Kondal, Tehsil Hathin",
            "salary": "18,000",
            "joining_date": "01-05-2026",
            "reg_no": "24756",
            "reg_date": "15-06-2020",
            "reg_valid_upto": "14-06-2025"
        },
        {
            "name": "Aakriti Singh",
            "relation": "D/o",
            "father_name": "Vedpal",
            "address": "Dayalpur",
            "salary": "18,000",
            "joining_date": "01-04-2026",
            "reg_no": "61584",
            "reg_date": "10-02-2025",
            "reg_valid_upto": "31-12-2029"
        }
    ],

    # ── Rent Agreement ──────────────────────────────────────
    "landlord_name": "Jyoti Chawla",
    "landlord_relation": "W/o",
    "landlord_relative_name": "Ashok Chawla",
    "landlord_address": "House No. 1224, Sector-21C, Faridabad, Haryana - 121001",
    "shop_address": "Shop No. 73, Ground Floor, Sector-21C, Faridabad, Haryana",
    "rent_amount": "27,000",
    "rent_amount_words": "Twenty Seven Thousand",
    "lease_months": "11",
    "lease_months_words": "Eleven",
    "rent_start_date": "01-05-2026",
    "rent_agreement_date": "01-05-2026",
    "neighbor_right": "Flower Aura Shop",
    "neighbor_left": "Creative Digital Printing Shop",
    "neighbor_front": "Parking Area / Main Road",
    "neighbor_back": "Vacant Land",

    # ── AC Receipt ──────────────────────────────────────────
    "ac_seller_name": "Om Prakash",
    "ac_seller_relation": "through its Prop M/s Life Ok Pharmacy",
    "ac_seller_address": "Shop No. 06, Milhad Colony, Faridabad",
    "ac_amount": "15,000",
    "ac_amount_words": "Fifteen Thousand",
    "ac_make": "Thomson",
    "ac_details": "Capacity 1.5 Tone",

    # ── Camera Receipt ──────────────────────────────────────
    "cam_seller_name": "Jyoti",
    "cam_seller_relation": "W/o Sh. Anil",
    "cam_seller_address": "Village Kondal, Tehsil Hathin, District Palwal",
    "cam_amount": "10,000",
    "cam_amount_words": "Ten Thousand",
    "cam_make": "Hikvision 4-Channel DVR",

    # ── Inverter Receipt ────────────────────────────────────
    "inv_seller_name": "Durgesh",
    "inv_seller_relation": "S/o Sh. Harbu Lal",
    "inv_seller_address": "House No. 1224/1, Mathura Road, Faridabad",
    "inv_amount": "5,000",
    "inv_amount_words": "Five Thousand",
    "inv_make": "Microtek 800VA",

    # ── Refrigerator Receipt ────────────────────────────────
    "fridge_seller_name": "Jyoti",
    "fridge_seller_relation": "W/o Sh. Anil",
    "fridge_seller_address": "Village Kondal, Tehsil Hathin, District Palwal",
    "fridge_amount": "10,000",
    "fridge_amount_words": "Ten Thousand",
    "fridge_make": "Godrej",
    "fridge_details": "Color Sky Blue, 210 Liters",

    # ── Work History ────────────────────────────────────────
    "prop_work_history": [
        {"sr_no": "1", "time_period": "Jan 2023 - Dec 2023", "occupation": "Business - Grocery Store", "remarks": "Self-employed"},
        {"sr_no": "2", "time_period": "Jan 2024 - Dec 2024", "occupation": "Business - General Store", "remarks": "Self-employed"},
        {"sr_no": "3", "time_period": "Jan 2025 - Present", "occupation": "Prop - Janaushadhi Kendra", "remarks": "Current"},
    ],
    "rp_work_history": [
        {"sr_no": "1", "time_period": "Jul 2020 - Jun 2022", "occupation": "RP - Ankar Life Care LLP", "remarks": "Full-time"},
        {"sr_no": "2", "time_period": "Jul 2022 - Apr 2026", "occupation": "RP - MedPlus Pharmacy", "remarks": "Full-time"},
        {"sr_no": "3", "time_period": "May 2026 - Present", "occupation": "RP - Janaushadhi Kendra", "remarks": "Current"},
    ],

    # ── Common ──────────────────────────────────────────────
    "current_date": date.today().strftime("%d-%m-%Y"),
}


if __name__ == "__main__":
    print("Generating documents with sample data...\n")

    zip_bytes, rendered_names = generate_documents(SAMPLE_CONTEXT)

    # Save the ZIP
    out_path = os.path.join(os.path.dirname(__file__), "New_Retail_File_Himanshu_Kumar.zip")
    with open(out_path, "wb") as f:
        f.write(zip_bytes)

    print(f"ZIP saved: {out_path}")
    print(f"Size: {len(zip_bytes):,} bytes\n")

    # List contents
    with zipfile.ZipFile(out_path, "r") as zf:
        print(f"Archive contains {len(zf.namelist())} files:")
        for i, name in enumerate(zf.namelist(), 1):
            info = zf.getinfo(name)
            print(f"  {i}. {name}  ({info.file_size:,} bytes)")

    print("\nAll documents generated successfully.")
