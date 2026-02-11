import streamlit as st

# إعداد الصفحة
st.set_page_config(page_title="نظام وضعية الوقود الرسمي", layout="wide")

# كود الطباعة الاحترافي لجعل الجدول مطابقاً للصورة
def add_print_button():
    st.markdown(
        """
        <style>
        @media print {
            .no-print, .stSidebar, header, [data-testid="stHeader"] { display: none !important; }
            .main { width: 100% !important; padding: 0 !important; }
            .print-container { display: block !important; }
            table { width: 100% !important; border-collapse: collapse !important; border: 2px solid black !important; }
            th, td { border: 1px solid black !important; padding: 5px !important; text-align: center !important; font-family: Arial, sans-serif; font-size: 12px; }
            .header-title { text-align: center; font-weight: bold; text-decoration: underline; margin-bottom: 20px; }
        }
        .print-container { direction: ltr; }
        </style>
        <div class="no-print">
            <button onclick="window.print()" style="
                background-color: #1a73e8; color: white; padding: 12px 24px;
                border: none; border-radius: 4px; cursor: pointer; font-weight: bold; margin-bottom: 20px;
            ">🖨️ طباعة التقرير (طبعة رسمية)</button>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown('<div class="no-print"><h1>⛽ نظام تسيير استهلاك الوقود</h1></div>', unsafe_allow_html=True)

# --- القائمة الجانبية ---
with st.sidebar:
    st.header("📋 البيانات الأساسية")
    liste_cdd = ["cdd ziadia", "cdd zighoud youcef", "cdd nouvel ville", "cdd 20 aout"]
    bureau = st.selectbox("المكتب (BUREAU/CDD):", options=liste_cdd)
    
    n_carte = st.text_input("رقم البطاقة (N° Carte):", value="9887")
    
    # ميزة التعبئة التلقائية
    default_immat = "00341-318-25" if bureau == "cdd ziadia" and n_carte == "9887" else ""
    immat = st.text_input("رقم الترقيم (IMMATRICULATION):", value=default_immat)
    
    prix_litre = st.number_input("سعر اللتر الحالي (DA):", value=45.60)
    
    st.markdown("---")
    st.subheader("📊 قراءات العداد")
    index_prec = st.number_input("العداد السابق (FIN MOIS PRECEDENT):", min_value=0.0)
    index_fin = st.number_input("العداد الحالي (FIN DU MOIS CONSIDERE):", min_value=0.0)
    
    st.markdown("---")
    st.subheader("💰 المبالغ والارصدة")
    solde_init = st.number_input("الرصيد في 01/01 (RESTE 01/01):", min_value=0.0)
    chargement = st.number_input("المبلغ المشحون (Chargement):", min_value=0.0)

    st.markdown("---")
    st.subheader("⛽ إدخال البونات")
    b1 = st.number_input("البون الأول", min_value=0.0, step=100.0)
    bons = [b1]
    if b1 > 0:
        b2 = st.number_input("البون الثاني", min_value=0.0)
        bons.append(b2)
        if b2 > 0:
            b3 = st.number_input("البون الثالث", min_value=0.0)
            bons.append(b3)
            if b3 > 0:
                b4 = st.number_input("البون الرابع", min_value=0.0)
                bons.append(b4)
                if b4 > 0:
                    b5 = st.number_input("البون الخامس", min_value=0.0)
                    bons.append(b5)

# --- الحسابات ---
total_consom_da = sum(bons)
km_parcourus = index_fin - index_prec
reste_31 = solde_init + chargement - total_consom_da
moyenne = ((total_consom_da / prix_litre) / km_parcourus * 100) if km_parcourus > 0 else 0.0

# --- عرض النتيجة النهائية ---
if index_fin > 0:
    add_print_button()
    
    # بناء الجدول مطابق للصورة تماماً
    html_content = f"""
    <div class="print-container">
        <div class="header-title">SITUATION CARBURANT MOIS DE JANVIER 2026</div>
        <table>
            <tr>
                <th rowspan="2">N°</th>
                <th rowspan="2">N° Carte</th>
                <th rowspan="2">BUREAU/CDD /CTR</th>
                <th rowspan="2">IMMATRICUL TION</th>
                <th colspan="2">INDEX DU COMPTEUR</th>
                <th rowspan="2">KILOMETRAGE DU MOIS</th>
                <th rowspan="2">CONSOMMATION MOYENNE DE CARBURANT AUX 100 KM</th>
                <th rowspan="2">RESTE 01/01/2026</th>
                <th rowspan="2">Chargement en DA</th>
                <th rowspan="2">Consomma tion en DA</th>
                <th rowspan="2">Reste 31/01/2026</th>
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
                <td>{index_fin:,.0f}</td>
                <td>{index_prec:,.0f}</td>
                <td>{km_parcourus:,.0f} km</td>
                <td>{moyenne:.1f}</td>
                <td>{solde_init:,.2f} DA</td>
                <td>{chargement:,.2f} DA</td>
                <td>{total_consom_da:,.2f} DA</td>
                <td>{reste_31:,.2f} DA</td>
            </tr>
        </table>
    </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)
else:
    st.info("قم بإدخال قراءات العداد في القائمة الجانبية لإظهار التقرير المطابق للصورة.")
