# 🚀 GenAI Job Application Assistant  
AI-powered resume analysis & job-matching tool built using **Python**, **Streamlit**, and **Google Gemini**.

---

## 📌 Features
- Resume text extraction (PDF / TXT)
- TF-IDF–based skill extraction from JD
- Semantic + keyword match scoring
- Interactive Match Score Dashboard
- ATS-friendly bullet point generation
- Professional cover letter generation
- Dark-mode optimized UI

---

## 📁 Project Structure
GENAI-JOB-ASSISTANT/
│
├── main.py # Streamlit UI + app flow
├── scoring.py # Semantic similarity & keyword matching
├── resume_parser.py # PDF/text extraction & cleaning
├── jd_parser.py # Skill extraction & preprocessing
├── generator.py # Bullet point & cover letter generation
├── config.py # Gemini API configuration
├── requirements.txt # Dependency list
├── examples/ # Sample JD, resume & outputs
└── .env # API keys (ignored)



---

# ⚙️ Installation & Setup

## 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/genai-job-assistant.git
cd genai-job-assistant

## 2️⃣ Create a virtual environment
macOS / Linux

```bash

python3 -m venv venv
source venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt


Windows (PowerShell)

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt

Windows (Command Prompt)

```bash
python -m venv venv
venv\Scripts\activate

python -m pip install --upgrade pip
pip install -r requirements.txt

## 3️⃣ Add Gemini API Key (.env file)

Create a .env file in the project root:

GEMINI_API_KEY=your_api_key_here
MODEL_NAME=gemini-1.5-flash

##4️⃣ Run the Application
```bash
streamlit run main.py


After running, open:

http://localhost:8501