"""
Page d'inscription — Hannibal Lease
Collecte les informations du nouveau client et les insère dans
les tables `clients` et `dossiers` via inscrire_client().
"""

import streamlit as st
from backend.data.auth_utilisateurs import inscrire_client


# CSS partagé (identique à main.py pour l'harmonie visuelle)

COMMON_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; box-sizing: border-box; }

.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

/* Carte centrale */
.register-card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    max-width: 540px;
    margin: 2rem auto;
}

/* Titres */
h1, h2, h3 { color: #ffffff !important; }
.subtitle {
    color: #a0a0c0;
    text-align: center;
    font-size: 1rem;
    margin-bottom: 1.8rem;
}

/* Champs de formulaire */
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

/* Bouton principal */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #7c6ef5, #5a4de0) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.7rem 1.5rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px;
    transition: transform .15s, box-shadow .15s;
    margin-top: 0.5rem;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(124,110,245,.45) !important;
}

/* Divider */
hr { border-color: rgba(255,255,255,0.12); margin: 1.5rem 0; }

/* Lien retour */
.back-link {
    text-align: center;
    color: #a0a0c0;
    font-size: 0.9rem;
    margin-top: 1rem;
}
.back-link span {
    color: #7c6ef5;
    cursor: pointer;
    font-weight: 600;
    text-decoration: underline;
}

/* Alertes Streamlit */
.stAlert { border-radius: 10px !important; }
</style>
"""


# Composant principal

def afficher_inscription():
    """
    Affiche le formulaire d'inscription.
    Si l'inscription réussit, passe l'état de session à 'login'
    pour rediriger vers la page de connexion.
    """
    st.markdown(COMMON_CSS, unsafe_allow_html=True)

    # Logo + titre
    col_logo, col_title = st.columns([1, 5])
    with col_logo:
        st.image("logo.png", width=60)
    with col_title:
        st.title("Créer un compte")
    st.markdown(
        '<p class="subtitle">Rejoignez Hannibal Lease et suivez vos dossiers en temps réel.</p>',
        unsafe_allow_html=True,
    )

    # Formulaire 
    with st.form("form_inscription", clear_on_submit=False):
        st.markdown("#### Informations personnelles")

        col1, col2 = st.columns(2)
        with col1:
            prenom = st.text_input("Prénom *", placeholder="ex. Ahmed")
        with col2:
            nom = st.text_input("Nom *", placeholder="ex. Ben Ali")

        col3, col4 = st.columns(2)
        with col3:
            cin = st.text_input("CIN *", placeholder="8 chiffres", max_chars=8)
        with col4:
            email = st.text_input("Email", placeholder="exemple@email.com")

        st.markdown("---")
        st.markdown("#### Identifiants de connexion")

        login = st.text_input("Login *", placeholder="ex. ahmed_benali")

        col5, col6 = st.columns(2)
        with col5:
            mdp = st.text_input("Mot de passe *", type="password",
                                placeholder="6 caractères minimum")
        with col6:
            mdp_confirm = st.text_input("Confirmer le mot de passe *",
                                        type="password", placeholder="...")

        submitted = st.form_submit_button("Créer mon compte")

    # Traitement 
    if submitted:
        # Vérifications côté client
        champs_vides = [f for f, v in {
            "Prénom": prenom, "Nom": nom, "CIN": cin,
            "Login": login, "Mot de passe": mdp, "Confirmation": mdp_confirm,
        }.items() if not v.strip()]

        if champs_vides:
            st.error(f"Champs obligatoires manquants : {', '.join(champs_vides)}")
        elif mdp != mdp_confirm:
            st.error("Les mots de passe ne correspondent pas.")
        else:
            with st.spinner("Création du compte en cours..."):
                resultat = inscrire_client(
                    login=login,
                    mot_de_passe=mdp,
                    nom=nom,
                    prenom=prenom,
                    cin=cin,
                    email=email,
                )

            if resultat["succes"]:
                st.success(
                    f"Compte cree avec succes ! "
                    f"Votre numero de dossier : **{resultat['numero_dossier']}**. "
                    f"Vous pouvez maintenant vous connecter."
                )
                # Pré-remplir le login pour la page de connexion
                st.session_state["prefill_login"] = login
                # Bouton pour passer à la connexion
                if st.button("Se connecter maintenant"):
                    st.session_state["page"] = "login"
                    st.rerun()
            else:
                st.error(resultat["message"])

    #  Lien retour connexion 
    st.markdown("---")
    st.markdown(
        '<div class="back-link">Vous avez déjà un compte ?</div>',
        unsafe_allow_html=True,
    )
    if st.button("Retour à la connexion", key="btn_retour_login"):
        st.session_state["page"] = "login"
        st.rerun()


# Permet de tester cette page seule : streamlit run register.py
if __name__ == "__main__":
    st.set_page_config(
        page_title="Inscription — Hannibal Lease",
        page_icon="logo.png",
        layout="centered",
    )
    afficher_inscription()
