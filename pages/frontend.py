import streamlit as st
import requests

API_URL = "http://localhost:8000/ask"  # Update with your backend URL

st.title("FAQ Chatbot with RAG")

# Chat-like interfacre for user input

if "messages" not in st.session_state:
    st.session_state.messages = []

# Input box
user_input = st.text_input("You:","")

if st.button("Send") and user_input:
    # call the backend API
    response = requests.post(API_URL, json={"question": user_input})
    data = response.json()

    #Save conversation
    st.session_state["messages"].append(("user", user_input)
                                        )
    st.session_state["messages"].append(("bot", data.get("generated_answer", "Sorry, I couldn't generate an answer.")))

   # Display chat history
    for role, msg in st.session_state["messages"]:
        if role == "user":
            st.markdown(f"**You:** {msg}")
        else:
            st.markdown(f"**Bot:** {msg}") 