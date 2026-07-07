import streamlit as st
from backend.ai.chatbot import repondre  

st.set_page_config(
    page_title="Hannibal Lease - Assistant",
    page_icon="logo.png",
    layout="centered"
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }
    .stChatMessage {
        border-radius: 12px;
    }
    h1 {
        color: #ffffff;
    }
    .subtitle {
        color: #b0b0b0;
        text-align: center;
        front-size: 1.1rem;
        margin-bottom: 2rem;
    }
<style>
""",unsafe_allow_html=True)

col1, col2 = st.columns([1, 5])

with col1:
    st.image("logo.png", width=70) 

with col2:
    st.title("Hannibal Lease")

st.markdown('<p class="subtitle">Votre assistant intelligent de leasing</p',
            unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",                             # Line 41
        "content": "Bonjour ! 👋 Je suis l'assistant virtuel de Hannibal Lease. "
                   "Comment puis-je vous aider aujourd'hui ?\n\n"
                   "Je peux vous aider avec :\n"
                   "- 🚗 Recherche de véhicules et prix\n"
                   "- 📋 Documents requis pour un dossier de crédit\n"
                   "- 📂 Consultation du statut de votre dossier\n"
                   "- 🪪 Vérification de votre CIN\n"
                   "- ℹ️ Informations sur le leasing en Tunisie"
    })


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Posez votre question..."):   
    st.session_state.messages.append({"role": "user", "content": prompt})  
    with st.chat_message("user"):                        
        st.markdown(prompt)                             
    with st.chat_message("assistant"):                   
        with st.spinner("Réflexion en cours..."):   
            historique_pour_ia = [                       
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages[1:-1] 
            ]                                            
            reponse_ia = repondre(prompt, historique_pour_ia) 
        st.markdown(reponse_ia)                          
    st.session_state.messages.append({"role": "assistant", "content": reponse_ia})


