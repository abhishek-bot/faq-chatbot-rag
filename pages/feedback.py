import streamlit as st
import json
import requests

UNMATCHED_FILE = "data/unmatched_queries.json"
API_URL = "http://localhost:8000/feedback"

st.title("FAQ Feedback Review")

# Load unmatched queries
try:
    with open(UNMATCHED_FILE, "r", encoding="utf-8") as f:
        unmatched = json.load(f)
except FileNotFoundError:
    unmatched = []

# Track current index
if "current_index" not in st.session_state:
    st.session_state["current_index"] = 0

total = len(unmatched)

if total == 0:
    st.success("🎉 All queries have been reviewed! No unanswered questions remain.")
else:
    i = st.session_state["current_index"]
    query = unmatched[i]["query"]

    # Show progress
    st.info(f"Reviewing query {i+1} of {total} — {total - (i+1)} remaining after this")

    st.write(f"**Query:** {query}")
    proposed_answer = f"Sorry, I couldn't find an answer for: '{query}'. Please provide a suitable answer or edit the query for better matching."
    st.write(f"Proposed Answer: {proposed_answer}")

    # Feedback buttons
    if st.button("✅ Accept", key=f"accept_{i}"):
        requests.post(API_URL, json={"question": query, "answer": proposed_answer, "action": "accept"})
        st.success(f"Added {query} to FAQs")
        st.session_state["current_index"] += 1
        st.rerun()   # <-- FIXED

    edited = st.text_area("Edit the answer:", key=f"edit_area_{i}")
    if st.button("Save Edit", key=f"save_edit_{i}"):
        requests.post(API_URL, json={"question": query, "answer": edited, "action": "edit"})
        st.success(f"Edited answer for {query} added to FAQs")
        st.session_state["current_index"] += 1
        st.rerun()   # <-- FIXED

    if st.button("❌ Reject", key=f"reject_{i}"):
        requests.post(API_URL, json={"question": query, "answer": "", "action": "reject"})
        st.error(f"Rejected {query}")
        st.session_state["current_index"] += 1
        st.rerun()   # <-- FIXED

    # Navigation
    if st.button("➡️ Next"):
        if st.session_state["current_index"] < total - 1:
            st.session_state["current_index"] += 1
            st.rerun()   # <-- FIXED
        else:
            st.success("🎉 You’ve reached the end of unanswered queries.")