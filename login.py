"""
Page de connexion — Hannibal Lease
"""

import streamlit as st
from backend.data.auth_utilisateurs import verifier_login


COMMON_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; box-sizing: border-box; }

.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

h1, h2, h3 { color: #ffffff !important; }

.subtitle {
    color: #a0a0c0;
    text-align: center;
    font-size: 1rem;
    margin-bottom: 1.8rem;
}

.stTextInput > label,
.stPasswordInput > label { color: #c8c8e8 !important; font-weight: 500; }

.stTextInput input,
.stPasswordInput input {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 10px !important;
    color: #ffffff !important;
    padding: 0.55rem 0.9rem !important;
    transition: border-color .25s;
}
.stTextInput input:focus,
.stPasswordInput input:focus {
    border-color: #7c6ef5 !important;
    box-shadow: 0 0 0 3px rgba(124,110,245,.25) !important;
}
.stTextInput input::placeholder,
.stPasswordInput input::placeholder { color: rgba(255,255,255,0.35) !important; }

.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #7c6ef5, #5a4de0) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.7rem 1.5rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    transition: transform .15s, box-shadow .15s;
    margin-top: 0.5rem;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(124,110,245,.45) !important;
}

hr { border-color: rgba(255,255,255,0.12); margin: 1.5rem 0; }

.bottom-link {
    text-align: center;
    color: #a0a0c0;
    font-size: 0.9rem;
    margin-top: 0.5rem;
}
</style>
"""


def afficher_login():
    """
    Affiche le formulaire de connexion.
    En cas de succès, enregistre le client dans st.session_state
    et bascule sur la page 'chatbot'.
    """
    st.markdown(COMMON_CSS, unsafe_allow_html=True)

    col_logo, col_title = st.columns([1, 5])
    with col_logo:
        st.image("logo.png", width=60)
    with col_title:
        st.title("Connexion")

    st.markdown(
        '<p class="subtitle">Accédez à votre espace Hannibal Lease.</p>',
        unsafe_allow_html=True,
    )

    # Pré-remplir le login si l'utilisateur vient de s'inscrire
    prefill = st.session_state.pop("prefill_login", "")

    with st.form("form_login"):
        login = st.text_input("Login", value=prefill, placeholder="Votre identifiant")
        mdp   = st.text_input("Mot de passe", type="password", placeholder="••••••••")
        submitted = st.form_submit_button("Se connecter")

    if submitted:
        if not login.strip() or not mdp.strip():
            st.error("Veuillez renseigner votre login et votre mot de passe.")
        else:
            with st.spinner("Vérification..."):
                resultat = verifier_login(login.strip(), mdp)

            if resultat["succes"]:
                st.session_state["client_id"] = resultat["client_id"]
                st.session_state["client_nom"] = resultat["nom"]
                st.session_state["client_prenom"] = resultat["prenom"]
                st.session_state["page"] = "chatbot"
                st.rerun()
            else:
                st.error(resultat["message"])

    st.markdown("---")
    st.markdown('<div class="bottom-link">Pas encore de compte ?</div>', unsafe_allow_html=True)
    if st.button("Créer un compte", key="btn_vers_inscription"):
        st.session_state["page"] = "register"
        st.rerun()


if __name__ == "__main__":
    st.set_page_config(
        page_title="Connexion — Hannibal Lease",
        page_icon="logo.png",
        layout="centered",
    )
    afficher_login()
