import re

with open("app.py", "r") as f:
    content = f.read()

# CSS replacement block
modern_css = """    <style>
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
    * {
        font-family: 'Outfit', 'Inter', sans-serif !important;
    }
    
    /* ── Animated Background Layout ──────────────────── */
    [data-testid="stAppViewContainer"], .stApp {
        background: linear-gradient(-45deg, #f6f8fd, #f1f5f9, #e0e7ff, #f3e8ff) !important;
        background-size: 400% 400% !important;
        animation: gradientBG 15s ease infinite !important;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
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
    }
    div[role="radiogroup"] > label:hover {
        background: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    div[role="radiogroup"] > label[data-checked="true"] {
        background: white;
        border-color: var(--brand);
        box-shadow: 0 0 0 1px var(--brand), 0 4px 12px rgba(79, 91, 213, 0.15);
    }
    div[role="radiogroup"] > label > div:first-child {
        display: none; /* Hide the default radio circle for cleaner look */
    }
    div[role="radiogroup"] > label > div:last-child {
        margin-left: 0 !important;
        font-weight: 600 !important;
        color: var(--text-primary) !important;
        font-size: 0.95rem !important;
    }
    div[role="radiogroup"] > label[data-checked="true"] > div:last-child {
        color: var(--brand) !important;
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
    .stSelectbox > div > div,
    .stNumberInput > div > div > input {
        border-radius: var(--radius-sm) !important;
        border: 2px solid rgba(255,255,255,0.8) !important;
        background: rgba(255,255,255,0.4) !important;
        backdrop-filter: blur(5px) !important;
        transition: all 0.3s ease !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        color: var(--text-primary) !important;
        padding: 0.7rem 1rem !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--brand) !important;
        background: white !important;
        box-shadow: 0 0 0 4px rgba(79, 91, 213, 0.15) !important;
        transform: translateY(-1px);
    }
    
    .stTextInput label, .stTextArea label,
    .stSelectbox label, .stDateInput label, .stNumberInput label {
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        color: var(--text-secondary) !important;
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
    </style>"""

# Using regex to replace the entire <style> block
content = re.sub(r'<style>.*?</style>', modern_css, content, flags=re.DOTALL)

with open("app.py", "w") as f:
    f.write(content)
