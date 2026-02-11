import streamlit as st

# إعداد الصفحة لتكون واسعة جداً
st.set_page_config(page_title="نظام وقود بريد الجزائر", layout="wide")

# --- مدخلات القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.header("📅 الإعدادات العامة")
    months = ["JANVIER", "FEVRIER", "MARS", "AVRIL", "MAI", "JUIN", "JUILLET", "AOUT", "SEPTEMBRE", "OCTOBRE", "NOVEMBRE", "DECEMBRE"]
    sel_month = st.selectbox("اختر الشهر:", months)
    sel_year = st.selectbox("اختر السنة:", [2025, 2026, 2027], index=1)
    
    st.header("📋 بيانات السيارة")
    bureau = st.selectbox("المكتب:", ["cdd ziadia", "cdd zighoud youcef", "cdd nouvel ville", "cdd 20 aout"])
    n_carte = st.text_input("رقم البطاقة:", value="9887")
    immat = st.text_input("رقم الترقيم:", value="00341-318-25")
    prix_litre = st.number_input("سعر اللتر (DA):", value=45.60)
    
    st.header("📊 قراءات العداد")
    idx_prec = st.number_input("العداد السابق (PRECEDENT):", min_value=0.0)
    idx_fin = st.number_input("العداد الحالي (CONSIDERE):", min_value=0.0)
    
    st.header("💰 الرصيد والماليات")
    solde_init = st.number_input(f"الرصيد في 01/{sel_month}:", min_value=0.0)
    chargement = st.number_input("المبلغ المشحون (DA):", min_value=0.0)

    st.header("⛽ مبالغ البونات (حتى 5)")
    b1 = st.number_input("مبلغ بون 1", min_value=0.0)
    b2 = st.number_input("مبلغ بون 2", min_value=0.0)
    b3 = st.number_input("مبلغ بون 3", min_value=0.0)
    b4 = st.number_input("مبلغ بون 4", min_value=0.0)
    b5 = st.number_input("مبلغ بون 5", min_value=0.0)

# --- الحسابات ---
total_consom_da = b1 + b2 + b3 + b4 + b5
km_parcourus = idx_fin - idx_prec
reste_fin_mois = solde_init + chargement - total_consom_da
# حساب المعدل (الاستهلاك باللتر / المسافة * 100)
moyenne = ((total_consom_da / prix_litre) / km_parcourus * 100) if km_parcourus > 0 else 0.0

# --- عرض التقرير والطباعة ---
if idx_fin > 0:
    # تنسيق الطباعة (أبيض وأسود، خط عريض، جدول واسع)
    st.markdown(f"""
        <style>
        @media print {{
            .no-print, [data-testid="stSidebar"], header {{ display: none !important; }}
            .main {{ width: 100% !important; padding: 0 !important; }}
            table {{ width: 100% !important; border: 2px solid black !important; border-collapse: collapse !important; }}
            th, td {{ border: 2px solid black !important; padding: 12px !important; text-align: center !important; 
                     font-size: 15px !important; color: black !important; font-weight: bold !important; }}
        }}
        .print-button {{
            background-color: #f0f2f6; color: black; padding: 10px 20px; border: 2px solid black;
            border-radius: 5px; cursor: pointer; font-weight: bold; width: 100%; margin-bottom: 20px;
        }}
        </style>
        <button class="print-button no-print" onclick="window.print()">🖨️ اضغط هنا لطباعة التقرير الرسمي (أبيض وأسود)</button>
    """, unsafe_allow_html=True)

    # هيكل الجدول (مطابق تماماً لورقتك الرسمية بدون ألوان)
    report_html = f"""
    <div style="background-color: white; color: black; font-family: Arial, sans-serif; padding: 10px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;">
            <div style="font-weight: bold; font-size: 18px;">{bureau.upper()}</div>
            <h2 style="text-decoration: underline; text-align: center; margin: 0;">SITUATION CARBURANT MOIS DE {sel_month} {sel_year}</h2>
            <div style="font-weight: bold; border: 2px solid black; padding: 10px;">PROPRE</div>
        </div>

        <table style="width: 100%; border: 2px solid black; border-collapse: collapse;">
            <thead>
                <tr style="height: 60px;">
                    <th rowspan="2">N°</th>
                    <th rowspan="2">N° Carte</th>
                    <th rowspan="2">BUREAU / CDD / CTR</th>
                    <th rowspan="2">IMMATRICULATION</th>
                    <th colspan="2">INDEX DU COMPTEUR</th>
                    <th rowspan="2">KILOMETRAGE DU MOIS</th>
                    <th rowspan="2">CONSOMMATION MOYENNE 100 KM</th>
                    <th rowspan="2">RESTE 01/{sel_month}</th>
                    <th rowspan="2">Chargement en DA</th>
                    <th rowspan="2">Consommation en DA</th>
                    <th rowspan="2">Reste FIN MOIS</th>
                </tr>
                <tr style="height: 40px;">
                    <th>FIN DU MOIS CONSIDERE</th>
                    <th>FIN DU MOIS PRECEDENT</th>
                </tr>
            </thead>
            <tbody>
                <tr style="height: 80px; font-size: 17px;">
                    <td>01</td>
                    <td>{n_carte}</td>
                    <td>{bureau.upper()}</td>
                    <td>{immat}</td>
                    <td>{idx_fin:,.0f}</td>
                    <td>{idx_prec:,.0f}</td>
                    <td>{km_parcourus:,.0f} km</td>
                    <td>{moyenne:.1f}</td>
                    <td>{solde_init:,.2f}</td>
                    <td>{chargement:,.2f}</td>
                    <td>{total_consom_da:,.2f}</td>
                    <td>{reste_fin_mois:,.2f}</td>
                </tr>
            </tbody>
        </table>

        <div style="margin-top: 80px; display: flex; justify-content: space-between; font-weight: bold; padding: 0 50px;">
            <p style="text-decoration: underline; font-size: 16px;">Signature du Chauffeur</p>
            <p style="text-decoration: underline; font-size: 16px;">Le Chef de Bureau</p>
        </div>
    </div>
    """
    # استخدام st.write بدلاً من st.components لضمان تفاعل المتصفح مع الجدول فوراً
    st.write(report_html, unsafe_allow_html=True)
else:
    st.info("💡 الرجاء إدخال 'العداد الحالي' في القائمة الجانبية لعرض التقرير.")
