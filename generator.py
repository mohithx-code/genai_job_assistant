import json
from config import get_model

MODEL = get_model()

def call_generation(prompt, temperature=0.2, max_output_tokens=400):
    try:
        response = MODEL.generate_content(
            prompt,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_output_tokens
            }
        )
        return response.text
    except Exception as e:
        return f"[ERROR] {str(e)}"

# def generate_tailored_bullets(jd_skills, resume_text, count=4):
#     prompt = f"""
# You are an expert resume writer.

# JD Skills: {jd_skills}
# Resume:
# {resume_text[:1500]}

# Generate {count} ATS-friendly achievement bullets.
# Return ONLY JSON:
# {{"bullets": ["..."]}}
# """

#     output = call_generation(prompt)
#     try:
#         return json.loads(output).get("bullets", [])
#     except:
#         return ["Bullet generation failed"]

def generate_tailored_bullets(jd_skills, resume_text, count=4):
    skill_str = ", ".join(jd_skills)

    prompt = f"""
You are an expert ATS resume writer.

Generate EXACTLY {count} professional resume bullet points that match these skills:
{skill_str}

Use ONLY information from this resume:
{resume_text[:1500]}

Return output in ONLY this exact JSON format:
{{
  "bullets": ["bullet 1", "bullet 2", "bullet 3", "bullet 4"]
}}
JSON ONLY. No explanation, no additional text.
"""

    output = call_generation(prompt)

    # Try extracting JSON inside the response (even if model adds text)
    import re, json

    try:
        json_str = re.search(r"\{[\s\S]*\}", output).group(0)
        data = json.loads(json_str)
        return data.get("bullets", [])
    except Exception as e:
        print("Bullet JSON parsing error:", e)
        print("Model raw output:", output)
        return ["Bullet generation failed."]


def generate_cover_letter(name, job_title, company, resume_text, bullets, jd_text):
    bullets_text = "\n".join([f"- {b}" for b in bullets])

    prompt = f"""
Write a professional 350-word cover letter.

Name: {name}
Role: {job_title}
Company: {company}

Achievements:
{bullets_text}

Job Description:
{jd_text[:1200]}

Tone: confident, specific, structured.
End with a strong interview request.
    """

    return call_generation(prompt, temperature=0.3, max_output_tokens=600)
