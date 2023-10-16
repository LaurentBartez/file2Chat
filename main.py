import streamlit as st
from streamlit_chat import message
import tempfile
import requests
import PyPDF2
import io
import base64

# api-endpoint
URL = "http://127.0.0.1:8000"

def get_history_as_json():
    chatHistory = []
    for history in st.session_state['history']:
        chatHistory.append(history['content'])
    return chatHistory

def generate_response(prompt):
    chatHistory = get_history_as_json()
    payload = {"prompt": prompt,
               "history": chatHistory}
    print(payload)
    r = requests.post(url=URL+"/chat", json=payload)
    
    answer = "Something happened."

    if r.status_code == 200:
        answer = r.json()["answer"]

    history = {"question": prompt,
               "answer": answer}
    st.session_state['history'].append({"role": "user", "content": history})
    print (r.json())
    return answer

def getOnlineStatus():
    isOnline = requests.get(url=URL+"/ping/")
    statusText = ""
    if isOnline.status_code == 204:
        statusText = "Online"
    else:
        statusText = "Offline"
    
    return statusText

def setOpenDocument(document):
    r = requests.get(url=URL+"/files/"+document)
    if r.status_code == 200:
        st.session_state['document'] = base64.b64encode(r.content).decode('utf-8')
    else:
        st.session_state['document'] = None



st.set_page_config(page_title="chat2file", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items={
    "About": "Server is " + getOnlineStatus()
})
st.title("chat2file")

tabChat, tabDocs = st.tabs(["Chat", "Docs"])

with tabChat:
    
    # Initialize chat history
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    # Initialize messages
    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello ! Ask me about "]

    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hey ! 👋"]


    response_container = st.container()
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("Query:", placeholder="Enter your question...", key='input')
            submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        st.session_state['past'].append(user_input)
        print(len(st.session_state['generated']))
        output = generate_response(user_input)
        print(len(st.session_state['generated']))
        st.session_state['generated'].append(output)


    if st.session_state['generated']:
        with response_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
                message(st.session_state["generated"][i], key=str(i))

with tabDocs:
    if 'document' not in st.session_state:
        st.session_state['document'] = None

    uploaded_file = st.file_uploader("Upload File", type=["pdf"])
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
            print(uploaded_file)
            headers = {
                'Content-Type': 'multipart/form-data'
            }
            files = {'file':(uploaded_file.name, uploaded_file.getvalue())}
            print(files)
            r =requests.post(url=URL + "/uploadFiles?uploadFile",files=files)
    
    r = requests.get(url=URL+"/files/")
    filesOnServer = r.json()["files"]
    filesButtons = []
    for i in range(len(filesOnServer)):
        filesButtons.append(st.button(filesOnServer[i], on_click=setOpenDocument, args=[filesOnServer[i]]))

    if st.session_state['document'] is not None:
        base64_pdf = st.session_state['document']
        pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" width="800" height="1200" type="application/pdf">'

        st.markdown(pdf_display, unsafe_allow_html=True)

    
