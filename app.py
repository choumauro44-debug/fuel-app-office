import streamlit as st
import datetime

# إعداد الصفحة
st.set_page_config(page_title="نظام وضعية الوقود - بريد الجزائر", layout="wide")

# رابط الشعار الذي أرسلته (استخدام رابط مباشر لضمان الظهور)
LOGO_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Alg%C3%A9rie_Poste_logo.svg/1200px-Alg%C3%A9rie_Poste_logo.svg.png"

def add_print_button(month, year):
    st.markdown(
        f"""
        <style>
        @media print {{
            .no-print, .stSidebar, header, [data-testid="stHeader"] {{ display: none !important; }}
            .main {{ width: 100% !important; padding: 0 !important; }}
            .print-container {{ display: block !important; padding: 20px; }}
            table {{ width: 100% !important; border-collapse: collapse !important; border: 2px solid black !important; }}
            th, td {{ border: 1px solid black !important; padding: 5px !important; text-align: center !important; font-family: Arial, sans-serif; font-size: 12px; }}
            .header-report {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }}
            .logo-img {{ width: 100px; }}
            .footer-sign {{ margin-top: 50px; display: flex; justify-content: space-between; padding: 0 50px; font-weight: bold; }}
        }}
        </style>
        <div class="no-print">
            <button onclick="window.print()" style="
                background-color: #ffcc00; color: #003399; padding: 12px 24px;
                border: 2px solid #003399; border-radius: 4px; cursor: pointer; font-weight: bold;
            ">🖨️ طباعة تقرير شهر {month} {year}</button>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown('<div class="no-print"><h1>⛽ نظام تسيير استهلاك الوقود - بريد الجزائر</h1></div>', unsafe_allow_html=True)

# --- القائمة الجانبية ---
with st.sidebar:
    st.image(LOGO_URL, width=150)
    st.header("📅 تاريخ التقرير")
    months = ["JANVIER", "FEVRIER", "MARS", "AVRIL", "MAI", "JUIN", "JUILLET", "AOUT", "SEPTEMBRE", "OCTOBRE", "NOVEMBRE", "DECEMBRE"]
    selected_month = st.selectbox("اختر الشهر:", options=months)
    selected_year = st.selectbox("اختر السنة:", options=[2025, 2026, 2027], index=1)

    st.header("📋 البيانات الأساسية")
    liste_cdd = ["cdd ziadia", "cdd zighoud youcef", "cdd nouvel ville", "cdd 20 aout"]
    bureau = st.selectbox("المكتب (BUREAU/CDD):", options=liste_cdd)
    n_carte = st.text_input("رقم البطاقة (N° Carte):", value="9887")
    
    default_immat = "00341-318-25" if bureau == "cdd ziadia" and n_carte == "9887" else ""
    immat = st.text_input("رقم الترقيم (IMMATRICULATION):", value=default_immat)
    
    st.markdown("---")
    index_prec = st.number_input("العداد السابق (FIN MOIS PRECEDENT):", min_value=0.0)
    index_fin = st.number_input("العداد الحالي (FIN DU MOIS CONSIDERE):", min_value=0.0)
    solde_init = st.number_input(f"الرصيد في 01/{selected_month}:", min_value=0.0)
    chargement = st.number_input("المبلغ المشحون (Chargement):", min_value=0.0)

    st.subheader("⛽ إدخال البونات")
    b1 = st.number_input("البون 1", min_value=0.0)
    bons = [b1]
    if b1 > 0:
        b2 = st.number_input("البون 2", min_value=0.0)
        bons.append(b2)
        if b2 > 0:
            b3 = st.number_input("البون 3", min_value=0.0)
            bons.append(b3)
            # يمكن إضافة المزيد بنفس الطريقة

# --- الحسابات ---
total_consom_da = sum(bons)
km_parcourus = index_fin - index_prec
reste_31 = solde_init + chargement - total_consom_da
moyenne = ((total_consom_da / 45.6) / km_parcourus * 100) if km_parcourus > 0 else 0.0

# --- عرض التقرير ---
if index_fin > 0:
    add_print_button(selected_month, selected_year)
    
    html_content = f"""
    <div class="print-container">
        <div class="header-report">
            <img src="{LOGO_URL}" class="logo-img">
            <div style="text-align: right; font-weight: bold;">{bureau.upper()}</div>
        </div>
        
        <div style="text-align: center; font-weight: bold; text-decoration: underline; margin-bottom: 20px;">
            SITUATION CARBURANT MOIS DE {selected_month} {selected_year}
        </div>

        <table>
            <tr style="background-color: #f2f2f2;">
                <th rowspan="2">N°</th>
                <th rowspan="2">N° Carte</th>
                <th rowspan="2">BUREAU/CDD /CTR</th>
                <th rowspan="2">IMMATRICUL TION</th>
                <th colspan="2">INDEX DU COMPTEUR</th>
                <th rowspan="2">KILOMETRAGE DU MOIS</th>
                <th rowspan="2">CONSOMMATION MOYENNE AUX 100 KM</th>
                <th rowspan="2">RESTE 01/{selected_month}</th>
                <th rowspan="2">Chargement DA</th>
                <th rowspan="2">Consomma tion DA</th>
                <th rowspan="2">Reste FIN MOIS</th>
            </tr>
            <tr>
                <th>FIN MOIS CONSIDERE</th>
                <th>FIN MOIS PRECEDENT</th>
            </tr>
            <tr>
                <td>01</td>
                <td>{n_carte}</td>
                <td>{bureau.upper()}</td>
                <td>{immat}</td>
                <td>{index_fin:,.0f}</td>
                <td>{index_prec:,.0f}</td>
                <td>{km_parcourus:,.0f} km</td>
                <td>{moyenne:.1f}</td>
                <td>{solde_init:,.2f}</td>
                <td>{chargement:,.2f}</td>
                <td>{total_consom_da:,.2f}</td>
                <td>{reste_31:,.2f}</td>
            </tr>
        </table>
        
        <div class="footer-sign">
            <div>Signature du Chauffeur</div>
            <div>Le Chef de Bureau</div>
        </div>
    </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)
else:
    st.info("الرجاء إدخال البيانات لإظهار التقرير الرسمي.")
