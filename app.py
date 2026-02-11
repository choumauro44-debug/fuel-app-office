import streamlit as st

# إعداد الصفحة
st.set_page_config(page_title="نظام وقود بريد الجزائر", layout="wide")

# رابط الشعار الرسمي
LOGO_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Alg%C3%A9rie_Poste_logo.svg/1200px-Alg%C3%A9rie_Poste_logo.svg.png"

# وظيفة الطباعة مع التصميم الرسمي
def add_print_button(month, year):
    st.markdown(
        f"""
        <style>
        @media print {{
            .no-print, [data-testid="stSidebar"], header, [data-testid="stHeader"] {{ display: none !important; }}
            .main {{ width: 100% !important; padding: 0 !important; }}
            table {{ width: 100% !important; border-collapse: collapse !important; border: 2px solid black !important; }}
            th, td {{ border: 1px solid black !important; padding: 8px !important; text-align: center !important; font-size: 12px; }}
            .header-report {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }}
        }}
        .print-btn {{
            background-color: #ffcc00; color: #003399; padding: 15px 30px;
            border: 2px solid #003399; border-radius: 8px; cursor: pointer; 
            font-weight: bold; font-size: 18px; width: 100%; margin-bottom: 20px;
        }}
        </style>
        <div class="no-print">
            <button class="print-btn" onclick="window.print()">🖨️ استخراج التقرير الرسمي لشهر {month} {year}</button>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- المدخلات في القائمة الجانبية ---
with st.sidebar:
    st.image(LOGO_URL, width=150)
    st.header("📅 الإعدادات")
    months = ["JANVIER", "FEVRIER", "MARS", "AVRIL", "MAI", "JUIN", "JUILLET", "AOUT", "SEPTEMBRE", "OCTOBRE", "NOVEMBRE", "DECEMBRE"]
    sel_month = st.selectbox("الشهر:", months, index=0)
    sel_year = st.selectbox("السنة:", [2025, 2026, 2027], index=1)
    
    st.header("📋 البيانات")
    liste_cdd = ["cdd ziadia", "cdd zighoud youcef", "cdd nouvel ville", "cdd 20 aout"]
    bureau = st.selectbox("المكتب:", options=liste_cdd)
    n_carte = st.text_input("رقم البطاقة:", value="9887")
    
    # التعبئة التلقائية لـ Ziadia
    default_im = "00341-318-25" if bureau == "cdd ziadia" and n_carte == "9887" else ""
    immat = st.text_input("رقم الترقيم:", value=default_im)
    
    idx_prec = st.number_input("العداد السابق:", min_value=0.0)
    idx_fin = st.number_input("العداد الحالي:", min_value=0.0)
    solde = st.number_input(f"الرصيد في 01/{sel_month}:", min_value=0.0)
    char = st.number_input("المبلغ المشحون:", min_value=0.0)
    consom_da = st.number_input("إجمالي البونات (DA):", min_value=0.0)

# --- الحسابات ---
km = idx_fin - idx_prec
reste = solde + char - consom_da
moy = ((consom_da / 45.6) / km * 100) if km > 0 else 0.0

# --- عرض التقرير النهائي (هنا الإصلاح الحقيقي) ---
if idx_fin > 0:
    add_print_button(sel_month, sel_year)
    
    # استخدمنا st.write مع unsafe_allow_html=True لعرض الجدول بشكل صحيح
    report_html = f"""
    <div class="header-report">
        <img src="{LOGO_URL}" width="120">
        <h2 style="text-align: center; text-decoration: underline;">SITUATION CARBURANT MOIS DE {sel_month} {sel_year}</h2>
        <div style="font-weight: bold;">{bureau.upper()}</div>
    </div>
    
    <table style="width:100%; border-collapse: collapse; border: 2px solid black;">
        <tr style="background-color: #f2f2f2;">
            <th rowspan="2">N°</th>
            <th rowspan="2">N° Carte</th>
            <th rowspan="2">BUREAU/CDD</th>
            <th rowspan="2">IMMATRICULATION</th>
            <th colspan="2">INDEX DU COMPTEUR</th>
            <th rowspan="2">KM DU MOIS</th>
            <th rowspan="2">MOYENNE 100 KM</th>
            <th rowspan="2">RESTE 01/{sel_month}</th>
            <th rowspan="2">Chargement</th>
            <th rowspan="2">Consom DA</th>
            <th rowspan="2">Reste 31/{sel_month}</th>
        </tr>
        <tr>
            <th>FIN MOIS</th>
            <th>MOIS PREC</th>
        </tr>
        <tr>
            <td>01</td>
            <td>{n_carte}</td>
            <td>{bureau.upper()}</td>
            <td>{immat}</td>
            <td>{idx_fin:,.0f}</td>
            <td>{idx_prec:,.0f}</td>
            <td>{km:,.0f}</td>
            <td>{moy:.1f}</td>
            <td>{solde:,.2f}</td>
            <td>{char:,.2f}</td>
            <td>{consom_da:,.2f}</td>
            <td>{reste:,.2f}</td>
        </tr>
    </table>
    
    <div style="margin-top: 40px; display: flex; justify-content: space-between; font-weight: bold;">
        <p>Signature du Chauffeur</p>
        <p>Le Chef de Bureau</p>
    </div>
    """
    # السطر الأهم الذي سيحول النص إلى جدول
    st.write(report_html, unsafe_allow_html=True)
else:
    st.info("قم بإدخال البيانات في اليسار لإظهار الجدول الرسمي.")
