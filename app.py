import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة لتكون واسعة
st.set_page_config(page_title="نظام وقود بريد الجزائر", layout="wide")

# --- مدخلات القائمة الجانبية ---
with st.sidebar:
    st.header("📅 الإعدادات")
    months = ["JANVIER", "FEVRIER", "MARS", "AVRIL", "MAI", "JUIN", "JUILLET", "AOUT", "SEPTEMBRE", "OCTOBRE", "NOVEMBRE", "DECEMBRE"]
    sel_month = st.selectbox("الشهر:", months)
    sel_year = st.selectbox("السنة:", [2025, 2026, 2027], index=1)
    
    st.header("📋 البيانات")
    bureau = st.selectbox("المكتب:", ["cdd ziadia", "cdd zighoud youcef", "cdd nouvel ville", "cdd 20 aout"])
    n_carte = st.text_input("رقم البطاقة:", value="9887")
    immat = st.text_input("رقم الترقيم:", value="00341-318-25")
    prix_litre = st.number_input("سعر اللتر:", value=45.60)
    
    st.header("📊 العداد")
    idx_prec = st.number_input("العداد السابق:", min_value=0.0, step=1.0)
    idx_fin = st.number_input("العداد الحالي:", min_value=0.0, step=1.0)
    
    st.header("💰 الماليات")
    solde_init = st.number_input(f"الرصيد في 01/{sel_month}:", min_value=0.0)
    chargement = st.number_input("المبلغ المشحون:", min_value=0.0)

    st.header("⛽ البونات (5)")
    b1 = st.number_input("بون 1", min_value=0.0)
    b2 = st.number_input("بون 2", min_value=0.0)
    b3 = st.number_input("بون 3", min_value=0.0)
    b4 = st.number_input("بون 4", min_value=0.0)
    b5 = st.number_input("بون 5", min_value=0.0)

# --- الحسابات ---
total_consom = b1 + b2 + b3 + b4 + b5
km = idx_fin - idx_prec
reste_fin = solde_init + chargement - total_consom
moy = ((total_consom / prix_litre) / km * 100) if km > 0 else 0.0

# --- عرض الجدول المضمون ---
if idx_fin > 0:
    # زر طباعة بسيط
    st.info("💡 للطباعة: اضغط على الزر أدناه ثم اختر (Save as PDF) أو (Print)")
    
    # تصميم الجدول كـ HTML صافي
    html_layout = f"""
    <div style="font-family: Arial, sans-serif; background-color: white; padding: 20px; color: black;">
        <style>
            table {{ width: 100%; border-collapse: collapse; border: 2.5px solid black; }}
            th, td {{ border: 1.5px solid black; padding: 12px; text-align: center; font-weight: bold; font-size: 14px; color: black; }}
            .header-info {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }}
            @media print {{ .no-print {{ display: none; }} }}
        </style>
        
        <button class="no-print" onclick="window.print()" style="width: 100%; padding: 15px; margin-bottom: 20px; cursor: pointer; font-weight: bold;">
            🖨️ طباعة التقرير الرسمي
        </button>

        <div class="header-info">
            <div style="font-size: 18px;">{bureau.upper()}</div>
            <h2 style="text-decoration: underline;">SITUATION CARBURANT MOIS DE {sel_month} {sel_year}</h2>
            <div style="border: 2px solid black; padding: 10px;">PROPRE</div>
        </div>

        <table>
            <thead>
                <tr style="background-color: #f0f0f0;">
                    <th rowspan="2">N°</th>
                    <th rowspan="2">N° Carte</th>
                    <th rowspan="2">BUREAU / CDD</th>
                    <th rowspan="2">IMMATRICULATION</th>
                    <th colspan="2">INDEX DU COMPTEUR</th>
                    <th rowspan="2">KM DU MOIS</th>
                    <th rowspan="2">MOYENNE 100 KM</th>
                    <th rowspan="2">RESTE 01/{sel_month}</th>
                    <th rowspan="2">Chargement</th>
                    <th rowspan="2">Consom DA</th>
                    <th rowspan="2">Reste FIN</th>
                </tr>
                <tr style="background-color: #f0f0f0;">
                    <th>FIN MOIS</th>
                    <th>MOIS PREC</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>01</td>
                    <td>{n_carte}</td>
                    <td>{bureau.upper()}</td>
                    <td>{immat}</td>
                    <td>{idx_fin:,.0f}</td>
                    <td>{idx_prec:,.0f}</td>
                    <td>{km:,.0f} km</td>
                    <td>{moy:.1f}</td>
                    <td>{solde_init:,.2f}</td>
                    <td>{chargement:,.2f}</td>
                    <td>{total_consom:,.2f}</td>
                    <td>{reste_fin:,.2f}</td>
                </tr>
            </tbody>
        </table>

        <div style="margin-top: 60px; display: flex; justify-content: space-between; font-weight: bold; padding: 0 40px;">
            <p style="text-decoration: underline;">Signature du Chauffeur</p>
            <p style="text-decoration: underline;">Le Chef de Bureau</p>
        </div>
    </div>
    """
    # استخدام المكون المضمون لعرض الـ HTML
    components.html(html_layout, height=600, scrolling=True)
else:
    st.warning("⚠️ يرجى إدخال 'العداد الحالي' لعرض التقرير.")
