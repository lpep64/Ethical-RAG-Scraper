import streamlit as st
import requests

st.title("Subreddit Q&A Expert")
question = st.text_input("Enter your question:")
if st.button("Submit"):
    if question.strip():
        response = requests.post("http://localhost:8000/query", json={"question": question})
        if response.ok:
            data = response.json()
            st.markdown(f"**Answer:**\n{data['answer']}")
            st.markdown("**Sources:**")
            for url in data['sources']:
                st.markdown(f"- [{url}]({url})")
        else:
            st.error("API error: " + response.text)
