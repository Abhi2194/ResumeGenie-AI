import streamlit as st
import docx2txt
from PyPDF2 import PdfReader
import json

# ----------------------------
# Paywall / Access Control
# ----------------------------

st.set_page_config(page_title="Resume Genie AI", layout="centered")
st.title("🔒 Resume Genie AI – Premium Access")

user_code = st.text_input("Enter your 6-digit access code to unlock (₹499 users only):", type="password")

if user_code != "ABHI499":
    st.warning("🛑 This is a paid tool. Please send ₹499 to unlock all features.")
    st.markdown("📲 **UPI ID**: `abhijeet@upi`  \n💬 DM me on WhatsApp after payment to receive your access code.")
    st.stop()

st.success("✅ Access granted. Welcome to Resume Genie AI!")

# ----------------------------
# ATS Resume Checker Section
# ----------------------------

st.markdown("## 📄 Resume ATS Score Checker")

with open("skills.json", "r") as f:
    skill_data = json.load(f)

job_roles = list(skill_data.keys())
selected_role = st.selectbox("Select Job Role", job_roles)
uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text.lower()

def extract_text_from_docx(docx_file):
    return docx2txt.process(docx_file).lower()

def calculate_ats_score(resume_text, required_skills):
    found = []
    missing = []
    for skill in required_skills:
        if skill.lower() in resume_text:
            found.append(skill)
        else:
            missing.append(skill)
    score = int((len(found) / len(required_skills)) * 100)
    return score, found, missing

if uploaded_file:
    file_type = uploaded_file.name.split('.')[-1]
    if file_type == "pdf":
        resume_text = extract_text_from_pdf(uploaded_file)
    elif file_type == "docx":
        resume_text = extract_text_from_docx(uploaded_file)
    else:
        resume_text = ""

    st.subheader("📊 Resume Analysis Results")
    required_skills = skill_data[selected_role]
    ats_score, found_skills, missing_skills = calculate_ats_score(resume_text, required_skills)

    st.markdown(f"### ✅ ATS Match Score: `{ats_score}%`")
    st.progress(ats_score)

    st.markdown("#### ✅ Skills Found:")
    st.write(", ".join(found_skills) if found_skills else "None")

    st.markdown("#### ❌ Missing Keywords:")
    st.write(", ".join(missing_skills) if missing_skills else "None")

    st.markdown("#### 💡 Tip:")
    st.info("Try to include the missing keywords naturally in your resume to increase your chances.")

# ----------------------------
# Resume Template Downloads
# ----------------------------

st.markdown("## 📥 Download Resume Templates")

with open("Fresher_Resume_Template.docx", "rb") as f:
    st.download_button("📄 Download Fresher Resume", f, file_name="Fresher_Resume_Template.docx")

with open("Experienced_Resume_Template.docx", "rb") as f:
    st.download_button("📄 Download Experienced Resume", f, file_name="Experienced_Resume_Template.docx")

# ----------------------------
# AI Resume Summary Generator
# ----------------------------

st.markdown("## ✍️ AI Resume Summary Generator")
st.info("Fill the form to auto-generate a resume summary")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Your Full Name")
    job_title = st.text_input("Target Job Title (e.g., Data Scientist)")
with col2:
    experience = st.text_input("Years of Experience")
    skills = st.text_area("Key Skills (comma-separated)")

if st.button("📝 Generate Summary"):
    if name and job_title and skills:
        generated_summary = f"{name} is an aspiring {job_title} with {experience} years of experience. Skilled in {skills}. Passionate about solving real-world problems and delivering impactful solutions."
        st.success("✅ Resume Summary:")
        st.markdown(f"🧾 {generated_summary}")
    else:
        st.warning("Please fill all fields to generate summary.")
