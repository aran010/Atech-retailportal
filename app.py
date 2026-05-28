"""
Aran Technologies - Retail Document Portal  v3.1
=================================================
Futuristic minimalist UI with sidebar navigation.
Zero emojis. Clean lines. Smooth UX.

Usage:
    streamlit run app.py
"""

import io
import os
import re
import zipfile
from datetime import date

import streamlit as st
from docxtpl import DocxTemplate, RichText

# ── Constants ────────────────────────────────────────────────────────────

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
ADDR_TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates_address_change")
MIN_DATE = date(1950, 1, 1)
MAX_DATE = date(2100, 12, 31)

# ── Page Configuration ───────────────────────────────────────────────────

st.set_page_config(
    page_title="Drug File Management System",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────

st.markdown(
    """
        <style>
    /* ── 2026 Modern UI CSS ──────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');

    /* ── CSS Variables ─────────────────────────────────────── */
    :root {
        --brand: #4f5bd5;
        --brand-light: #F59E0B;
        --brand-secondary: #9333ea;
        --bg-grad-1: #f8fafc;
        --bg-grad-2: #e2e8f0;
        --text-primary: #0f172a;
        --text-secondary: #475569;
        --text-muted: #94a3b8;
        --border: rgba(255, 255, 255, 0.5);
        --border-hover: rgba(79, 91, 213, 0.4);
        --glass-bg: rgba(255, 255, 255, 0.65);
        --glass-border: rgba(255, 255, 255, 0.8);
        --glass-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        --radius-sm: 8px;
        --radius-md: 16px;
        --radius-lg: 24px;
        --shadow-hover: 0 20px 40px -10px rgba(79, 91, 213, 0.2);
    }

    /* ── Typography ────────────────────────── */
    .stApp,
    .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .stMarkdown h4, .stMarkdown li,
    .stTextInput label, .stTextArea label,
    .stSelectbox label, .stDateInput label, .stNumberInput label,
    .stTextInput input, .stTextArea textarea,
    [data-testid="stExpander"] summary p,
    button, div[role="radiogroup"] > label > div:last-child {
        font-family: 'Outfit', 'Inter', sans-serif !important;
    }
    
    /* ── Hide Streamlit Cloud Toolbar ──────────────── */
    [data-testid="stToolbar"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* ── Static Background Layout ──────────────────── */
    [data-testid="stAppViewContainer"], .stApp {
        background: #f6f8fd !important;
    }
    
    .main .block-container {
        max-width: 1200px;
        padding: 2rem 4rem 5rem;
    }

    /* ── Streamlit Overrides ─────────────── */
    [data-testid="stDecoration"] { display: none !important; }
    header[data-testid="stHeader"] { background: transparent !important; backdrop-filter: blur(10px); }

    /* ══════════════════════════════════════════════════════════
       GLASSMORPHISM SIDEBAR
       ══════════════════════════════════════════════════════════ */
    [data-testid="stSidebar"] {
        min-width: 300px !important;
        max-width: 320px !important;
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-right: 1px solid var(--glass-border) !important;
        box-shadow: var(--glass-shadow);
    }
    [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        padding-top: 0;
    }
    
    /* Brand Logo Area */
    .sidebar-brand-strip {
        padding: 2.5rem 1.5rem 1.5rem;
        text-align: center;
        background: transparent;
        margin-bottom: 1rem;
    }
    .sidebar-brand-strip h2 {
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--brand), var(--brand-secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.02em;
    }

    /* ── Sidebar Navigation Labels & Radios ─────────────────────────── */
    .sidebar-nav-label {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        color: var(--text-muted);
        margin: 1.5rem 1.5rem 0.5rem;
    }
    
    /* Radio Button Styling */
    div[role="radiogroup"] > label {
        background: rgba(255, 255, 255, 0.5);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-sm);
        padding: 0.8rem 1rem !important;
        margin-bottom: 0.5rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    div[role="radiogroup"] > label:hover {
        background: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    div[role="radiogroup"] > label[data-checked="true"] {
        background: white;
        border-color: #10b981;
        box-shadow: 0 0 0 1px #10b981, 0 4px 12px rgba(16, 185, 129, 0.15);
    }
    div[role="radiogroup"] > label > div:first-child {
        /* Circle is now visible */
        margin-top: 2px;
    }
    div[role="radiogroup"] > label > div:last-child {
        margin-left: 0 !important;
        font-weight: 600 !important;
        color: var(--text-primary) !important;
        font-size: 0.95rem !important;
    }
    div[role="radiogroup"] > label[data-checked="true"] > div:last-child {
        color: #10b981 !important;
    }
    div[role="radiogroup"] > label[data-checked="true"] svg {
        fill: #10b981 !important;
    }

    /* ══════════════════════════════════════════════════════════
       MAIN HEADER
       ══════════════════════════════════════════════════════════ */
    .portal-header-wrapper {
        background: var(--glass-bg);
        backdrop-filter: blur(12px);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-lg);
        padding: 2.5rem 3rem 2rem;
        margin: 0 0 2.5rem;
        box-shadow: var(--glass-shadow);
        text-align: center;
        animation: slideDown 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    @keyframes slideDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .portal-header h1 {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin: 0;
        color: var(--text-primary);
    }
    .portal-header .accent {
        color: var(--brand-light);
    }
    .portal-header .rule {
        display: block;
        width: 80px;
        height: 4px;
        background: linear-gradient(90deg, var(--brand), var(--brand-secondary), var(--brand-light));
        background-size: 200% 200%;
        animation: gradientBG 3s ease infinite;
        margin: 1.2rem auto;
        border-radius: 4px;
    }
    .portal-header .subtitle {
        font-size: 1.1rem;
        font-weight: 400;
        color: var(--text-secondary);
    }

    /* ── Meta Pills ──────────────────────────────────────────── */
    .meta-bar {
        display: flex;
        justify-content: center;
        gap: 1.2rem;
        margin-top: 1.5rem;
    }
    .meta-pill {
        background: rgba(255, 255, 255, 0.8);
        border: 1px solid var(--glass-border);
        border-radius: 30px;
        padding: 0.5rem 1.2rem;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--text-muted);
        box-shadow: 0 2px 10px rgba(0,0,0,0.02);
        transition: transform 0.2s ease;
    }
    .meta-pill:hover {
        transform: translateY(-2px);
    }
    .meta-pill span {
        color: var(--brand);
        font-weight: 800;
        margin-left: 0.4rem;
    }

    /* ══════════════════════════════════════════════════════════
       GLASS CARDS & EXPANDERS
       ══════════════════════════════════════════════════════════ */
    [data-testid="stExpander"] {
        background: var(--glass-bg) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-lg) !important;
        box-shadow: var(--glass-shadow) !important;
        margin-bottom: 1.5rem;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    [data-testid="stExpander"]:hover {
        transform: translateY(-4px) !important;
        box-shadow: var(--shadow-hover) !important;
        border-color: rgba(255,255,255,1) !important;
    }
    [data-testid="stExpander"] summary {
        padding: 1.2rem 1.8rem !important;
    }
    [data-testid="stExpander"] summary p {
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        color: var(--text-primary) !important;
    }
    
    [data-testid="stForm"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
    }

    /* ── Section Titles ─────────────────────────────────────── */
    .section-title {
        font-size: 1rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--brand);
        margin: 2.5rem 0 1.2rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .section-title::after {
        content: '';
        height: 2px;
        flex: 1;
        background: linear-gradient(90deg, var(--brand) 0%, transparent 100%);
        opacity: 0.2;
    }

    /* ══════════════════════════════════════════════════════════
       PREMIUM INPUT FIELDS
       ══════════════════════════════════════════════════════════ */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {
        border-radius: var(--radius-sm) !important;
        border: 2px solid rgba(255,255,255,0.8) !important;
        background: #ffffff !important;
        transition: all 0.3s ease !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        color: var(--text-primary) !important;
        padding: 0.7rem 1rem !important;
    }
    
    /* Selectbox specific (avoid padding breaking internal input layout) */
    .stSelectbox > div > div {
        border-radius: var(--radius-sm) !important;
        border: 2px solid rgba(255,255,255,0.8) !important;
        background: #ffffff !important;
        transition: all 0.3s ease !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
    }
    
    /* Force selectbox inner text to be visible */
    .stSelectbox div[data-baseweb="select"] span,
    .stSelectbox div[data-baseweb="select"] input {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div:focus-within,
    .stNumberInput > div > div > input:focus {
        border-color: var(--brand) !important;
        background: white !important;
        box-shadow: 0 0 0 4px rgba(79, 91, 213, 0.15) !important;
        transform: translateY(-1px);
    }
    
    .stTextInput label, .stTextArea label,
    .stSelectbox label, .stDateInput label, .stNumberInput label {
        font-size: 0.85rem !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        color: var(--text-primary) !important;
        margin-bottom: 0.4rem !important;
    }
    .req { color: #f43f5e; font-weight: 800; }

    /* ══════════════════════════════════════════════════════════
       ANIMATED BUTTONS
       ══════════════════════════════════════════════════════════ */
    /* Form Submit Button */
    [data-testid="stForm"] button[type="submit"] {
        width: 100%;
        border-radius: var(--radius-lg) !important;
        padding: 1.2rem 2rem !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        letter-spacing: 0.15em !important;
        text-transform: uppercase;
        margin-top: 1.5rem;
        background: linear-gradient(135deg, var(--brand), var(--brand-secondary), var(--brand-light)) !important;
        background-size: 200% 200% !important;
        animation: gradientBG 4s ease infinite !important;
        border: none !important;
        color: #fff !important;
        box-shadow: 0 10px 30px rgba(79,91,213,0.3) !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    }
    [data-testid="stForm"] button[type="submit"]:hover {
        transform: translateY(-4px) scale(1.02) !important;
        box-shadow: 0 20px 40px rgba(79,91,213,0.4) !important;
    }
    [data-testid="stForm"] button[type="submit"]:active {
        transform: translateY(0) scale(0.98) !important;
    }

    /* Regular / Add Buttons */
    .main .stButton > button {
        border-radius: var(--radius-sm) !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border: 2px solid var(--brand) !important;
        background: transparent !important;
        color: var(--brand) !important;
        transition: all 0.3s ease !important;
    }
    .main .stButton > button:hover {
        background: var(--brand) !important;
        color: white !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(79,91,213,0.2) !important;
    }

    /* ══════════════════════════════════════════════════════════
       SUCCESS RESULT CARD
       ══════════════════════════════════════════════════════════ */
    .result-card {
        background: rgba(255,255,255,0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(16,185,129,0.3);
        border-radius: var(--radius-lg);
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(16,185,129,0.1);
        text-align: center;
        animation: slideUp 0.5s cubic-bezier(0.16, 1, 0.3, 1);
    }
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .result-card h4 {
        font-size: 1.5rem;
        font-weight: 800;
        color: #059669;
        margin: 0 0 0.5rem;
    }
    .result-card p {
        color: var(--text-secondary);
        font-size: 1.1rem;
        font-weight: 500;
    }
    
    /* ── Download Button ───────────────────────────────────── */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981, #059669) !important;
        border: none !important;
        color: white !important;
        font-weight: 800 !important;
        border-radius: var(--radius-md) !important;
        padding: 1rem !important;
        box-shadow: 0 10px 20px rgba(16,185,129,0.3) !important;
        transition: all 0.3s ease !important;
    }
    .stDownloadButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 15px 30px rgba(16,185,129,0.4) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── Helper Functions ─────────────────────────────────────────────────────


def get_template_files(template_dir: str = TEMPLATES_DIR) -> list[str]:
    """Return sorted list of .docx files in the given templates directory."""
    if not os.path.isdir(template_dir):
        return []
    return sorted(f for f in os.listdir(template_dir) if f.lower().endswith(".docx"))


def sanitize_filename(name: str) -> str:
    """Remove non-alphanumeric characters (except underscores/hyphens)."""
    return re.sub(r"[^\w\s-]", "", name).strip().replace(" ", "_")


def fmt_date(d) -> str:
    """Format a date object to dd-mm-yyyy string."""
    if d is None:
        return ""
    if isinstance(d, date):
        return d.strftime("%d-%m-%Y")
    return str(d)


def parse_amount(s: str) -> int:
    """Extract numeric value from strings like '18,000', '18000/-', 'Rs. 27000'."""
    cleaned = re.sub(r"[^\d]", "", s)
    return int(cleaned) if cleaned else 0


def num_to_words(n: int) -> str:
    """Convert an integer to Indian English words (supports up to Crores)."""
    if n == 0:
        return "Zero"

    ones = [
        "", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight",
        "Nine", "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen",
        "Sixteen", "Seventeen", "Eighteen", "Nineteen",
    ]
    tens = [
        "", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy",
        "Eighty", "Ninety",
    ]

    def _two(x):
        if x < 20:
            return ones[x]
        return tens[x // 10] + (" " + ones[x % 10] if x % 10 else "")

    def _three(x):
        if x >= 100:
            return ones[x // 100] + " Hundred" + (" " + _two(x % 100) if x % 100 else "")
        return _two(x)

    parts: list[str] = []
    if n >= 10_000_000:
        parts.append(_three(n // 10_000_000) + " Crore")
        n %= 10_000_000
    if n >= 100_000:
        parts.append(_two(n // 100_000) + " Lakh")
        n %= 100_000
    if n >= 1_000:
        parts.append(_two(n // 1_000) + " Thousand")
        n %= 1_000
    if n > 0:
        parts.append(_three(n))
    return " ".join(parts)


def amount_to_words(raw: str) -> str:
    """Parse an amount string and return Indian English words."""
    val = parse_amount(raw)
    return num_to_words(val) if val else ""


PHARMACY_COUNCIL = "Haryana State Pharmacy Council"


def boldify_context(context: dict) -> dict:
    """
    Wrap every user-input string value in RichText(bold=True) so that
    filled-in data appears bold in the generated Word documents.
    Lists of dicts (work history) are processed recursively.
    """
    bold = {}
    for key, value in context.items():
        if isinstance(value, str):
            bold[key] = RichText(value, bold=True) if value else RichText("")
        elif isinstance(value, list):
            bold[key] = [
                {
                    k: RichText(v, bold=True) if isinstance(v, str) and v else v
                    for k, v in item.items()
                }
                if isinstance(item, dict)
                else item
                for item in value
            ]
        else:
            bold[key] = value
    return bold


def generate_documents(context: dict, template_dir: str = TEMPLATES_DIR) -> tuple[bytes, list[str]]:
    """
    Render every .docx template with *context*, return (zip_bytes, file_list).
    All string values are auto-bolded via RichText. Fully in-memory via BytesIO.
    """
    bold_context = boldify_context(context)
    template_files = get_template_files(template_dir)
    zip_buffer = io.BytesIO()
    rendered_names: list[str] = []

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for tpl_name in template_files:
            tpl_path = os.path.join(template_dir, tpl_name)
            tpl = DocxTemplate(tpl_path)
            tpl.render(bold_context)

            doc_buffer = io.BytesIO()
            tpl.save(doc_buffer)
            doc_buffer.seek(0)

            out_name = f"Filled_{tpl_name}"
            zf.writestr(out_name, doc_buffer.read())
            rendered_names.append(out_name)

    zip_buffer.seek(0)
    return zip_buffer.getvalue(), rendered_names


def reset_session():
    """Clear all session state to start a fresh file."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]


# ── Session State Initialisation ─────────────────────────────────────────

if "prop_work_history" not in st.session_state:
    st.session_state.prop_work_history = [
        {"sr_no": "1", "time_period": "", "occupation": "", "remarks": ""}
    ]

if "rp_work_history" not in st.session_state:
    st.session_state.rp_work_history = [
        {"sr_no": "1", "time_period": "", "occupation": "", "remarks": ""}
    ]

if "action_type" not in st.session_state:
    st.session_state.action_type = "new_file"

if "entity_type" not in st.session_state:
    st.session_state.entity_type = "proprietor"

if "num_entities" not in st.session_state:
    st.session_state.num_entities = 1

if "num_pharmacists" not in st.session_state:
    st.session_state.num_pharmacists = 1


# ── Work History Renderer ────────────────────────────────────────────────


def render_work_history(prefix: str, state_key: str):
    """Render a dynamic work-history table with add/remove rows."""
    if st.button("Add Entry", key=f"{prefix}_add", use_container_width=True):
        next_sr = str(len(st.session_state[state_key]) + 1)
        st.session_state[state_key].append(
            {"sr_no": next_sr, "time_period": "", "occupation": "", "remarks": ""}
        )
        st.rerun()

    for idx, row in enumerate(st.session_state[state_key]):
        vis = "visible" if idx == 0 else "collapsed"
        c1, c2, c3, c4, c5 = st.columns([0.5, 2.2, 3, 2, 0.6])
        with c1:
            st.session_state[state_key][idx]["sr_no"] = st.text_input(
                "Sr.", value=row["sr_no"], key=f"{prefix}_sr_{idx}",
                label_visibility=vis,
            )
        with c2:
            st.session_state[state_key][idx]["time_period"] = st.text_input(
                "Time Period", value=row["time_period"], key=f"{prefix}_tp_{idx}",
                label_visibility=vis,
            )
        with c3:
            st.session_state[state_key][idx]["occupation"] = st.text_input(
                "Working / Occupation", value=row["occupation"],
                key=f"{prefix}_occ_{idx}", label_visibility=vis,
            )
        with c4:
            st.session_state[state_key][idx]["remarks"] = st.text_input(
                "Remarks", value=row["remarks"], key=f"{prefix}_rem_{idx}",
                label_visibility=vis,
            )
        with c5:
            if idx == 0:
                st.markdown(
                    "<div style='height:28px'></div>", unsafe_allow_html=True
                )
            if len(st.session_state[state_key]) > 1:
                if st.button("X", key=f"{prefix}_del_{idx}"):
                    st.session_state[state_key].pop(idx)
                    st.rerun()


# ── Main Application ─────────────────────────────────────────────────────


def main():
    # ────────────────────────────────────────────────────────────
    # SIDEBAR
    # ────────────────────────────────────────────────────────────
    with st.sidebar:
        # Brand strip
        st.markdown(
            '<div class="sidebar-brand-strip">'
            '<h2>DFMS</h2>'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown('<div class="sidebar-nav-label">Action</div>', unsafe_allow_html=True)
        action_val = st.radio("Action", ["New File", "Address Change"], label_visibility="collapsed")
        
        st.markdown('<div class="sidebar-nav-label">Entity Type</div>', unsafe_allow_html=True)
        entity_val = st.radio("Entity Type", ["Proprietor", "Partner", "Director"], label_visibility="collapsed")
        
        action_type = "new_file" if action_val == "New File" else "address_change"
        entity_type = entity_val.lower()
        
        if st.session_state.action_type != action_type or st.session_state.entity_type != entity_type:
            st.session_state.action_type = action_type
            st.session_state.entity_type = entity_type

    # Determine which template directory to use
    tpl_dir = ADDR_TEMPLATES_DIR if action_type == "address_change" else TEMPLATES_DIR
    templates = get_template_files(tpl_dir)

    # ────────────────────────────────────────────────────────────
    # MAIN CONTENT
    # ────────────────────────────────────────────────────────────

    # ── Header & Meta Bar ───────────────────────────────────────
    type_label = f"{action_val.upper()} ({entity_val.upper()})"
    st.markdown(
        f"""
        <div class="portal-header-wrapper">
            <div class="portal-header">
                <h1>Drug File Management System</h1>
                <span class="rule"></span>
                <p class="subtitle">Automated document generation for new retail drug file processing</p>
            </div>
            <div class="meta-bar">
                <div class="meta-pill">Mode  <span>{type_label}</span></div>
                <div class="meta-pill">Templates  <span>{len(templates)}</span></div>
                <div class="meta-pill">Date  <span>{date.today().strftime("%d %b %Y")}</span></div>
                <div class="meta-pill">Output  <span>ZIP</span></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Pre-flight ──────────────────────────────────────────────
    if not templates:
        st.error(
            f"No .docx templates found in {TEMPLATES_DIR}/. "
            "Run  python create_templates.py  first."
        )
        st.stop()

    # ────────────────────────────────────────────────────────────
    # WORK HISTORY  (outside form — requires dynamic buttons)
    # ────────────────────────────────────────────────────────────

    st.markdown(
        '<div class="section-title">Work History</div>', unsafe_allow_html=True
    )

    if entity_type in ["partner", "director"]:
        num_entities = st.session_state.get("num_entities", 1)
        entity_label = "Partner" if entity_type == "partner" else "Director"
        for i in range(num_entities):
            state_key = f"{entity_type}_work_history_{i}"
            if state_key not in st.session_state:
                st.session_state[state_key] = [
                    {"sr_no": "1", "time_period": "", "occupation": "", "remarks": ""}
                ]
            with st.expander(f"{entity_label} {i+1} Work History", expanded=False):
                render_work_history(f"e_{i}", state_key)
    else:
        with st.expander("Proprietor Work History", expanded=False):
            render_work_history("prop", "prop_work_history")

    num_pharmacists = st.session_state.get("num_pharmacists", 1)
    for i in range(num_pharmacists):
        state_key = f"rp_work_history_{i}"
        if state_key not in st.session_state:
            st.session_state[state_key] = [
                {"sr_no": "1", "time_period": "", "occupation": "", "remarks": ""}
            ]
        with st.expander(f"Registered Pharmacist {i+1} Work History", expanded=False):
            render_work_history(f"rp_{i}", state_key)

    # ────────────────────────────────────────────────────────────
    # MAIN FORM
    # ────────────────────────────────────────────────────────────

    st.markdown(
        '<div class="section-title">Client Details</div>', unsafe_allow_html=True
    )

    if entity_type in ["partner", "director"]:
        entity_label = "Partners" if entity_type == "partner" else "Directors"
        st.number_input(f"Number of {entity_label} (Press Enter to update form)", min_value=1, value=1, step=1, key="num_entities")
        
    st.number_input("Number of Pharmacists (Press Enter to update form)", min_value=1, value=1, step=1, key="num_pharmacists")

    with st.form("document_form", clear_on_submit=False):

        # ── Document Date ───────────────────────────────────────
        col_dt, col_blank = st.columns([1, 2])
        with col_dt:
            doc_date = st.date_input(
                "Document Date", value=date.today(),
                min_value=MIN_DATE, max_value=MAX_DATE,
            )

        # ── Dynamic Entity & Firm ───────────────────────────────────
        if entity_type in ["partner", "director"]:
            entity_label_s = "Partner" if entity_type == "partner" else "Director"
            entity_label_pl = "Partners" if entity_type == "partner" else "Directors"
            
            with st.expander(f"{entity_label_pl} and Firm Details", expanded=True):
                st.markdown('<div class="section-title" style="margin-top:0;">License Type</div>', unsafe_allow_html=True)
                license_type = st.radio("License Type", ["New Retail", "New Wholesale", "New Retail/Wholesale"], index=0, horizontal=True, label_visibility="collapsed", key="lic_type_multi")
                firm_name = st.text_input("Firm Name :red[*]")
                firm_address = st.text_area("Firm / Shop Address :red[*]", height=80)
                st.markdown("---")
                
                entities_data = []
                num_entities = st.session_state.get("num_entities", 1)
                for i in range(num_entities):
                    st.markdown(f"**{entity_label_s} {i+1}**")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        p_name = st.text_input(f"{entity_label_s} Name :red[*]", key=f"e_name_{i}")
                        c_rel, c_father = st.columns(2)
                        with c_rel:
                            p_rel = st.selectbox("Relation", options=["S/o", "D/o", "W/o"], index=0, key=f"e_rel_{i}")
                        with c_father:
                            p_father = st.text_input("Father / Relative", key=f"e_father_{i}")
                    with col_b:
                        p_address = st.text_area(f"{entity_label_s} Address :red[*]", height=80, key=f"e_address_{i}")
                        p_phone = st.text_input("Phone", max_chars=10, key=f"e_phone_{i}")
                    
                    entities_data.append({
                        "name": p_name.strip(),
                        "relation": p_rel,
                        "father_name": p_father.strip(),
                        "address": p_address.strip(),
                        "phone": p_phone.strip()
                    })
                    st.markdown("---")
        else:
            with st.expander("Proprietor and Firm Details", expanded=True):
                st.markdown('<div class="section-title" style="margin-top:0;">License Type</div>', unsafe_allow_html=True)
                license_type = st.radio("License Type", ["New Retail", "New Wholesale", "New Retail/Wholesale"], index=0, horizontal=True, label_visibility="collapsed", key="lic_type_single")
                col_a, col_b = st.columns(2)

                with col_a:
                    prop_name = st.text_input("Proprietor Name :red[*]")
                    c_rel, c_father = st.columns(2)
                    with c_rel:
                        prop_relation = st.selectbox("Relation", options=["S/o", "D/o", "W/o"], index=0, key="prop_relation")
                    with c_father:
                        prop_father_name = st.text_input("Father / Relative")
                    prop_address = st.text_area("Proprietor Address :red[*]", height=80)
                    prop_phone = st.text_input("Phone", max_chars=10)

                with col_b:
                    firm_name = st.text_input("Firm Name :red[*]")
                    firm_address = st.text_area("Firm / Shop Address :red[*]", height=80)

        # ── Address Change Fields (shown only for address change) ───
        if action_type == "address_change":
            with st.expander("Address Change Details :red[*]", expanded=True):
                ac_col1, ac_col2 = st.columns(2)
                with ac_col1:
                    old_address = st.text_area(
                        "Old Premises Address :red[*]", height=80,
                    )
                    drug_license_number = st.text_area(
                        "Drug License Number and Validity :red[*]", height=80,
                    )
                with ac_col2:
                    new_address = st.text_area(
                        "New Premises Address :red[*]", height=80,
                    )
                    applying_for = st.text_input(
                        "Applying For",
                        value="Retail Sale Drug License due to change in premises",
                    )

        # ── Registered Pharmacist ───────────────────────────────
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

        # ── Rent Agreement ──────────────────────────────────────
        with st.expander("Rent Agreement"):
            col_g, col_h = st.columns(2)

            with col_g:
                landlord_name = st.text_input(
                    "Landlord Name"
                )
                c_ll_rel, c_ll_f = st.columns(2)
                with c_ll_rel:
                    landlord_relation = st.selectbox(
                        "Relation", options=["S/o", "D/o", "W/o"], index=0,
                        key="landlord_relation",
                    )
                with c_ll_f:
                    landlord_relative_name = st.text_input(
                        "Relative Name", key="ll_rel_name",
                    )
                landlord_address = st.text_area(
                    "Landlord Address", height=80,
                )
                shop_address = st.text_area(
                    "Shop / Premises Address", height=80,
                )

            with col_h:
                rent_amount = st.text_input(
                    "Rent (Rs.)"
                )
                lease_months = st.text_input(
                    "Lease (months)"
                )
                c_rs, c_ra = st.columns(2)
                with c_rs:
                    rent_start_date = st.date_input(
                        "Rent Start Date", value=None,
                        min_value=MIN_DATE, max_value=MAX_DATE,
                        key="rent_start_date",
                    )
                with c_ra:
                    rent_agreement_date = st.date_input(
                        "Agreement Date", value=None,
                        min_value=MIN_DATE, max_value=MAX_DATE,
                        key="rent_agreement_date",
                    )

            # Neighbours
            st.markdown("**Neighbouring Boundaries**")
            cn1, cn2 = st.columns(2)
            with cn1:
                neighbor_right = st.text_input(
                    "Right"
                )
                neighbor_front = st.text_input(
                    "Front"
                )
            with cn2:
                neighbor_left = st.text_input(
                    "Left"
                )
                neighbor_back = st.text_input(
                    "Back"
                )

        # ── Equipment Receipts ──────────────────────────────────
        with st.expander("Equipment Receipts"):

            # — AC —
            st.markdown(
                '<div class="receipt-label">Air Conditioner</div>',
                unsafe_allow_html=True,
            )
            col_i, col_j = st.columns(2)
            with col_i:
                ac_seller_name = st.text_input(
                    "AC Seller Name"
                )
                ac_seller_relation = st.text_input(
                    "Seller Relation / Through",
                    key="ac_rel",
                )
                ac_seller_address = st.text_input(
                    "Seller Address",
                    key="ac_addr",
                )
            with col_j:
                ac_amount = st.text_input(
                    "Amount (Rs.)",
                    key="ac_amt",
                )
                ac_make = st.text_input(
                    "Make / Brand", key="ac_make"
                )
                ac_details = st.text_input(
                    "Details",
                    key="ac_det",
                )

            st.divider()

            # — Camera —
            st.markdown(
                '<div class="receipt-label">CCTV Camera</div>',
                unsafe_allow_html=True,
            )
            col_k, col_l = st.columns(2)
            with col_k:
                cam_seller_name = st.text_input(
                    "Camera Seller Name"
                )
                cam_seller_relation = st.text_input(
                    "Seller Relation", key="cam_rel",
                )
                cam_seller_address = st.text_input(
                    "Seller Address",
                    key="cam_addr",
                )
            with col_l:
                cam_amount = st.text_input(
                    "Amount (Rs.)",
                    key="cam_amt",
                )
                cam_make = st.text_input(
                    "Make / Brand",
                    key="cam_make",
                )

            st.divider()

            # — Inverter —
            st.markdown(
                '<div class="receipt-label">Inverter</div>',
                unsafe_allow_html=True,
            )
            col_m, col_n = st.columns(2)
            with col_m:
                inv_seller_name = st.text_input(
                    "Inverter Seller Name"
                )
                inv_seller_relation = st.text_input(
                    "Seller Relation", key="inv_rel",
                )
                inv_seller_address = st.text_input(
                    "Seller Address",
                    key="inv_addr",
                )
            with col_n:
                inv_amount = st.text_input(
                    "Amount (Rs.)",
                    key="inv_amt",
                )
                inv_make = st.text_input(
                    "Make / Brand",
                    key="inv_make",
                )

            st.divider()

            # — Refrigerator —
            st.markdown(
                '<div class="receipt-label">Refrigerator</div>',
                unsafe_allow_html=True,
            )
            col_o, col_p = st.columns(2)
            with col_o:
                fridge_seller_name = st.text_input(
                    "Fridge Seller Name"
                )
                fridge_seller_relation = st.text_input(
                    "Seller Relation", key="fridge_rel",
                )
                fridge_seller_address = st.text_input(
                    "Seller Address",
                    key="fridge_addr",
                )
            with col_p:
                fridge_amount = st.text_input(
                    "Amount (Rs.)",
                    key="fridge_amt",
                )
                fridge_make = st.text_input(
                    "Make / Brand",
                    key="fridge_make",
                )
                fridge_details = st.text_input(
                    "Details",
                    key="fridge_det",
                )

        # ── Generate Button ─────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("GENERATE DOCUMENTS")

    # ────────────────────────────────────────────────────────────
    # POST-SUBMIT PROCESSING
    # ────────────────────────────────────────────────────────────

    if submitted:
        # Validate key fields
        required = {
            "Firm Name": firm_name,
            "Firm Address": firm_address,
        }
        if pharmacists_data:
            required["Pharmacist 1 Name"] = pharmacists_data[0]["name"]
        if entity_type == "proprietor":
            required["Proprietor Name"] = prop_name
        else:
            entity_label_s = "Partner" if entity_type == "partner" else "Director"
            if entities_data:
                required[f"{entity_label_s} 1 Name"] = entities_data[0]["name"]

        missing = [k for k, v in required.items() if not v.strip()]

        if missing:
            st.warning(
                "Please fill in the following required fields: "
                f"**{', '.join(missing)}**"
            )
            st.stop()

        # Default proprietor values if multi-entity mode
        if entity_type in ["partner", "director"]:
            prop_name = entities_data[0]["name"] if entities_data else ""
            prop_relation = entities_data[0]["relation"] if entities_data else ""
            prop_father_name = entities_data[0]["father_name"] if entities_data else ""
            prop_address = entities_data[0]["address"] if entities_data else ""
            prop_phone = entities_data[0]["phone"] if entities_data else ""

        # Build context dictionary
        context = {
            "license_type": license_type.lower(),
            # Proprietor (used as fallback or for main proprietor)
            "prop_name": prop_name.strip(),
            "prop_relation": prop_relation,
            "prop_father_name": prop_father_name.strip(),
            "prop_address": prop_address.strip(),
            "prop_phone": prop_phone.strip(),
            "partners": entities_data if entity_type == "partner" else [],
            "directors": entities_data if entity_type == "director" else [],
            # Firm
            "firm_name": firm_name.strip(),
            "firm_address": firm_address.strip(),
            # Pharmacists (list for looping)
            "pharmacists": pharmacists_data,
            # Fallback single variables for old templates
            "rp_name": pharmacists_data[0]["name"] if pharmacists_data else "",
            "rp_relation": pharmacists_data[0]["relation"] if pharmacists_data else "",
            "rp_father_name": pharmacists_data[0]["father_name"] if pharmacists_data else "",
            "rp_address": pharmacists_data[0]["address"] if pharmacists_data else "",
            "rp_salary": pharmacists_data[0]["salary"] if pharmacists_data else "",
            "rp_salary_words": amount_to_words(pharmacists_data[0]["salary"]) if pharmacists_data else "",
            "rp_joining_date": pharmacists_data[0]["joining_date"] if pharmacists_data else "",
            "rp_reg_number": pharmacists_data[0]["reg_no"] if pharmacists_data else "",
            "rp_reg_date": pharmacists_data[0]["reg_date"] if pharmacists_data else "",
            "rp_reg_valid_upto": pharmacists_data[0]["reg_valid_upto"] if pharmacists_data else "",
            "rp_pharmacy_council": PHARMACY_COUNCIL,
            "rp_qualification": pharmacists_data[0]["qualification"] if pharmacists_data else "",
            "rp_college": pharmacists_data[0]["college"] if pharmacists_data else "",
            "rp_phone": pharmacists_data[0]["phone"] if pharmacists_data else "",
            "rp_prev_firm_name": pharmacists_data[0]["prev_firm_name"] if pharmacists_data else "",
            "rp_prev_firm_address": pharmacists_data[0]["prev_firm_address"] if pharmacists_data else "",
            "rp_resign_date": pharmacists_data[0]["resign_date"] if pharmacists_data else "",
            "rp_work_history": st.session_state.get("rp_work_history_0", []),
            # Rent Agreement
            "landlord_name": landlord_name.strip(),
            "landlord_relation": landlord_relation,
            "landlord_relative_name": landlord_relative_name.strip(),
            "landlord_address": landlord_address.strip(),
            "shop_address": shop_address.strip(),
            "rent_amount": rent_amount.strip(),
            "rent_amount_words": amount_to_words(rent_amount),
            "lease_months": lease_months.strip(),
            "lease_months_words": amount_to_words(lease_months),
            "rent_start_date": fmt_date(rent_start_date),
            "rent_agreement_date": fmt_date(rent_agreement_date),
            "neighbor_right": neighbor_right.strip(),
            "neighbor_left": neighbor_left.strip(),
            "neighbor_front": neighbor_front.strip(),
            "neighbor_back": neighbor_back.strip(),
            # AC Receipt
            "ac_seller_name": ac_seller_name.strip(),
            "ac_seller_relation": ac_seller_relation.strip(),
            "ac_seller_address": ac_seller_address.strip(),
            "ac_amount": ac_amount.strip(),
            "ac_amount_words": amount_to_words(ac_amount),
            "ac_make": ac_make.strip(),
            "ac_details": ac_details.strip(),
            # Camera Receipt
            "cam_seller_name": cam_seller_name.strip(),
            "cam_seller_relation": cam_seller_relation.strip(),
            "cam_seller_address": cam_seller_address.strip(),
            "cam_amount": cam_amount.strip(),
            "cam_amount_words": amount_to_words(cam_amount),
            "cam_make": cam_make.strip(),
            # Inverter Receipt
            "inv_seller_name": inv_seller_name.strip(),
            "inv_seller_relation": inv_seller_relation.strip(),
            "inv_seller_address": inv_seller_address.strip(),
            "inv_amount": inv_amount.strip(),
            "inv_amount_words": amount_to_words(inv_amount),
            "inv_make": inv_make.strip(),
            # Refrigerator Receipt
            "fridge_seller_name": fridge_seller_name.strip(),
            "fridge_seller_relation": fridge_seller_relation.strip(),
            "fridge_seller_address": fridge_seller_address.strip(),
            "fridge_amount": fridge_amount.strip(),
            "fridge_amount_words": amount_to_words(fridge_amount),
            "fridge_make": fridge_make.strip(),
            "fridge_details": fridge_details.strip(),
            # Working Reports
            "prop_work_history": st.session_state.prop_work_history,
            
            # Common
            "current_date": fmt_date(doc_date),
        }

        if entity_type in ["partner", "director"]:
            for i in range(len(entities_data)):
                entities_data[i]["work_history"] = st.session_state.get(f"{entity_type}_work_history_{i}", [])
                
        for i in range(len(pharmacists_data)):
            pharmacists_data[i]["work_history"] = st.session_state.get(f"rp_work_history_{i}", [])

        # Add address-change-specific fields
        if action_type == "address_change":
            context["old_address"] = old_address.strip()
            context["new_address"] = new_address.strip()
            context["drug_license_number"] = drug_license_number.strip()
            context["applying_for"] = applying_for.strip()

        # Generate
        with st.spinner("Processing..."):
            try:
                zip_bytes, rendered_names = generate_documents(context, tpl_dir)
            except Exception as exc:
                st.error(f"Document generation failed: {exc}")
                st.stop()

        # Success
        safe_name = sanitize_filename(firm_name)
        prefix = "Address_Change" if action_type == "address_change" else "New_Retail_File"
        zip_filename = f"{prefix}_{safe_name}.zip"

        st.markdown(
            f"""
            <div class="result-card">
                <h4>Generation Complete</h4>
                <p>{len(rendered_names)} documents compiled into {zip_filename}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.expander("Files included in archive", expanded=True):
            for idx, name in enumerate(rendered_names, 1):
                st.markdown(f"`{idx}.`&ensp;{name}")

        st.download_button(
            label="DOWNLOAD ZIP ARCHIVE",
            data=zip_bytes,
            file_name=zip_filename,
            mime="application/zip",
            use_container_width=True,
        )




if __name__ == "__main__":
    main()
