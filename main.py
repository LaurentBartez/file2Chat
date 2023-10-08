import streamlit as st
from streamlit_chat import message
import tempfile
import requests

# api-endpoint
URL = "http://127.0.0.1:8000"

def get_history():
    if 'history' in st.session_state:
        chatHistory = ""
        for history in st.session_state['history']:
            chatHistory+= "&history=" + history['content']
        if len(st.session_state['history']) == 1:
            chatHistory+= "&history=" + ' '
        return chatHistory
    
def generate_response(prompt):
    chatHistory = get_history()
    r = requests.get(url=URL+"/chat/?prompt="+prompt+chatHistory)
    print("Answer")
    print(r.json())
    st.session_state['history'].append({"role": "user", "content": prompt})
    return r.json()["answer"]


st.title("Talk to that file")

tabChat, tabDocs = st.tabs(["Chat", "Docs"])

with tabChat:
    
    # Initialize chat history
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    # Initialize messages
    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello ! Ask me about "]#+ uploaded_file.name + " 🤗"]

    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hey ! 👋"]


    response_container = st.container()
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("Query:", placeholder="Enter your question...", key='input')
            submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        # st.session_state['generated'].append("Generating answer...")
        output = generate_response(user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)


    if st.session_state['generated']:
        with response_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
                message(st.session_state["generated"][i], key=str(i))

with tabDocs:
    uploaded_file = st.file_uploader("Upload File", type=["pdf"])
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
            print(uploaded_file)
            headers = {
                'Content-Type': 'multipart/form-data'
            }
            files = {'file':(tmp_file.name, uploaded_file.getvalue())}
            r =requests.post(url=URL + "/uploadFiles?uploadFile",files=files)
