import streamlit as st
import requests
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

st.title("🦙 AI Resume Builder using Meta LLaMA")

name = st.text_input("Enter Name")
email = st.text_input("Enter Email")
skills = st.text_area("Enter Skills")

template = st.selectbox("Select Template",
["Classic","Modern","Professional","Creative"])

# LLaMA FUNCTION
def generate_with_llama(prompt):
    url = "http://localhost:11434/api/generate"

    data = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=data)
    return response.json()['response']

# PDF
def create_pdf(name,email,skills,summary):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(name, styles['Title']))
    story.append(Paragraph(email, styles['Normal']))
    story.append(Spacer(1,20))

    story.append(Paragraph("Skills", styles['Heading2']))
    story.append(Paragraph(skills, styles['Normal']))
    story.append(Spacer(1,20))

    story.append(Paragraph("Professional Summary", styles['Heading2']))
    story.append(Paragraph(summary, styles['Normal']))

    doc.build(story)
    buffer.seek(0)
    return buffer

# BUTTON
if st.button("Generate Resume"):
    if not name or not skills:
        st.warning("Enter all details")
    else:
        prompt=f"""
        Create professional resume summary.
        Name:{name}
        Skills:{skills}
        Template:{template}
        """

        summary=generate_with_llama(prompt)

        st.subheader("Generated Summary")
        st.write(summary)

        pdf=create_pdf(name,email,skills,summary)
        st.download_button("Download Resume PDF",pdf,"resume.pdf")