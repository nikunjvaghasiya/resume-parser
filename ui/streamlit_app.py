import streamlit as st
import requests
import os

API_BASE = os.getenv("API_BASE", "http://localhost:8000")

st.title("Resume parser")


upload_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx", "doc"])
if upload_file:
    st.write(f"Uploaded: {upload_file.name}")
    extract_btn = st.button("Extract")
    if extract_btn:
        with st.spinner("Uploading and extracting..."):
            files = {"file": (upload_file.name, upload_file.getvalue())}
            resp = requests.post(f"{API_BASE}/api/upload", files=files)

            if resp.status_code != 200:
                try:
                    error_json = resp.json()
                    st.error(error_json.get("detail", "Unknown error"))
                except:
                    st.error("Server returned non-JSON error response.")
                st.stop()

            try:
                data = resp.json()["parsed_data"]
            except:
                st.error("Invalid JSON response received from backend.")
                st.stop()

            st.success("Extraction successful!")
            st.json(data)

        st.stop()

st.header("Processed Files Dashboard")

if "resume_list" not in st.session_state:
    st.session_state.resume_list = []

if st.button("Load Processed Resumes"):
    try:
        resp = requests.get(f"{API_BASE}/api/resumes")
        resp.raise_for_status()
        st.session_state.resume_list = resp.json()
    except:
        st.error("Backend server not reachable")
        st.stop()

for resume in st.session_state.resume_list:
    st.write(f"{resume['filename']}")
    st.write(f"{resume['created_at']}")

    if st.button(f"View Content ({resume['document_id']})", key=resume["document_id"]):
        detail = requests.get(f"{API_BASE}/api/resume/{resume['document_id']}").json()
        st.json(detail["parsed_json"])