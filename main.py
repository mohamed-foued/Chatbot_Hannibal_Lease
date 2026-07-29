"""
Point d'entrée Streamlit — Hannibal Lease
- Chatbot accessible SANS connexion (questions générales)
- Connexion / Inscription uniquement si l'utilisateur veut un leasing
"""

import streamlit as st

st.set_page_config(
    page_title="Hannibal Lease - Assistant",
    page_icon="logo.png",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Initialisation de la session
# ---------------------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state["page"] = "chatbot"      # on arrive direct sur le chat
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ---------------------------------------------------------------------------
# Routeur : login / register sont des overlays optionnels
# ---------------------------------------------------------------------------
page = st.session_state["page"]

if page == "login":
    from login import afficher_login
    afficher_login()
    st.stop()

if page == "register":
    from register import afficher_inscription
    afficher_inscription()
    st.stop()

# ---------------------------------------------------------------------------
# CSS global
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; box-sizing: border-box; }

.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
}
.stChatMessage { border-radius: 12px; }
h1 { color: #ffffff !important; }

.subtitle {
    color: #b0b0b0;
    text-align: center;
    font-size: 1rem;
    margin-bottom: 1.5rem;
}

/* Badge utilisateur connecté */
.user-badge {
    background: rgba(124,110,245,0.15);
    border: 1px solid rgba(124,110,245,0.4);
    border-radius: 20px;
    padding: 0.3rem 0.9rem;
    color: #c8c8e8;
    font-size: 0.82rem;
    display: inline-block;
    margin-bottom: 0.8rem;
}

/* Boutons sidebar */
section[data-testid="stSidebar"] {
    background: rgba(15,12,41,0.85);
    border-right: 1px solid rgba(255,255,255,0.08);
}
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label {
    color: #c8c8e8 !important;
}

/* Bouton principal violet */
.stButton > button {
    background: linear-gradient(135deg, #7c6ef5, #5a4de0) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.5rem 1.2rem !important;
    font-weight: 600 !important;
    transition: transform .15s, box-shadow .15s;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(124,110,245,.4) !important;
}

/* Tip box */
.tip-box {
    background: rgba(124,110,245,0.12);
    border-left: 3px solid #7c6ef5;
    border-radius: 8px;
    padding: 0.7rem 1rem;
    color: #c0b8f0;
    font-size: 0.85rem;
    margin-top: 0.8rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Sidebar : connexion / compte
# ---------------------------------------------------------------------------
with st.sidebar:
    st.image("logo.png", width=80)
    st.markdown("## Hannibal Lease")
    st.markdown("---")

    if "client_id" in st.session_state:
        # --- Utilisateur connecté ---
        prenom = st.session_state.get("client_prenom", "")
        nom    = st.session_state.get("client_nom", "")
        st.markdown(f"**Connecte :** {prenom} {nom}")
        st.markdown(" ")
        if st.button("Se deconnecter"):
            for k in ["client_id", "client_nom", "client_prenom", "messages"]:
                st.session_state.pop(k, None)
            st.session_state["page"] = "chatbot"
            st.rerun()
    else:
        # --- Visiteur non connecté ---
        st.markdown("**Vous souhaitez un leasing ?**")
        st.markdown(
            '<p style="color:#a0a0c0;font-size:.85rem;">'
            "Créez un compte pour ouvrir un dossier et suivre votre demande."
            "</p>",
            unsafe_allow_html=True,
        )
        if st.button("Creer un compte", key="sb_register"):
            st.session_state["page"] = "register"
            st.rerun()

        st.markdown(" ")
        st.markdown("**Déjà client ?**")
        if st.button("Se connecter", key="sb_login"):
            st.session_state["page"] = "login"
            st.rerun()

        st.markdown(
            '<div class="tip-box">'
            "Vous pouvez aussi poser vos questions directement sans vous connecter."
            "</div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown(
        '<p style="color:#606080;font-size:.75rem;">© 2026 Hannibal Lease</p>',
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# En-tête principal
# ---------------------------------------------------------------------------
col1, col2 = st.columns([1, 5])
with col1:
    st.image("logo.png", width=70)
with col2:
    st.title("Hannibal Lease")

if "client_id" in st.session_state:
    prenom = st.session_state.get("client_prenom", "")
    st.markdown(
        f'<span class="user-badge">Connecte : {prenom} {st.session_state.get("client_nom","")}</span>',
        unsafe_allow_html=True,
    )

st.markdown(
    '<p class="subtitle">Votre assistant intelligent de leasing</p>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Message d'accueil (une seule fois)
# ---------------------------------------------------------------------------
if not st.session_state["messages"]:
    prenom_accueil = st.session_state.get("client_prenom", "")
    salutation = f"Bonjour {prenom_accueil} !" if prenom_accueil else "Bonjour !"
    st.session_state["messages"].append({
        "role": "assistant",
        "content": (
            f"{salutation} Je suis l'assistant virtuel de Hannibal Lease.\n\n"
            "Je peux vous aider avec :\n"
            "- Recherche de vehicules et prix\n"
            "- Documents requis pour un dossier de credit\n"
            "- Consultation du statut de votre dossier\n"
            "- Verification de votre CIN\n"
            "- Informations generales sur le leasing en Tunisie\n\n"
            "Si vous souhaitez **demander un leasing**, utilisez le menu lateral "
            "pour creer un compte ou vous connecter."
        ),
    })

# ---------------------------------------------------------------------------
# Affichage de l'historique
# ---------------------------------------------------------------------------
from backend.ai.chatbot import repondre

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------------------------------------------------------
# Saisie utilisateur
# ---------------------------------------------------------------------------
if prompt := st.chat_input("Posez votre question..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Détection : l'utilisateur veut créer un dossier / leasing
    mots_leasing = ["leasing", "dossier", "financement", "crédit", "credit",
                    "créer un compte", "creer un compte", "inscription",
                    "s'inscrire", "ouvrir un dossier", "demande de leasing"]
    demande_leasing = any(m in prompt.lower() for m in mots_leasing)

    with st.chat_message("assistant"):
        if demande_leasing and "client_id" not in st.session_state:
            reponse_ia = (
                "Pour initier une demande de leasing ou consulter votre dossier, "
                "vous devez d'abord créer un compte ou vous connecter.\n\n"
                "Utilisez le **menu lateral** (a gauche) pour :\n"
                "- **Creer un compte** si c'est votre premiere demande\n"
                "- **Se connecter** si vous etes deja client\n\n"
                "Pour toute question generale sur le leasing, je suis la !"
            )
            st.markdown(reponse_ia)
        else:
            with st.spinner("Reflexion en cours..."):
                historique_pour_ia = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state["messages"][1:-1]
                ]
                reponse_ia = repondre(prompt, historique_pour_ia)
            st.markdown(reponse_ia)

    st.session_state["messages"].append({"role": "assistant", "content": reponse_ia})
