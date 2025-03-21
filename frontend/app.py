import streamlit as st
import requests

# Backend API URL (replace with your deployed Render URL)
BACKEND_URL = "https://ai-document-search.onrender.com"   # here we have to give backend url from render

st.title("📄 AI-Powered Document Search")

# Upload File Section
st.header("Upload a Document")
uploaded_file = st.file_uploader("Choose a PDF file...", type=["pdf"])

if uploaded_file is not None:
    files = {"file": uploaded_file.getvalue()}
    response = requests.post(f"{BACKEND_URL}/upload", files=files)
    if response.status_code == 200:
        st.success("✅ File uploaded and indexed successfully!")
    else:
        st.error("❌ Failed to upload file.")

# Search Section
st.header("Search Documents")
query = st.text_input("Enter your query:")
if st.button("🔍 Search"):
    if query:
        response = requests.get(f"{BACKEND_URL}/search", params={"query": query})
        if response.status_code == 200:
            results = response.json().get("results", [])
            if results:
                st.subheader("📄 Matching Documents:")
                for result in results:
                    st.write(f"🔹 **{result['filename']}** (Score: {result['distance']:.2f})")
            else:
                st.warning("⚠️ No matching documents found.")
        else:
            st.error("❌ Search failed.")
