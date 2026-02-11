import streamlit as st

# إعداد الصفحة لتكون عريضة ومنظمة
st.set_page_config(page_title="نظام وقود بريد الجزائر", layout="wide")

# رابط الشعار الرسمي لبريد الجزائر
LOGO_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Alg%C3%A9rie_Poste_logo.svg/1200px-Alg%C3%A9rie_Poste_logo.svg.png"

# وظيفة الطباعة الاحترافية
def add_print_button(month, year):
    st.markdown(
        f"""
        <style>
        @media print {{
            .no-print, [data-testid="stSidebar"], header, [data-testid="stHeader"], .stMarkdown {{ display: none !important; }}
            .main {{ width: 100% !important; padding: 0 !important; }}
            .printable-area {{ display: block !important; }}
            table {{ width: 100% !important; border-collapse: collapse !important; border: 2px solid black !important; }}
            th, td {{ border: 1px solid black !important; padding: 8px !important; text-align: center !important; font-size: 12px; font-family: Arial; }}
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

# --- القائمة الجانبية (كل المدخلات التي طلبتها) ---
with st.sidebar:
    st.image(LOGO_URL, width=150)
    st.header("📅 إعدادات الزمان")
    months = ["JANVIER", "FEVRIER", "MARS", "AVRIL", "MAI", "JUIN", "JUILLET", "AOUT", "SEPTEMBRE", "OCTOBRE", "NOVEMBRE", "DECEMBRE"]
    sel_month = st.selectbox("الشهر:", months)
    sel_year = st.selectbox("السنة:", [2025, 2026, 2027], index=1)
    
    st.header("📋 بيانات المكتب والسيارة")
    liste_cdd = ["cdd ziadia", "cdd zighoud youcef", "cdd nouvel ville", "cdd 20 aout"]
    bureau = st.selectbox("اختر المكتب:", options=liste_cdd)
    n_carte = st.text_input("رقم البطاقة (N° Carte):", value="9887")
    
    # التعبئة التلقائية لـ Ziadia
    default_immat = "00341-318-25" if bureau == "cdd ziadia" and n_carte == "9887" else ""
    immat = st.text_input("رقم الترقيم (IMMATRICULATION):", value=default_immat)
    
    prix_litre = st.number_input("سعر اللتر الحالي (DA):", value=45.60, format="%.2f")
    
    st.header("📊 قراءات العداد")
    idx_prec = st.number_input("العداد السابق (PRECEDENT):", min_value=0.0)
    idx_fin = st.number_input("العداد الحالي (CONSIDERE):", min_value=0.0)
    
    st.header("💰 الأرصدة والشحن")
    solde_init = st.number_input(f"الرصيد في 01/{sel_month}:", min_value=0.0)
    chargement = st.number_input("المبلغ المشحون (Chargement):", min_value=0.0)

    st.header("⛽ مبالغ البونات (حتى 5)")
    b1 = st.number_input("البون 1", min_value=0.0)
    bons = [b1]
    if b1 > 0:
        b2 = st.number_input("البون 2", min_value=0.0)
        bons.append(b2)
        if b2 > 0:
            b3 = st.number_input("البون 3", min_value=0.0)
            bons.append(b3)
            if b3 > 0:
                b4 = st.number_input("البون 4", min_value=0.0)
                bons.append(b4)
                if b4 > 0:
                    b5 = st.number_input("البون 5", min_value=0.0)
                    bons.append(b5)

# --- العمليات الحسابية ---
total_consom_da = sum(bons)
km_parcourus = idx_fin - idx_prec
reste_final = solde_init + chargement - total_consom_da
# حساب المعدل (لتر/100كلم)
moyenne = ((total_consom_da / prix_litre) / km_parcourus * 100) if km_parcourus > 0 else 0.0

# --- عرض التقرير النهائي ---
if idx_fin > 0:
    add_print_button(sel_month, sel_year)
    
    # بناء الجدول بنظام HTML لعرضه بشكل صحيح وقابل للطباعة
    report_html = f"""
    <div class="printable-area">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <img src="{LOGO_URL}" width="120">
            <div style="text-align: center;">
                <h3 style="text-decoration: underline;">SITUATION CARBURANT MOIS DE {sel_month} {sel_year}</h3>
            </div>
            <div style="font-weight: bold; border: 1px solid black; padding: 5px;">{bureau.upper()}</div>
        </div>

        <table style="width:100%; border-collapse: collapse; border: 2px solid black;">
            <tr style="background-color: #f2f2f2;">
                <th rowspan="2">N°</th>
                <th rowspan="2">N° Carte</th>
                <th rowspan="2">BUREAU/CDD /CTR</th>
                <th rowspan="2">IMMATRICUL TION</th>
                <th colspan="2">INDEX DU COMPTEUR</th>
                <th rowspan="2">KILOMETRAGE DU MOIS</th>
                <th rowspan="2">MOYENNE AUX 100 KM</th>
                <th rowspan="2">RESTE 01/{sel_month}</th>
                <th rowspan="2">Chargement en DA</th>
                <th rowspan="2">Consomma tion en DA</th>
                <th rowspan="2">Reste FIN MOIS</th>
            </tr>
            <tr>
                <th>FIN DU MOIS CONSIDERE</th>
                <th>FIN DU MOIS PRECEDENT</th>
            </tr>
            <tr>
                <td>01</td>
                <td>{n_carte}</td>
                <td>{bureau.upper()}</td>
                <td>{immat}</td>
                <td>{idx_fin:,.0f}</td>
                <td>{idx_prec:,.0f}</td>
                <td>{km_parcourus:,.0f} km</td>
                <td>{moyenne:.1f}</td>
                <td>{solde_init:,.2f} DA</td>
                <td>{chargement:,.2f} DA</td>
                <td>{total_consom_da:,.2f} DA</td>
                <td>{reste_final:,.2f} DA</td>
            </tr>
        </table>
        
        <div style="margin-top: 50px; display: flex; justify-content: space-between; padding: 0 50px; font-weight: bold;">
            <p>Signature du Chauffeur</p>
            <p>Le Chef de Bureau</p>
        </div>
    </div>
    """
    # عرض الجدول الحقيقي باستخدام unsafe_allow_html=True
    st.write(report_html, unsafe_allow_html=True)
else:
    st.info("💡 الرجاء إدخال 'العداد الحالي' في القائمة الجانبية ليظهر التقرير.")
