import streamlit as st

# إعداد الصفحة لتكون واسعة جداً لمنع تداخل الأعمدة
st.set_page_config(page_title="نظام وقود بريد الجزائر", layout="wide")

# --- مدخلات القائمة الجانبية ---
with st.sidebar:
    st.header("📅 إعدادات التاريخ")
    months = ["JANVIER", "FEVRIER", "MARS", "AVRIL", "MAI", "JUIN", "JUILLET", "AOUT", "SEPTEMBRE", "OCTOBRE", "NOVEMBRE", "DECEMBRE"]
    sel_month = st.selectbox("الشهر:", months)
    sel_year = st.selectbox("السنة:", [2025, 2026, 2027], index=1)
    
    st.header("📋 البيانات الأساسية")
    liste_cdd = ["cdd ziadia", "cdd zighoud youcef", "cdd nouvel ville", "cdd 20 aout"]
    bureau = st.selectbox("المكتب:", options=liste_cdd)
    n_carte = st.text_input("رقم البطاقة:", value="9887")
    
    # التعبئة التلقائية لبياناتك الأساسية
    default_im = "00341-318-25" if "ziadia" in bureau and n_carte == "9887" else ""
    immat = st.text_input("رقم الترقيم:", value=default_im)
    prix_litre = st.number_input("سعر اللتر (DA):", value=45.60, format="%.2f")
    
    st.header("📊 قراءات العداد")
    idx_prec = st.number_input("العداد السابق:", min_value=0.0, format="%.0f")
    idx_fin = st.number_input("العداد الحالي:", min_value=0.0, format="%.0f")
    
    st.header("💰 الماليات")
    solde = st.number_input(f"الرصيد في 01/{sel_month}:", min_value=0.0)
    char = st.number_input("المبلغ المشحون (DA):", min_value=0.0)

    st.header("⛽ مبالغ البونات (حتى 5)")
    b1 = st.number_input("مبلغ البون 1", min_value=0.0)
    bons = [b1]
    if b1 > 0:
        b2 = st.number_input("مبلغ البون 2", min_value=0.0); bons.append(b2)
        if b2 > 0:
            b3 = st.number_input("مبلغ البون 3", min_value=0.0); bons.append(b3)
            if b3 > 0:
                b4 = st.number_input("مبلغ البون 4", min_value=0.0); bons.append(b4)
                if b5 > 0:
                    b5 = st.number_input("مبلغ البون 5", min_value=0.0); bons.append(b5)

# --- الحسابات المنطقية ---
total_consom = sum(bons)
km = idx_fin - idx_prec
reste_fin = solde + char - total_consom
moy = ((total_consom / prix_litre) / km * 100) if km > 0 else 0.0

# --- عرض التقرير والطباعة ---
if idx_fin > 0:
    # تنسيق الطباعة (CSS)
    st.markdown(f"""
        <style>
        @media print {{
            .no-print, [data-testid="stSidebar"], header, [data-testid="stHeader"] {{ display: none !important; }}
            .main {{ width: 100% !important; padding: 0 !important; }}
            table {{ width: 100% !important; border-collapse: collapse !important; border: 1.5px solid black !important; }}
            th, td {{ border: 1.5px solid black !important; padding: 12px !important; text-align: center !important; font-size: 14px !important; color: black !important; font-weight: bold; }}
        }}
        .print-btn {{
            background-color: #f8f9fa; color: black; padding: 15px; border: 2px solid black;
            border-radius: 4px; cursor: pointer; font-weight: bold; width: 100%; margin-bottom: 25px; font-size: 18px;
        }}
        </style>
        <button class="print-btn no-print" onclick="window.print()">🖨️ اضغط هنا لطباعة التقرير النهائي</button>
    """, unsafe_allow_html=True)

    # هيكل الجدول الرسمي (موسع للأعمدة)
    report_html = f"""
    <div style="background-color: white; color: black; font-family: Arial, sans-serif;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px; padding: 0 10px;">
            <div style="font-weight: bold; font-size: 18px;">{bureau.upper()}</div>
            <h2 style="text-decoration: underline; text-align: center; margin: 0;">SITUATION CARBURANT MOIS DE {sel_month} {sel_year}</h2>
            <div style="font-weight: bold; border: 2px solid black; padding: 10px; min-width: 150px; text-align: center;">CONFIDENTIAL</div>
        </div>

        <table style="width: 100%; border: 2px solid black; border-collapse: collapse; table-layout: auto;">
            <thead>
                <tr style="height: 60px; background-color: #f9f9f9;">
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
                <tr style="height: 40px; background-color: #f9f9f9;">
                    <th>FIN DU MOIS CONSIDERE</th>
                    <th>FIN DU MOIS PRECEDENT</th>
                </tr>
            </thead>
            <tbody>
                <tr style="height: 80px; font-size: 16px;">
                    <td>01</td>
                    <td>{n_carte}</td>
                    <td>{bureau.upper()}</td>
                    <td>{immat}</td>
                    <td>{idx_fin:,.0f}</td>
                    <td>{idx_prec:,.0f}</td>
                    <td>{km:,.0f} km</td>
                    <td>{moy:.1f}</td>
                    <td>{solde:,.2f} DA</td>
                    <td>{char:,.2f} DA</td>
                    <td>{total_consom:,.2f} DA</td>
                    <td>{reste_fin:,.2f} DA</td>
                </tr>
            </tbody>
        </table>

        <div style="margin-top: 100px; display: flex; justify-content: space-between; font-weight: bold; padding: 0 60px; font-size: 16px;">
            <p style="text-decoration: underline;">Signature du Chauffeur</p>
            <p style="text-decoration: underline;">Le Chef de Bureau</p>
        </div>
    </div>
    """
    # عرض الجدول بمساحة مريحة
    st.write(report_html, unsafe_allow_html=True)
else:
    st.info("💡 أدخل قراءة 'العداد الحالي' في القائمة الجانبية ليظهر التقرير الرسمي.")
