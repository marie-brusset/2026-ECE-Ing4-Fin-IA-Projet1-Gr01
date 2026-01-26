import streamlit as st
from wordle_csp import WordleCSP
from llm_agent import llm_decision

# ------------------------
# Configuration de la page
# ------------------------
st.set_page_config(
    page_title="Wordle CSP + LLM",
    page_icon="🟩",
    layout="centered"
)

# ------------------------
# Chargement du dictionnaire (cache)
# ------------------------
@st.cache_data
def charger_dictionnaire(fichier):
    with open(fichier, "r") as f:
        return [l.strip() for l in f if len(l.strip()) == 5]

dictionnaire = charger_dictionnaire("dictionary.txt")

# ------------------------
# Initialisation de la session
# ------------------------
if "csp" not in st.session_state:
    st.session_state.csp = WordleCSP()
    st.session_state.historique_partie = []
    st.session_state.historique_global = []
    st.session_state.dernier_mot = None

# ------------------------
# Titre
# ------------------------
st.markdown(
    """
    <h1 style='text-align:center;'>🟩🟨⬜ Solveur Wordle par CSP + LLM</h1>
    <p style='text-align:center; color:grey;'>
    Programmation par contraintes & agent décisionnel
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# ------------------------
# Entrée utilisateur
# ------------------------
st.subheader("🎮 Entrée utilisateur")

col1, col2 = st.columns(2)

with col1:
    mot = st.text_input("Mot proposé", max_chars=5)

with col2:
    feedback = st.text_input("Feedback (G / Y / X)", max_chars=5)

# ------------------------
# Bouton Valider
# ------------------------
if st.button("✅ Valider", use_container_width=True):

    if len(mot) != 5 or not mot.isalpha():
        st.error("❌ Le mot doit contenir exactement 5 lettres.")
    elif len(feedback) != 5 or any(c not in "GYX" for c in feedback.upper()):
        st.error("❌ Le feedback doit contenir uniquement G, Y ou X.")
    else:
        # Ajout des contraintes CSP
        st.session_state.csp.ajouter_contraintes(
            mot.lower(), feedback.upper()
        )

        # Résolution
        candidats = st.session_state.csp.solutions(dictionnaire)

        # Historique de la partie
        st.session_state.historique_partie.append((mot, feedback))

        st.divider()

        # ------------------------
        # Résultats
        # ------------------------
        st.subheader("📊 Résultats")
        st.info(f"🔎 Nombre de solutions possibles : {len(candidats)}")

        if candidats:
            with st.expander("📋 Afficher tous les mots possibles"):
                texte = "\n".join(candidats)
                st.text_area(
                    "Mots possibles",
                    texte,
                    height=300
                )
        else:
            st.warning("Aucune solution possible.")

        # ------------------------
        # LLM
        # ------------------------
        explication, proposition = llm_decision(candidats)

        st.subheader("🤖 Proposition du LLM")
        st.write(explication)

        if proposition:
            st.session_state.dernier_mot = proposition
            st.success(f"Mot suggéré : **{proposition}**")

# ------------------------
# Historique de la partie
# ------------------------
if st.session_state.historique_partie:
    st.divider()
    st.subheader("📜 Partie en cours")
    st.table(
        [{"Mot": m, "Feedback": f} for m, f in st.session_state.historique_partie]
    )

# ------------------------
# Historique global
# ------------------------
if st.session_state.historique_global:
    st.divider()
    st.subheader("📚 Historique global")
    for i, partie in enumerate(st.session_state.historique_global, 1):
        st.markdown(f"**Partie {i}**")
        st.table(
            [{"Mot": m, "Feedback": f} for m, f in partie]
        )

# ------------------------
# Nouvelle partie
# ------------------------
st.divider()
if st.button("🔄 Nouvelle partie"):
    if st.session_state.historique_partie:
        st.session_state.historique_global.append(
            st.session_state.historique_partie.copy()
        )

    st.session_state.csp = WordleCSP()
    st.session_state.historique_partie = []
    st.session_state.dernier_mot = None

    st.success("🆕 Nouvelle partie lancée")
