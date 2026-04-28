import streamlit as st

# Simulation einer Datenbank: PLZ zu Netzbetreiber
plz_mapping = {
    "50667": "Rheinische NETZGesellschaft (RNG)",
    "40210": "Netzgesellschaft Düsseldorf",
    "44135": "Westnetz",
    "52062": "Regionetz",
    "53111": "Bonn-Netz GmbH"
}

st.set_page_config(page_title="WP-Anmelde-Assistent", layout="centered")

st.title("🚀 Wärmepumpen-Anmelde-Tool")
st.subheader("Assistent für steuerbare Verbrauchseinrichtungen (§14a EnWG)")

# SCHRITT 1: Stammdaten
with st.expander("1. Standort & Netzbetreiber", expanded=True):
    plz = st.text_input("Postleitzahl des Objekts", placeholder="z.B. 44135")
    if plz in plz_mapping:
        nb = plz_mapping[plz]
        st.success(f"Zuständiger Netzbetreiber erkannt: **{nb}**")
    elif plz:
        nb = "Unbekannter Betreiber (bitte manuell wählen)"
        st.warning(nb)
    else:
        nb = ""

# SCHRITT 2: Technische Daten
if nb:
    with st.expander("2. Technische Details der Wärmepumpe", expanded=True):
        leistung = st.number_input("Maximale Bezugsleistung (in kW)", min_value=0.0, step=0.1, value=11.7)
        
        # Logik-Check §14a
        if leistung > 4.2:
            st.info("ℹ️ Anlage > 4,2 kW: Verpflichtende Teilnahme an Steuerung nach §14a EnWG.")
            modul = st.radio("Gewähltes Vergütungsmodul:", ["Modul 1 (Pauschale)", "Modul 2 (Arbeitspreis-Rabatt)"])
        else:
            st.success("Anlage < 4,2 kW: Nur Informationspflicht, keine aktive Steuerung nötig.")
            modul = "N/A"

        ep_id = st.text_input("Erzeugungspunkt-ID (EP-ID)", placeholder="z.B. 1209778")
        zaehler = st.text_input("Aktuelle Zählernummer")

    # SCHRITT 3: Westnetz-Spezifische Logik (basierend auf deinen PDF-Notizen)
    if "Westnetz" in nb:
        with st.expander("3. Westnetz Spezial-Check", expanded=True):
            st.warning("⚠️ Westnetz-Hinweis: Anlage erst NACH Inbetriebnahme im Portal final melden.")
            gas_ab = st.checkbox("Muss ein Gaszähler abgemeldet werden? (Öl-auf-Gas / Gas-auf-WP)")
            foto_check = st.checkbox("Zählerfoto im Kundenordner vorhanden?")
            
            if not foto_check:
                st.error("Bitte Zählerfoto hochladen, bevor die Anmeldung gestartet wird.")

    # SCHRITT 4: Ausgabe / Zusammenfassung
    if st.button("Anmeldedaten generieren"):
        st.divider()
        st.success("Zusammenfassung für das Installateur-Portal:")
        summary = f"""
        **Netzbetreiber:** {nb}
        **Leistung:** {leistung} kW
        **Modul:** {modul}
        **EP-ID:** {ep_id}
        **Zählernummer:** {zaehler}
        {'**Status:** Gasabmeldung erforderlich' if 'gas_ab' in locals() and gas_ab else ''}
        """
        st.code(summary, language="markdown")
        st.button("Als PDF für Backoffice exportieren (Simulation)")
