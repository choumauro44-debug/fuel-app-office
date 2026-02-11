import streamlit as st
import streamlit.components.v1 as components

# Configuration de la page
st.set_page_config(page_title="Gestion Carburant - Algérie Poste", layout="wide")

# --- Barre latérale (Sidebar) ---
with st.sidebar:
    st.header("📅 Paramètres")
    months = ["JANVIER", "FEVRIER", "MARS", "AVRIL", "MAI", "JUIN", "JUILLET", "AOUT", "SEPTEMBRE", "OCTOBRE", "NOVEMBRE", "DECEMBRE"]
    sel_month = st.selectbox("Mois:", months)
    sel_year = st.selectbox("Année:", [2025, 2026, 2027], index=1)
    
    st.header("📋 Informations")
    bureau = st.selectbox("Bureau / CDD:", ["cdd ziadia", "cdd zighoud youcef", "cdd nouvel ville", "cdd 20 aout"])
    n_carte = st.text_input("N° Carte:", value="9887")
    immat = st.text_input("Immatriculation:", value="00341-318-25")
    prix_litre = st.number_input("Prix du litre (DA):", value=45.60)
    
    st.header("📊 Index Compteur")
    idx_prec = st.number_input("Index Précédent:", min_value=0.0, step=1.0)
    idx_fin = st.number_input("Index Actuel (Considéré):", min_value=0.0, step=1.0)
    
    st.header("💰 Finances")
    solde_init = st.number_input(f"Reste au 01/{sel_month}:", min_value=0.0)
    chargement = st.number_input("Chargement (DA):", min_value=0.0)

    st.header("⛽ Bons de Carburant (5)")
    b1 = st.number_input("Montant Bon 1", min_value=0.0)
    b2 = st.number_input("Montant Bon 2", min_value=0.0)
    b3 = st.number_input("Montant Bon 3", min_value=0.0)
    b4 = st.number_input("Montant Bon 4", min_value=0.0)
    b5 = st.number_input("Montant Bon 5", min_value=0.0)

# --- Calculs ---
total_consom = b1 + b2 + b3 + b4 + b5
km = idx_fin - idx_prec
reste_fin = solde_init + chargement - total_consom
moyenne = ((total_consom / prix_litre) / km * 100) if km > 0 else 0.0

# --- Affichage du Rapport ---
if idx_fin > 0:
    st.success("✅ Rapport généré avec succès!")
    
    # Structure HTML/CSS du tableau officiel
    html_layout = f"""
    <div style="font-family: Arial, sans-serif; background-color: white; padding: 20px; color: black;">
        <style>
            table {{ width: 100%; border-collapse: collapse; border: 2.5px solid black; }}
            th, td {{ border: 1.5px solid black; padding: 12px; text-align: center; font-weight: bold; font-size: 13px; color: black; }}
            .header-info {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }}
            @media print {{ .no-print {{ display: none; }} }}
        </style>
        
        <button class="no-print" onclick="window.print()" style="width: 100%; padding: 15px; margin-bottom: 20px; cursor: pointer; font-weight: bold; background-color: #f8f9fa; border: 2px solid black;">
            🖨️ IMPRIMER LE RAPPORT OFFICIEL
        </button>

        <div class="header-info">
            <div style="font-size: 16px;">DIRECTION DE WILAYA<br>{bureau.upper()}</div>
            <h2 style="text-decoration: underline; text-align: center;">SITUATION CARBURANT MOIS DE {sel_month} {sel_year}</h2>
            <div style="border: 2px solid black; padding: 10px; font-weight: bold;">PROPRE</div>
        </div>

        <table>
            <thead>
                <tr style="background-color: #f0f0f0;">
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
                <tr style="background-color: #f0f0f0;">
                    <th>FIN DU MOIS CONSIDERE</th>
                    <th>FIN DU MOIS PRECEDENT</th>
                </tr>
            </thead>
            <tbody>
                <tr style="height: 60px;">
                    <td>01</td>
                    <td>{n_carte}</td>
                    <td>{bureau.upper()}</td>
                    <td>{immat}</td>
                    <td>{idx_fin:,.0f}</td>
                    <td>{idx_prec:,.0f}</td>
                    <td>{km:,.0f} km</td>
                    <td>{moyenne:.1f}</td>
                    <td>{solde_init:,.2f}</td>
                    <td>{chargement:,.2f}</td>
                    <td>{total_consom:,.2f}</td>
                    <td>{reste_fin:,.2f}</td>
                </tr>
            </tbody>
        </table>

        <div style="margin-top: 80px; display: flex; justify-content: space-between; font-weight: bold; padding: 0 40px;">
            <p style="text-decoration: underline;">Signature du Chauffeur</p>
            <p style="text-decoration: underline;">Le Chef de Bureau</p>
        </div>
    </div>
    """
    # Affichage via le composant sécurisé
    components.html(html_layout, height=650, scrolling=True)
else:
    st.info("💡 Veuillez saisir l'Index Actuel dans la barre latérale pour afficher le tableau.")
