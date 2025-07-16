from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pdfminer.high_level import extract_text
from github import Github
import io
import os
import zipfile
import re
import requests
from dotenv import load_dotenv
from datetime import datetime

app = FastAPI()

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load environment variables
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
VERCEL_TOKEN = os.getenv("VERCEL_TOKEN")

# Simulated AI parsing (replace with OpenAI API later)
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

        parsed_data["summary"] = f"Enhanced: {parsed_data['summary'] or 'Professional with diverse experience.'}"
        return parsed_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing PDF: {str(e)}")

# Generate portfolio files based on template and frontend type
def generate_portfolio_files(parsed_data, template, frontend_type):
    if template not in ["classic", "glassmorphism", "terminal"]:
        template = "classic"
    if frontend_type not in ["html", "react"]:
        frontend_type = "html"

    folder = f"templates/{template}/{frontend_type}"
    files = {}
    
    if frontend_type == "html":
        with open(f"{folder}/index.html", "r") as f:
            html = f.read()
        html = html.replace("{{name}}", parsed_data["name"])
        html = html.replace("{{summary}}", parsed_data["summary"])
        html = html.replace("{{skills}}", ", ".join(parsed_data["skills"]))
        html = html.replace("{{education}}", "<br>".join(parsed_data["education"]))
        html = html.replace("{{experience}}", "<br>".join(parsed_data["experience"]))
        html = html.replace("{{projects}}", "<br>".join(parsed_data["projects"]))
        html = html.replace("{{contact}}", parsed_data["contact"])
        files["index.html"] = html
        with open(f"{folder}/styles.css", "r") as f:
            files["styles.css"] = f.read()
    else:  # React
        with open(f"{folder}/App.jsx", "r") as f:
            app = f.read()
        app = app.replace("{{name}}", parsed_data["name"])
        app = app.replace("{{summary}}", parsed_data["summary"])
        app = app.replace("{{skills}}", str(parsed_data["skills"]))
        app = app.replace("{{education}}", str(parsed_data["education"]))
        app = app.replace("{{experience}}", str(parsed_data["experience"]))
        app = app.replace("{{projects}}", str(parsed_data["projects"]))
        app = app.replace("{{contact}}", parsed_data["contact"])
        files["src/App.jsx"] = app
        with open(f"{folder}/index.js", "r") as f:
            files["src/index.js"] = f.read()
        with open(f"{folder}/styles.css", "r") as f:
            files["src/styles.css"] = f.read()
        with open(f"{folder}/package.json", "r") as f:
            files["package.json"] = f.read()
        with open(f"{folder}/vercel.json", "r") as f:
            files["vercel.json"] = f.read()

    return files

# Create GitHub repository and push files
def create_github_repo(repo_name, files, github_token):
    try:
        g = Github(github_token)
        user = g.get_user()
        repo = user.create_repo(repo_name, private=False, auto_init=False)
        
        for file_path, content in files.items():
            repo.create_file(file_path, f"Add {file_path}", content, branch="main")
        
        return repo.html_url
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating GitHub repo: {str(e)}")

# Deploy to Vercel
def deploy_to_vercel(repo_url, vercel_token):
    try:
        headers = {"Authorization": f"Bearer {vercel_token}"}
        payload = {
            "name": f"portfolio-{int(datetime.now().timestamp())}",
            "gitRepository": {"type": "github", "repo": repo_url.replace("https://github.com/", "")}
        }
        response = requests.post(
            "https://api.vercel.com/v10/projects",
            json=payload,
            headers=headers
        )
        if response.status_code == 200 or response.status_code == 201:
            return response.json().get("domain", "Deployment in progress")
        else:
            raise HTTPException(status_code=500, detail=f"Vercel deployment failed: {response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deploying to Vercel: {str(e)}")

@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    content = await file.read()
    parsed_data = parse_resume(content)
    return {"filename": file.filename, "parsed_data": parsed_data}

@app.post("/generate")
async def generate_portfolio(data: dict):
    template = data.get("template", "classic")
    frontend_type = data.get("frontend_type", "html")
    parsed_data = data.get("parsed_data", {})
    try:
        files = generate_portfolio_files(parsed_data, template, frontend_type)
        
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for file_name, content in files.items():
                zip_file.writestr(file_name, content)
        zip_buffer.seek(0)

        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename=portfolio_{template}_{frontend_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating portfolio: {str(e)}")

@app.post("/deploy")
async def deploy_portfolio(data: dict):
    template = data.get("template", "classic")
    frontend_type = data.get("frontend_type", "html")
    parsed_data = data.get("parsed_data", {})
    github_token = data.get("github_token")
    vercel_token = data.get("vercel_token") or VERCEL_TOKEN

    if not github_token or not vercel_token:
        raise HTTPException(status_code=400, detail="GitHub and Vercel tokens are required")

    try:
        files = generate_portfolio_files(parsed_data, template, frontend_type)
        repo_name = f"portfolio-{parsed_data.get('name', 'user').replace(' ', '-').lower()}-{int(datetime.now().timestamp())}"
        repo_url = create_github_repo(repo_name, files, github_token)
        vercel_domain = deploy_to_vercel(repo_url, vercel_token)
        return {"repo_url": repo_url, "vercel_domain": vercel_domain}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deploying portfolio: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Resume2Portfolio Backend"}