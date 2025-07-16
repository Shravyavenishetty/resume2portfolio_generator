import streamlit as st
import streamlit.components.v1 as components
from pdfminer.high_level import extract_text
from github import Github
import io
import os
import zipfile
import re
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from components.hero import hero
from components.how_it_works import how_it_works
from components.template_showcase import template_showcase
from components.portfolio_editor import portfolio_editor

# Load environment variables
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
VERCEL_TOKEN = os.getenv("VERCEL_TOKEN")

# Path settings
current_dir = os.path.dirname(__file__)
css_file = os.path.join(current_dir, "styles", "main.css")
template_dir = os.path.join(current_dir, "templates")

# Page configuration
st.set_page_config(page_title="Resume2Portfolio", page_icon="🚀", layout="wide")

# Load CSS
with open(css_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Parse resume
def parse_resume(pdf_content):
    try:
        text = extract_text(io.BytesIO(pdf_content))
        parsed_data = {
            "name": "",
            "summary": "",
            "skills": [],
            "education": [],
            "experience": [],
            "projects": [],
            "contact": ""
        }
        lines = text.split("\n")
        for i, line in enumerate(lines):
            line = line.strip()
            if not parsed_data["name"] and i == 0:
                parsed_data["name"] = line
            elif re.match(r"^(Summary|Profile|Objective)", line, re.I):
                parsed_data["summary"] = lines[i + 1].strip() if i + 1 < len(lines) else ""
            elif re.match(r"^(Skills|Technical Skills)", line, re.I):
                parsed_data["skills"] = [s.strip() for s in lines[i + 1].split(",") if i + 1 < len(lines) and lines[i + 1].strip()]
            elif re.match(r"^(Education|Academic)", line, re.I):
                parsed_data["education"].append(lines[i + 1].strip() if i + 1 < len(lines) else "")
            elif re.match(r"^(Experience|Work)", line, re.I):
                parsed_data["experience"].append(lines[i + 1].strip() if i + 1 < len(lines) else "")
            elif re.match(r"^(Projects|Portfolio)", line, re.I):
                parsed_data["projects"].append(lines[i + 1].strip() if i + 1 < len(lines) else "")
            elif re.match(r"^(Contact|Email|Phone)", line, re.I):
                parsed_data["contact"] = lines[i + 1].strip() if i + 1 < len(lines) else ""
        parsed_data["summary"] = enhance_summary(parsed_data["summary"])
        return parsed_data
    except Exception as e:
        st.error(f"Error parsing PDF: {str(e)}")
        return None

# Simulate OpenAI GPT-4 enhancement
def enhance_summary(summary):
    # Placeholder: Replace with OpenAI GPT-4 API call
    return f"Enhanced: {summary or 'Professional with diverse experience in technology and innovation.'}"

# Generate portfolio files
def generate_portfolio_files(parsed_data, theme, output_type):
    if theme not in ["light", "glassmorphism", "terminal"]:
        theme = "light"
    if output_type not in ["html", "tailwind"]:
        output_type = "html"
    folder = os.path.join(template_dir, theme, output_type)
    files = {}
    with open(os.path.join(folder, "index.html"), "r") as f:
        html = f.read()
    html = html.replace("{{name}}", parsed_data["name"])
    html = html.replace("{{summary}}", parsed_data["summary"])
    html = html.replace("{{skills}}", ", ".join(parsed_data["skills"]))
    html = html.replace("{{education}}", "<br>".join(parsed_data["education"]))
    html = html.replace("{{experience}}", "<br>".join(parsed_data["experience"]))
    html = html.replace("{{projects}}", "<br>".join(parsed_data["projects"]))
    html = html.replace("{{contact}}", parsed_data["contact"])
    files["index.html"] = html
    with open(os.path.join(folder, "styles.css"), "r") as f:
        files["styles.css"] = f.read()
    return files

# Generate portfolio preview
def generate_preview(parsed_data, theme, output_type):
    files = generate_portfolio_files(parsed_data, theme, output_type)
    html_content = files["index.html"]
    css_content = files["styles.css"]
    return f"""
        <style>{css_content}</style>
        {html_content}
    """

# Create ZIP file
def create_zip(files):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file_name, content in files.items():
            zip_file.writestr(file_name, content)
    zip_buffer.seek(0)
    return zip_buffer

# Deploy to GitHub and Vercel
def deploy_to_vercel(parsed_data, theme, output_type, github_token, vercel_token):
    try:
        files = generate_portfolio_files(parsed_data, theme, output_type)
        repo_name = f"portfolio-{parsed_data.get('name', 'user').replace(' ', '-').lower()}-{int(datetime.now().timestamp())}"
        g = Github(github_token)
        user = g.get_user()
        repo = user.create_repo(repo_name, private=False, auto_init=False)
        for file_path, content in files.items():
            repo.create_file(file_path, f"Add {file_path}", content, branch="main")
        repo_url = repo.html_url
        headers = {"Authorization": f"Bearer {vercel_token}"}
        payload = {
            "name": repo_name,
            "gitRepository": {"type": "github", "repo": repo_url.replace("https://github.com/", "")}
        }
        response = requests.post("https://api.vercel.com/v10/projects", json=payload, headers=headers)
        if response.status_code in [200, 201]:
            return repo_url, response.json().get("domain", "Deployment in progress")
        else:
            st.error(f"Vercel deployment failed: {response.text}")
            return repo_url, None
    except Exception as e:
        st.error(f"Error deploying: {str(e)}")
        return None, None

# Main app
def main():
    hero()
    how_it_works()
    st.markdown("---")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.header("Upload Your Resume")
        uploaded_file = st.file_uploader("Choose a PDF resume", type=["pdf"])
        theme, output_type = template_showcase()
    with col2:
        st.header("Deployment Tokens")
        github_token = st.text_input("GitHub Token", type="password", value=GITHUB_TOKEN or "")
        vercel_token = st.text_input("Vercel Token", type="password", value=VERCEL_TOKEN or "")
    if uploaded_file:
        with st.spinner("Parsing resume..."):
            pdf_content = uploaded_file.read()
            parsed_data = parse_resume(pdf_content)
        if parsed_data:
            st.header("Portfolio Preview")
            components.html(generate_preview(parsed_data, theme, output_type), height=600, scrolling=True)
            edited_data = portfolio_editor(parsed_data)
            if st.button("Download Portfolio"):
                with st.spinner("Generating portfolio..."):
                    files = generate_portfolio_files(edited_data, theme, output_type)
                    zip_buffer = create_zip(files)
                    st.download_button(
                        label="Download ZIP",
                        data=zip_buffer,
                        file_name=f"portfolio_{theme}_{output_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                        mime="application/zip"
                    )
            if st.button("Deploy to Vercel") and github_token and vercel_token:
                with st.spinner("Deploying to Vercel..."):
                    repo_url, vercel_domain = deploy_to_vercel(edited_data, theme, output_type, github_token, vercel_token)
                    if repo_url:
                        st.success(f"GitHub Repository: [{repo_url}]({repo_url})")
                    if vercel_domain:
                        st.success(f"Vercel Domain: {vercel_domain}")

if __name__ == "__main__":
    main()