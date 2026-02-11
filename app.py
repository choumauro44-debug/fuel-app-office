import streamlit as st
import pandas as pd

st.set_page_config(page_title="نظام وقود المكاتب", layout="wide")

def add_print_button():
    st.markdown(
        """
        <style>
        @media print {
            .stButton, .stTextArea, .stNumberInput, .stSelectbox, .stTextInput, .stSidebar, header, [data-testid="stToolbar"] {
                display: none !important;
            }
            .main { width: 100% !important; }
            table { width: 100% !important; border-collapse: collapse !important; }
        }
        </style>
        <button onclick="window.print()" style="
            background-color: #2e7d32;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 20px;
        ">🖨️ طباعة التقرير النهائي</button>
        """,
        unsafe_allow_html=True
    )

st.title("⛽ نظام إدارة ومتابعة استهلاك الوقود")

with st.sidebar:
    st.header("📋 مدخلات التقرير")
    liste_bureaux = ["CDD CNE ZIADIA", "BUREAU ALGER", "BUREAU ORAN", "BUREAU ANNABA", "BUREAU CONSTANTINE"]
    bureau_selected = st.selectbox("اختر المكتب:", options=liste_bureaux)
    n_carte_input = st.text_input("رقم البطاقة (N° Carte):", value="9887")
    prix_litre = st.number_input("سعر اللتر الحالي (DA):", value=45.60, format="%.2f")
    st.markdown("---")
    index_prec = st.number_input("العداد السابق (INDEX DEB):", min_value=0.0, step=1.0)
    index_fin = st.number_input("العداد الحالي (INDEX FIN):", min_value=0.0, step=1.0)
    solde_init = st.number_input("الرصيد المتبقي 01 (RESTE 01):", min_value=0.0, step=1.0)
    chargement = st.number_input("المبلغ المشحون (CHARGEMENT):", min_value=0.0, step=1.0)
    st.subheader("⛽ مبالغ البونات")
    bons_input = st.text_area("أدخل المبالغ (افصل بينها بمسافة):")

if index_fin > 0:
    try:
        bons_list = [float(x) for x in bons_input.split() if x.strip()]
        total_consom_da = sum(bons_list)
        km_parcourus = index_fin - index_prec
        reste_31 = solde_init + chargement - total_consom_da
        
        if km_parcourus > 0:
            litres = total_consom_da / prix_litre
            moyenne_val = (litres / km_parcourus) * 100
        else:
            moyenne_val = 0.0

        st.markdown("---")
        st.subheader("📄 معاينة التقرير النهائي")
        add_print_button()

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("المسافة المقطوعة", f"{km_parcourus:,.0f} KM")
        c2.metric("إجمالي الاستهلاك", f"{total_consom_da:,.2f} DA")
        c3.metric("الرصيد النهائي", f"{reste_31:,.2f} DA")
        c4.metric("المعدل (L/100)", f"{moyenne_val:.2f}")

        immat_fixe = "00341-318-25"
        final_data = {
            "N° Carte": [n_carte_input],
            "BUREAU": [bureau_selected],
            "IMMATRICUL.": [immat_fixe],
            "INDEX DEB": [f"{index_prec:,.0f}"],
            "INDEX FIN": [f"{index_fin:,.0f}"],
            "KM MOIS": [f"{km_parcourus:,.0f}"],
            "MOY/100": [f"{moyenne_val:.2f}"],
            "RESTE 01": [f"{solde_init:,.2f}"],
            "CONS. DA": [f"{total_consom_da:,.2f}"],
            "RESTE 31": [f"{reste_31:,.2f}"]
        }
        st.table(pd.DataFrame(final_data))
    except Exception as e:
        st.error("خطأ في البيانات المدخلة")
else:
    st.info("💡 أدخل قراءة العداد للبدء")
