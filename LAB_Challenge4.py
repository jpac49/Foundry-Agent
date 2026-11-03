import streamlit as st
from azure.identity import DeviceCodeCredential
from azure.ai.projects import AIProjectClient

FOUNDRY_PROJECT_ENDPOINT = "https://foundry-tecnun-resource.services.ai.azure.com/api/projects/foundry-tecnun-project"
FOUNDRY_AGENT_NAME = "agent-challenge-4"

st.set_page_config(page_title="Movie Critic Agent", page_icon="🎬")
st.title("🎬 Movie Critic Agent - Foundry")

@st.cache_resource
def get_agent_client():
    
    credential = DeviceCodeCredential()
    
    project = AIProjectClient(
        endpoint=FOUNDRY_PROJECT_ENDPOINT,
        credential=credential,
    )
    return project.get_openai_client(agent_name=FOUNDRY_AGENT_NAME)

openai_client = get_agent_client()

# Inicializar conversación en la sesión
if "conversation_id" not in st.session_state:
    conversation = openai_client.conversations.create()
    st.session_state.conversation_id = conversation.id

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial de mensajes
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Entrada de usuario
if prompt := st.chat_input("Hazme una pregunta sobre cine..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response = openai_client.responses.create(
                conversation=st.session_state.conversation_id,
                input=prompt,
            )
            reply = response.output_text
            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})