import streamlit as st
from streamlit_chat import message
import backend.responseGenerator as rg
import tempfile

def generate_response(prompt, responseGenerator):
    st.session_state['history'].append({"role": "user", "content": prompt})
    return responseGenerator.getResponse(prompt)

st.title("Talk to that file")
uploaded_file = st.sidebar.file_uploader("Upload File", type=["pdf"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    gener = rg.responseGenerator(tmp_file_path)
    
    # Initialize chat history
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    # Initialize messages
    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello ! Ask me about " + uploaded_file.name + " 🤗"]

    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hey ! 👋"]


    response_container = st.container()
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("Query:", placeholder="Enter your question...", key='input')
            submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        output = generate_response(user_input, gener)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)


    if st.session_state['generated']:
        with response_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
                message(st.session_state["generated"][i], key=str(i))