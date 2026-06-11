"""
Perspectum — Regulatory Clearances & Certifications Dashboard
Run locally:  streamlit run app.py
Deploy free:  push to GitHub → connect at share.streamlit.io
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Perspectum · Regulatory Affairs",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #F8FAFC; }

    /* Hide Streamlit default header/footer */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    [data-testid="metric-container"] label {
        color: #64748B !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #0F1B33 !important;
        font-size: 32px !important;
        font-weight: 800 !important;
    }

    /* Dataframe */
    .stDataFrame { border-radius: 8px; overflow: hidden; }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: #F1F5F9;
        border-radius: 8px;
        padding: 4px;
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        font-weight: 600;
        font-size: 13px;
        padding: 6px 16px;
    }
    .stTabs [aria-selected="true"] {
        background: #0F1B33 !important;
        color: #FFFFFF !important;
    }

    /* Info/cert boxes */
    .cert-box {
        background: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 10px;
        font-size: 13px;
        line-height: 1.7;
    }
    .cert-box b { color: #15803D; }

    .info-box {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 10px;
        font-size: 13px;
        line-height: 1.7;
    }
    .info-box b { color: #0F1B33; }

    /* Page header */
    .page-header {
        background: linear-gradient(135deg, #0F1B33 0%, #1E3A5F 100%);
        color: white;
        padding: 24px 32px;
        border-radius: 12px;
        margin-bottom: 24px;
    }
    .page-header h1 { color: white; margin: 0; font-size: 26px; }
    .page-header p  { color: #94A3B8; margin: 4px 0 0; font-size: 13px; }

    /* Check / cross */
    .chk { color: #16A34A; font-size: 18px; font-weight: bold; }
    .crs { color: #CBD5E1; font-size: 18px; }

    /* Section headers */
    h3 { color: #0F1B33 !important; }
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────

@st.cache_data
def load_data():

    fda = pd.DataFrame([
        {"#":1, "510(k)":"K172685", "Product":"LiverMultiScan", "Version":"v2.x", "Cleared":"2017-11-21", "Code":"LNH", "Regulation":"21 CFR 892.100"},
        {"#":2, "510(k)":"K190017", "Product":"LiverMultiScan", "Version":"v3.x", "Cleared":"2019-06-27", "Code":"LNH", "Regulation":"21 CFR 892.100"},
        {"#":3, "510(k)":"K202170", "Product":"LiverMultiScan", "Version":"v4.0", "Cleared":"2020-02-10", "Code":"LNH", "Regulation":"21 CFR 892.100"},
        {"#":4, "510(k)":"K213960", "Product":"LiverMultiScan", "Version":"v5.x", "Cleared":"2022-09-06", "Code":"LNH", "Regulation":"21 CFR 892.100"},
        {"#":5, "510(k)":"K203280", "Product":"Hepatica",       "Version":"v1.0", "Cleared":"2021-01-12", "Code":"LNH", "Regulation":"21 CFR 892.100"},
        {"#":6, "510(k)":"K241925", "Product":"VitruvianScan",  "Version":"v1.0", "Cleared":"2024-10-02", "Code":"LNH", "Regulation":"21 CFR 892.100"},
        {"#":7, "510(k)":"K212565", "Product":"CoverScan",      "Version":"v1.0", "Cleared":"2022-05-19", "Code":"LLZ", "Regulation":"21 CFR 892.2050"},
        {"#":8, "510(k)":"K230294", "Product":"CoverScan",      "Version":"v1.1", "Cleared":"2023-03-03", "Code":"LLZ", "Regulation":"21 CFR 892.2050"},
        {"#":9, "510(k)":"K183133", "Product":"MRCP+",          "Version":"v1.x", "Cleared":"2019-01-09", "Code":"LLZ", "Regulation":"21 CFR 892.2050"},
        {"#":10,"510(k)":"K233930", "Product":"MRCP+",          "Version":"v2.0", "Cleared":"2024-03-13", "Code":"LLZ", "Regulation":"21 CFR 892.2050"},
    ])

    eudamed = pd.DataFrame([
        {"Product":"LiverMultiScan","Version":"v6.1",  "UDI-DI":"05056849000010",     "Basic UDI":"5056849LMSGV",      "Type":"MDR","Class":"Class IIa"},
        {"Product":"LiverMultiScan","Version":"v5.x",  "UDI-DI":"+B554LMS50D",        "Basic UDI":"++B554LMSST",       "Type":"MDR","Class":"Class IIa"},
        {"Product":"LiverMultiScan","Version":"v3.5.0","UDI-DI":"*+B554LMS30B*",      "Basic UDI":"B-*+B554LMS30B*",   "Type":"MDD","Class":"Class IIa"},
        {"Product":"VitruvianScan", "Version":"v1",    "UDI-DI":"+B554VSMD10/$+ 000N","Basic UDI":"++B554VSMUK",       "Type":"MDR","Class":"Class IIa"},
        {"Product":"Hepatica",      "Version":"v1",    "UDI-DI":"+B554HEPATICA10U",   "Basic UDI":"++B554HepaticaH2",  "Type":"MDR","Class":"Class IIb"},
        {"Product":"MRCP+",         "Version":"v1.01", "UDI-DI":"+B554MRCP10",        "Basic UDI":"B-+B554MRCP10",     "Type":"MDD","Class":"Class I"},
    ])

    singapore = pd.DataFrame([
        {"Product":"CoverScan",     "Registration":"Exempt from Registration","Status":"Cleared"},
        {"Product":"Hepatica",      "Registration":"Exempt from Registration","Status":"Cleared"},
        {"Product":"LiverMultiScan","Registration":"Exempt from Registration","Status":"Cleared"},
        {"Product":"VitruvianScan", "Registration":"Exempt from Registration","Status":"Cleared"},
        {"Product":"MRCP+",         "Registration":"Exempt from Registration","Status":"Cleared"},
    ])

    malaysia = pd.DataFrame([
        {"Device":"LiverMultiScan v3.1.0","Registration No.":"GB6824420-39123","Status":"Cleared"},
        {"Device":"LiverMultiScan v2.0.0","Registration No.":"GB579821204818", "Status":"Cleared"},
        {"Device":"LiverMultiScan v2.1.0","Registration No.":"GB579821204818", "Status":"Cleared"},
    ])

    uae = pd.DataFrame([
        {"Device":"LiverMultiScan","Registration No.":"DRCLAS-2026-002172","Date Cleared":"31/03/2026","Status":"Cleared"},
        {"Device":"VitruvianScan", "Registration No.":"DRCLAS-2026-002152","Date Cleared":"31/03/2026","Status":"Cleared"},
    ])

    switzerland = pd.DataFrame([
        {"Device":"LiverMultiScan","Registration No.":"CHRN-AR-20001035-MF-00093","Class":"Class IIa","Authority":"Swissmedic"},
        {"Device":"VitruvianScan", "Registration No.":"CHRN-AR-20001035-MF-00093","Class":"Class IIa","Authority":"Swissmedic"},
    ])

    matrix = pd.DataFrame([
        {"Product":"LiverMultiScan","MDD":"✔","MDR":"✔","UKCA":"✔","FDA":"✔","HSA":"✔","MDA":"✔","UAE":"✔","Swissmedic":"✔","Total":8},
        {"Product":"VitruvianScan", "MDD":"–","MDR":"✔","UKCA":"✔","FDA":"✔","HSA":"✔","MDA":"–","UAE":"✔","Swissmedic":"✔","Total":6},
        {"Product":"Hepatica",      "MDD":"–","MDR":"✔","UKCA":"✔","FDA":"✔","HSA":"✔","MDA":"–","UAE":"–","Swissmedic":"–","Total":4},
        {"Product":"CoverScan",     "MDD":"–","MDR":"–","UKCA":"✔","FDA":"✔","HSA":"✔","MDA":"–","UAE":"–","Swissmedic":"–","Total":3},
        {"Product":"MRCP+",         "MDD":"✔","MDR":"–","UKCA":"–","FDA":"✔","HSA":"✔","MDA":"–","UAE":"–","Swissmedic":"–","Total":3},
    ])

    all_clearances = pd.DataFrame([
        {"Market":"USA","Flag":"🇺🇸","Product":"LiverMultiScan","Version":"v2.x",       "Cert / Reg No.":"K172685",                  "Authority":"FDA 510(k)",        "Date":"2017-11-21","Status":"Active"},
        {"Market":"USA","Flag":"🇺🇸","Product":"LiverMultiScan","Version":"v3.x",       "Cert / Reg No.":"K190017",                  "Authority":"FDA 510(k)",        "Date":"2019-06-27","Status":"Active"},
        {"Market":"USA","Flag":"🇺🇸","Product":"LiverMultiScan","Version":"v4.0",       "Cert / Reg No.":"K202170",                  "Authority":"FDA 510(k)",        "Date":"2020-02-10","Status":"Active"},
        {"Market":"USA","Flag":"🇺🇸","Product":"LiverMultiScan","Version":"v5.x",       "Cert / Reg No.":"K213960",                  "Authority":"FDA 510(k)",        "Date":"2022-09-06","Status":"Active"},
        {"Market":"USA","Flag":"🇺🇸","Product":"Hepatica",      "Version":"v1.0",       "Cert / Reg No.":"K203280",                  "Authority":"FDA 510(k)",        "Date":"2021-01-12","Status":"Active"},
        {"Market":"USA","Flag":"🇺🇸","Product":"VitruvianScan", "Version":"v1.0",       "Cert / Reg No.":"K241925",                  "Authority":"FDA 510(k)",        "Date":"2024-10-02","Status":"Active"},
        {"Market":"USA","Flag":"🇺🇸","Product":"CoverScan",     "Version":"v1.0",       "Cert / Reg No.":"K212565",                  "Authority":"FDA 510(k)",        "Date":"2022-05-19","Status":"Active"},
        {"Market":"USA","Flag":"🇺🇸","Product":"CoverScan",     "Version":"v1.1",       "Cert / Reg No.":"K230294",                  "Authority":"FDA 510(k)",        "Date":"2023-03-03","Status":"Active"},
        {"Market":"USA","Flag":"🇺🇸","Product":"MRCP+",         "Version":"v1.x",       "Cert / Reg No.":"K183133",                  "Authority":"FDA 510(k)",        "Date":"2019-01-09","Status":"Active"},
        {"Market":"USA","Flag":"🇺🇸","Product":"MRCP+",         "Version":"v2.0",       "Cert / Reg No.":"K233930",                  "Authority":"FDA 510(k)",        "Date":"2024-03-13","Status":"Active"},
        {"Market":"UK", "Flag":"🇬🇧","Product":"LiverMultiScan","Version":"v2.x–v5.1.1","Cert / Reg No.":"UKCA 752965",              "Authority":"UKCA / BSI 0086",   "Date":"2021","Status":"Active"},
        {"Market":"UK", "Flag":"🇬🇧","Product":"Hepatica",      "Version":"v1.0",       "Cert / Reg No.":"UKCA 752965",              "Authority":"UKCA / BSI 0086",   "Date":"2022","Status":"Active"},
        {"Market":"UK", "Flag":"🇬🇧","Product":"CoverScan",     "Version":"v1.0–v1.2",  "Cert / Reg No.":"UKCA 752965",              "Authority":"UKCA / BSI 0086",   "Date":"2022","Status":"Active"},
        {"Market":"UK", "Flag":"🇬🇧","Product":"VitruvianScan", "Version":"v1.0",       "Cert / Reg No.":"UKCA 752965",              "Authority":"UKCA / BSI 0086",   "Date":"2024","Status":"Active"},
        {"Market":"EU", "Flag":"🇪🇺","Product":"LiverMultiScan","Version":"v3.5.0",     "Cert / Reg No.":"CE 677486",                "Authority":"CE/MDD BSI NL 2797","Date":"—","Status":"Active"},
        {"Market":"EU", "Flag":"🇪🇺","Product":"LiverMultiScan","Version":"v5.x/v6.1",  "Cert / Reg No.":"MDR 735482",               "Authority":"CE/MDR BSI NL 2797","Date":"—","Status":"Active"},
        {"Market":"EU", "Flag":"🇪🇺","Product":"VitruvianScan", "Version":"v1",         "Cert / Reg No.":"MDR 735482",               "Authority":"CE/MDR BSI NL 2797","Date":"—","Status":"Active"},
        {"Market":"EU", "Flag":"🇪🇺","Product":"Hepatica",      "Version":"v1",         "Cert / Reg No.":"MDR 735482",               "Authority":"CE/MDR BSI NL 2797","Date":"—","Status":"Active"},
        {"Market":"EU", "Flag":"🇪🇺","Product":"MRCP+",         "Version":"v1.01",      "Cert / Reg No.":"CE 677486",                "Authority":"CE/MDD BSI NL 2797","Date":"—","Status":"Active"},
        {"Market":"SG", "Flag":"🇸🇬","Product":"LiverMultiScan","Version":"All",        "Cert / Reg No.":"Exempt",                   "Authority":"HSA",               "Date":"—","Status":"Active"},
        {"Market":"SG", "Flag":"🇸🇬","Product":"CoverScan",     "Version":"All",        "Cert / Reg No.":"Exempt",                   "Authority":"HSA",               "Date":"—","Status":"Active"},
        {"Market":"SG", "Flag":"🇸🇬","Product":"Hepatica",      "Version":"All",        "Cert / Reg No.":"Exempt",                   "Authority":"HSA",               "Date":"—","Status":"Active"},
        {"Market":"SG", "Flag":"🇸🇬","Product":"VitruvianScan", "Version":"All",        "Cert / Reg No.":"Exempt",                   "Authority":"HSA",               "Date":"—","Status":"Active"},
        {"Market":"SG", "Flag":"🇸🇬","Product":"MRCP+",         "Version":"All",        "Cert / Reg No.":"Exempt",                   "Authority":"HSA",               "Date":"—","Status":"Active"},
        {"Market":"MY", "Flag":"🇲🇾","Product":"LiverMultiScan","Version":"v3.1.0",     "Cert / Reg No.":"GB6824420-39123",          "Authority":"MDA",               "Date":"—","Status":"Active"},
        {"Market":"MY", "Flag":"🇲🇾","Product":"LiverMultiScan","Version":"v2.0.0",     "Cert / Reg No.":"GB579821204818",           "Authority":"MDA",               "Date":"—","Status":"Active"},
        {"Market":"MY", "Flag":"🇲🇾","Product":"LiverMultiScan","Version":"v2.1.0",     "Cert / Reg No.":"GB579821204818",           "Authority":"MDA",               "Date":"—","Status":"Active"},
        {"Market":"UAE","Flag":"🇦🇪","Product":"LiverMultiScan","Version":"Current",    "Cert / Reg No.":"DRCLAS-2026-002172",       "Authority":"MOHAP",             "Date":"2026-03-31","Status":"Active"},
        {"Market":"UAE","Flag":"🇦🇪","Product":"VitruvianScan", "Version":"Current",    "Cert / Reg No.":"DRCLAS-2026-002152",       "Authority":"MOHAP",             "Date":"2026-03-31","Status":"Active"},
        {"Market":"CH", "Flag":"🇨🇭","Product":"LiverMultiScan","Version":"v3.5/v5.1",  "Cert / Reg No.":"CHRN-AR-20001035-MF-00093","Authority":"Swissmedic",        "Date":"—","Status":"Active"},
        {"Market":"CH", "Flag":"🇨🇭","Product":"VitruvianScan", "Version":"v1.0",       "Cert / Reg No.":"CHRN-AR-20001035-MF-00093","Authority":"Swissmedic",        "Date":"—","Status":"Active"},
    ])

    return fda, eudamed, singapore, malaysia, uae, switzerland, matrix, all_clearances

fda, eudamed, singapore, malaysia, uae, switzerland, matrix, all_clearances = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔬 Perspectum")
    st.markdown("**Regulatory Affairs**")
    st.markdown("---")
    st.markdown("**Portfolio Summary**")
    st.metric("Products",      "5")
    st.metric("Jurisdictions", "7")
    st.metric("Clearances",    "20+")
    st.metric("FDA 510(k)s",   "10")
    st.markdown("---")
    st.markdown("**Manufacturer**")
    st.caption("Perspectum Ltd")
    st.caption("Gemini One, Oxford, UK")
    st.caption("SRN: GB-MF-000016685")
    st.markdown("**Auth Rep (EU)**")
    st.caption("Perspectum Unipessoal Lda")
    st.caption("Lisbon, Portugal")
    st.caption("SRN: PT-AR-000009160")
    st.markdown("---")
    st.caption("QMS-REG-001  ·  April 2026")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
  <h1>Regulatory Clearances & Certifications</h1>
  <p>Global medical device portfolio  ·  Perspectum Ltd  ·  April 2026</p>
</div>
""", unsafe_allow_html=True)

# ── KPI row ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Product Families",   "5")
k2.metric("Jurisdictions",      "7")
k3.metric("Active Clearances",  "20+")
k4.metric("FDA 510(k)s",        "10")
k5.metric("GMDN / EMDN Codes",  "5")

st.markdown("<br>", unsafe_allow_html=True)

# ── Main tabs ─────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "🌍 Overview",
    "🇺🇸 USA (FDA)",
    "🇬🇧 UK (UKCA)",
    "🇪🇺 EU (MDR)",
    "🇸🇬 Singapore",
    "🇲🇾 Malaysia",
    "🇦🇪 UAE",
    "🇨🇭 Switzerland",
    "📋 All Clearances",
    "📊 Analytics",
])

# ════════ TAB 1: OVERVIEW ════════
with tabs[0]:
    st.markdown("### Product × Jurisdiction Matrix")
    st.caption("✔ = active clearance or approval  ·  – = not approved in this market")

    # Colour the checkmarks
    def style_matrix(val):
        if val == "✔":
            return "color: #16A34A; font-weight: bold; font-size: 16px; text-align: center"
        elif val == "–":
            return "color: #CBD5E1; text-align: center"
        return ""

    styled = matrix.set_index("Product").style.applymap(style_matrix)
    st.dataframe(styled, use_container_width=True, height=220)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Approved Markets Summary")

    market_info = [
        ("🇺🇸", "USA", "FDA 510(k)", "10 cleared submissions", "#EFF6FF", "#2563EB"),
        ("🇬🇧", "UK",  "UKCA",       "Certificate: UKCA 752965  ·  NB: BSI UK (0086)", "#F0FDF4", "#16A34A"),
        ("🇪🇺", "EU",  "MDR / MDD",  "MDR 735482  ·  CE 677486  ·  NB: BSI NL (2797)", "#FAF5FF", "#7C3AED"),
        ("🇸🇬", "Singapore", "HSA",  "5 products cleared (Class A SaMD — exempt from registration)", "#F0FDF4", "#059669"),
        ("🇲🇾", "Malaysia", "MDA",   "GB579821204818  ·  GB6824420-39123", "#FFFBEB", "#D97706"),
        ("🇦🇪", "UAE", "MOHAP",      "DRCLAS-2026-002172  ·  DRCLAS-2026-002152  ·  Cleared 31/03/2026", "#FFF7ED", "#EA580C"),
        ("🇨🇭", "Switzerland","Swissmedic","CHRN-AR-20001035-MF-00093  ·  Via EU MDR MRA", "#FAF5FF", "#7C3AED"),
    ]
    cols = st.columns(2)
    for i, (flag, market, authority, detail, bg, border) in enumerate(market_info):
        with cols[i % 2]:
            st.markdown(f"""
            <div style="background:{bg};border:1px solid {border};border-radius:8px;
                        padding:14px 18px;margin-bottom:10px;">
              <div style="font-size:18px;font-weight:700;color:#0F1B33;margin-bottom:4px;">
                {flag} {market} — {authority}
              </div>
              <div style="font-size:12px;color:#475569;">{detail}</div>
            </div>
            """, unsafe_allow_html=True)

# ════════ TAB 2: USA FDA ════════
with tabs[1]:
    st.markdown("### 🇺🇸 United States — FDA 510(k) Clearances")
    c1, c2 = st.columns([3, 1])
    with c1:
        st.caption("Food & Drug Administration  ·  10 cleared submissions  ·  Product codes LNH & LLZ")
    with c2:
        product_filter = st.selectbox("Filter by product",
            ["All"] + sorted(fda["Product"].unique().tolist()), key="fda_filter")

    df_show = fda if product_filter == "All" else fda[fda["Product"] == product_filter]
    st.dataframe(df_show.drop(columns=["#"]), use_container_width=True, hide_index=True, height=380)

    st.markdown("<br>", unsafe_allow_html=True)
    # Timeline chart
    st.markdown("#### Clearance Timeline")
    fda_chart = fda.copy()
    fda_chart["Cleared"] = pd.to_datetime(fda_chart["Cleared"])
    prod_colors = {
        "LiverMultiScan":"#2563EB","Hepatica":"#7C3AED",
        "CoverScan":"#059669","VitruvianScan":"#DB2777","MRCP+":"#D97706"
    }
    fig = px.scatter(
        fda_chart, x="Cleared", y="Product", text="510(k)",
        color="Product", color_discrete_map=prod_colors,
        size_max=12,
    )
    fig.update_traces(textposition="top center", marker_size=12)
    fig.update_layout(
        height=280, showlegend=False,
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
        yaxis=dict(showgrid=False),
        margin=dict(l=0, r=0, t=20, b=0),
    )
    st.plotly_chart(fig, use_container_width=True)

# ════════ TAB 3: UK ════════
with tabs[2]:
    st.markdown("### 🇬🇧 United Kingdom — UKCA")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<div class="cert-box">
            <b>UKCA Certificate:</b> UKCA 752965<br>
            <b>Notified Body:</b> BSI UK (0086)<br>
            <b>Manufacturer SRN:</b> GB-MF-000016685<br>
            <b>GMDN Code:</b> 57812<br>
            <b>EMDN Code:</b> Z11059082
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="info-box">
            <b>Regulation:</b> UK MDR 2002<br>
            <b>Classification framework:</b> CE marking transitioned to UKCA<br>
            <b>Auth Rep (GB):</b> Perspectum Ltd (manufacturer — GB based)
        </div>""", unsafe_allow_html=True)

    st.markdown("#### Products with UKCA Clearance")
    uk_data = pd.DataFrame([
        {"Product":"LiverMultiScan","Versions":"v2.x – v5.1.1","Class":"Class IIa","Certificate":"UKCA 752965"},
        {"Product":"Hepatica",      "Versions":"v1.0",          "Class":"Class IIb","Certificate":"UKCA 752965"},
        {"Product":"CoverScan",     "Versions":"v1.0 – v1.2",   "Class":"Class IIa","Certificate":"UKCA 752965"},
        {"Product":"VitruvianScan", "Versions":"v1.0",           "Class":"Class IIa","Certificate":"UKCA 752965"},
    ])
    st.dataframe(uk_data, use_container_width=True, hide_index=True)

# ════════ TAB 4: EU ════════
with tabs[3]:
    st.markdown("### 🇪🇺 European Union — CE/MDR & EUDAMED")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<div class="cert-box">
            <b>MDR Certificate:</b> MDR 735482<br>
            <b>Legacy CE Certificate:</b> CE 677486<br>
            <b>Notified Body:</b> BSI NL (2797)<br>
            <b>Auth Rep SRN:</b> PT-AR-000009160
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="info-box">
            <b>Auth Representative:</b> Perspectum Unipessoal Lda<br>
            Avenida Antonio Augusto de Aguiar, No. 19<br>
            4th Floor, Lisbon, Portugal<br>
            <b>Manufacturer SRN:</b> GB-MF-000016685
        </div>""", unsafe_allow_html=True)

    st.markdown("#### EUDAMED Device Registry")
    st.dataframe(eudamed, use_container_width=True, hide_index=True)

# ════════ TAB 5: SINGAPORE ════════
with tabs[4]:
    st.markdown("### 🇸🇬 Singapore — Health Sciences Authority (HSA)")
    st.markdown("""<div class="cert-box">
        <b>Registration status:</b> Exempt from Registration<br>
        <b>Basis:</b> Singapore HSA exempts Class A Software as a Medical Device (SaMD) from product registration<br>
        <b>Authority:</b> Health Sciences Authority
    </div>""", unsafe_allow_html=True)
    st.dataframe(singapore, use_container_width=True, hide_index=True)

# ════════ TAB 6: MALAYSIA ════════
with tabs[5]:
    st.markdown("### 🇲🇾 Malaysia — Medical Device Authority (MDA)")
    st.markdown("""<div class="info-box">
        <b>Authority:</b> Medical Device Authority (MDA)<br>
        <b>Regulation:</b> Medical Device Act 2012
    </div>""", unsafe_allow_html=True)
    st.dataframe(malaysia, use_container_width=True, hide_index=True)

# ════════ TAB 7: UAE ════════
with tabs[6]:
    st.markdown("### 🇦🇪 UAE — MOHAP / Emirates Drug Establishment")
    st.markdown("""<div class="cert-box">
        <b>Authority:</b> Ministry of Health and Prevention (MOHAP)<br>
        <b>Local Agent:</b> Freyr Solutions<br>
        <b>Regulation:</b> Cabinet Decision No. 39 of 2019
    </div>""", unsafe_allow_html=True)
    st.dataframe(uae, use_container_width=True, hide_index=True)

# ════════ TAB 8: SWITZERLAND ════════
with tabs[7]:
    st.markdown("### 🇨🇭 Switzerland — Swissmedic")
    st.markdown("""<div class="cert-box">
        <b>Authority:</b> Swissmedic — Swiss Agency for Therapeutic Products<br>
        <b>Regulation:</b> MedDO (SR 812.213)<br>
        <b>Route:</b> Recognised via EU MDR Mutual Recognition Agreement (MRA)
    </div>""", unsafe_allow_html=True)
    st.dataframe(switzerland, use_container_width=True, hide_index=True)

# ════════ TAB 9: ALL CLEARANCES ════════
with tabs[8]:
    st.markdown("### All Clearances — Master Table")
    st.caption("Complete listing of all active certifications and registration numbers")

    col1, col2, col3 = st.columns(3)
    with col1:
        mkt_filter = st.selectbox("Market", ["All"] + sorted(all_clearances["Market"].unique().tolist()))
    with col2:
        prd_filter = st.selectbox("Product", ["All"] + sorted(all_clearances["Product"].unique().tolist()))
    with col3:
        search = st.text_input("Search cert number", placeholder="e.g. K213960")

    df_all = all_clearances.copy()
    if mkt_filter != "All":
        df_all = df_all[df_all["Market"] == mkt_filter]
    if prd_filter != "All":
        df_all = df_all[df_all["Product"] == prd_filter]
    if search:
        df_all = df_all[df_all["Cert / Reg No."].str.contains(search, case=False, na=False)]

    st.dataframe(
        df_all.drop(columns=["Flag"]),
        use_container_width=True, hide_index=True, height=520
    )
    st.caption(f"Showing {len(df_all)} of {len(all_clearances)} records")

    # Download
    csv = df_all.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇ Download as CSV",
        data=csv,
        file_name="perspectum_clearances.csv",
        mime="text/csv",
    )

# ════════ TAB 10: ANALYTICS ════════
with tabs[9]:
    st.markdown("### Analytics")
    col1, col2 = st.columns(2)

    with col1:
        # Approvals by market (bar)
        market_counts = all_clearances.groupby("Market").size().reset_index(name="Clearances")
        market_counts = market_counts.sort_values("Clearances", ascending=True)
        fig1 = px.bar(
            market_counts, x="Clearances", y="Market", orientation="h",
            title="Clearances by Market",
            color="Clearances",
            color_continuous_scale=["#BAE6FD","#0284C7","#0F1B33"],
        )
        fig1.update_layout(
            height=320, showlegend=False, coloraxis_showscale=False,
            plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
            yaxis=dict(showgrid=False),
            title_font_size=13, title_font_color="#0F1B33",
            margin=dict(l=0, r=0, t=40, b=0),
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        # Clearances by product (bar)
        prod_counts = all_clearances.groupby("Product").size().reset_index(name="Clearances")
        prod_counts = prod_counts.sort_values("Clearances", ascending=True)
        fig2 = px.bar(
            prod_counts, x="Clearances", y="Product", orientation="h",
            title="Clearances by Product",
            color="Product",
            color_discrete_map={
                "LiverMultiScan":"#2563EB","Hepatica":"#7C3AED",
                "CoverScan":"#059669","VitruvianScan":"#DB2777","MRCP+":"#D97706"
            },
        )
        fig2.update_layout(
            height=320, showlegend=False,
            plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
            yaxis=dict(showgrid=False),
            title_font_size=13, title_font_color="#0F1B33",
            margin=dict(l=0, r=0, t=40, b=0),
        )
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        # Authority distribution (pie)
        auth_counts = all_clearances.groupby("Authority").size().reset_index(name="Count")
        fig3 = px.pie(
            auth_counts, values="Count", names="Authority",
            title="Clearances by Regulatory Authority",
            color_discrete_sequence=px.colors.qualitative.Set2,
            hole=0.4,
        )
        fig3.update_layout(
            height=320, title_font_size=13, title_font_color="#0F1B33",
            margin=dict(l=0, r=0, t=40, b=0),
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        # FDA clearances over time (line)
        fda_time = fda.copy()
        fda_time["Year"] = pd.to_datetime(fda_time["Cleared"]).dt.year
        fda_by_year = fda_time.groupby("Year").size().reset_index(name="Clearances")
        fig4 = px.line(
            fda_by_year, x="Year", y="Clearances",
            title="FDA 510(k) Clearances by Year",
            markers=True,
        )
        fig4.update_traces(line_color="#2563EB", line_width=2.5, marker_size=8)
        fig4.update_layout(
            height=320, plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(showgrid=True, gridcolor="#F1F5F9", dtick=1),
            yaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
            title_font_size=13, title_font_color="#0F1B33",
            margin=dict(l=0, r=0, t=40, b=0),
        )
        st.plotly_chart(fig4, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption(
    "Perspectum Ltd  ·  Gemini One, 5520 John Smith Drive, Oxford, OX4 2LL  ·  "
    "regulatory@perspectum.com  ·  perspectum.com  ·  GB-MF-000016685  ·  QMS-REG-001"
)
