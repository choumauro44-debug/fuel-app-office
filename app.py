import streamlit as st

# إعداد الصفحة
st.set_page_config(page_title="نظام وقود بريد الجزائر", layout="wide")

# رابط الشعار الرسمي
LOGO_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Alg%C3%A9rie_Poste_logo.svg/1200px-Alg%C3%A9rie_Poste_logo.svg.png"

# القائمة الجانبية: المدخلات
with st.sidebar:
    st.image(LOGO_URL, width=150)
    st.header("📅 الإعدادات")
    months = ["JANVIER", "FEVRIER", "MARS", "AVRIL", "MAI", "JUIN", "JUILLET", "AOUT", "SEPTEMBRE", "OCTOBRE", "NOVEMBRE", "DECEMBRE"]
    sel_month = st.selectbox("الشهر:", months)
    sel_year = st.selectbox("السنة:", [2025, 2026, 2027], index=1)
    
    st.header("📋 بيانات السيارة")
    liste_cdd = ["cdd ziadia", "cdd zighoud youcef", "cdd nouvel ville", "cdd 20 aout"]
    bureau = st.selectbox("المكتب:", options=liste_cdd)
    n_carte = st.text_input("رقم البطاقة:", value="9887")
    
    # ميزة التعبئة التلقائية لـ Ziadia
    default_im = "00341-318-25" if bureau == "cdd ziadia" and n_carte == "9887" else ""
    immat = st.text_input("رقم الترقيم:", value=default_im)
    prix_litre = st.number_input("سعر اللتر:", value=45.60)
    
    st.header("📊 العداد")
    idx_prec = st.number_input("العداد السابق:", min_value=0.0)
    idx_fin = st.number_input("العداد الحالي:", min_value=0.0)
    
    st.header("💰 الماليات")
    solde = st.number_input(f"الرصيد في 01/{sel_month}:", min_value=0.0)
    char = st.number_input("المبلغ المشحون:", min_value=0.0)

    st.header("⛽ البونات (حتى 5)")
    b1 = st.number_input("بون 1", min_value=0.0)
    bons = [b1]
    if b1 > 0:
        b2 = st.number_input("بون 2", min_value=0.0); bons.append(b2)
        if b2 > 0:
            b3 = st.number_input("بون 3", min_value=0.0); bons.append(b3)
            if b3 > 0:
                b4 = st.number_input("بون 4", min_value=0.0); bons.append(b4)
                if b4 > 0:
                    b5 = st.number_input("بون 5", min_value=0.0); bons.append(b5)

# الحسابات
total_consom = sum(bons)
km = idx_fin - idx_prec
reste_fin = solde + char - total_consom
moy = ((total_consom / prix_litre) / km * 100) if km > 0 else 0.0

# عرض النتائج والطباعة (الإصلاح الجذري لمشكلة النص)
if idx_fin > 0:
    # زر الطباعة بتصميم رسمي
    st.markdown(f"""
        <style>
        @media print {{
            .no-print, [data-testid="stSidebar"], header {{ display: none !important; }}
            .main {{ width: 100% !important; padding: 0 !important; }}
            table {{ width: 100% !important; border: 2px solid black !important; border-collapse: collapse !important; }}
            th, td {{ border: 1px solid black !important; padding: 8px !important; text-align: center !important; font-size: 12px; }}
        }}
        </style>
        <button onclick="window.print()" class="no-print" style="
            background-color: #ffcc00; color: #003399; padding: 15px; border: 2px solid #003399;
            border-radius: 8px; cursor: pointer; font-weight: bold; width: 100%; margin-bottom: 20px;
        ">🖨️ طباعة التقرير الرسمي لشهر {sel_month} {sel_year}</button>
    """, unsafe_allow_html=True)

    # إنشاء محتوى الجدول مطابق للصورة تماماً
    report_html = f"""
    <div style="font-family: Arial;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <img src="{LOGO_URL}" width="120">
            <h3 style="text-decoration: underline;">SITUATION CARBURANT MOIS DE {sel_month} {sel_year}</h3>
            <div style="font-weight: bold; border: 1px solid black; padding: 5px;">{bureau.upper()}</div>
        </div>
        <table>
            <tr style="background-color: #f2f2f2;">
                <th rowspan="2">N°</th><th rowspan="2">N° Carte</th><th rowspan="2">BUREAU/CDD</th><th rowspan="2">IMMATRICULATION</th>
                <th colspan="2">INDEX DU COMPTEUR</th><th rowspan="2">KM DU MOIS</th><th rowspan="2">MOYENNE 100 KM</th>
                <th rowspan="2">RESTE 01/{sel_month}</th><th rowspan="2">Chargement</th><th rowspan="2">Consom DA</th><th rowspan="2">Reste FIN</th>
            </tr>
            <tr><th>FIN MOIS</th><th>MOIS PREC</th></tr>
            <tr>
                <td>01</td><td>{n_carte}</td><td>{bureau.upper()}</td><td>{immat}</td>
                <td>{idx_fin:,.0f}</td><td>{idx_prec:,.0f}</td><td>{km:,.0f} km</td><td>{moy:.1f}</td>
                <td>{solde:,.2f}</td><td>{char:,.2f}</td><td>{total_consom:,.2f}</td><td>{reste_fin:,.2f}</td>
            </tr>
        </table>
        <div style="margin-top: 50px; display: flex; justify-content: space-between; font-weight: bold;">
            <p>Signature du Chauffeur</p><p>Le Chef de Bureau</p>
        </div>
    </div>
    """
    # السطر السحري الذي سيحول الكود إلى جدول حقيقي
    st.components.v1.html(report_html, height=400, scrolling=True)
else:
    st.info("💡 أدخل قراءات العداد في القائمة الجانبية ليبدأ النظام بالعمل.")
