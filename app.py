import os
import re
import smtplib
from email.message import EmailMessage
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='.')

SMTP_SERVER = os.getenv('SMTP_SERVER', 'localhost')
SMTP_PORT = int(os.getenv('SMTP_PORT', '25'))
SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
SMTP_USE_TLS = os.getenv('SMTP_USE_TLS', 'false').lower() in ('true', '1', 'yes')
EMAIL_FROM = os.getenv('EMAIL_FROM', 'no-reply@example.com')

def polish_text(text):
    if not text:
        return "", []
    
    corrections_made = []
    polished = text
    
    # Capitalize professional brands and fix common typos
    corrections_map = {
        r'\bpyton\b': ('Python', 'Fixed spelling of "pyton"'),
        r'\bpython\b': ('Python', 'Capitalized "Python"'),
        r'\bjavascript\b': ('JavaScript', 'Capitalized "JavaScript"'),
        r'\btypescript\b': ('TypeScript', 'Capitalized "TypeScript"'),
        r'\breact\b': ('React', 'Capitalized "React"'),
        r'\breactjs\b': ('React', 'Standardized "reactjs" to "React"'),
        r'\bnode\b': ('Node.js', 'Standardized "node" to "Node.js"'),
        r'\bnodejs\b': ('Node.js', 'Standardized "nodejs" to "Node.js"'),
        r'\baws\b': ('AWS', 'Capitalized "AWS"'),
        r'\bgcp\b': ('GCP', 'Capitalized "GCP"'),
        r'\bdocker\b': ('Docker', 'Capitalized "Docker"'),
        r'\bkubernetes\b': ('Kubernetes', 'Capitalized "Kubernetes"'),
        r'\bk8s\b': ('Kubernetes', 'Expanded "k8s" to "Kubernetes"'),
        r'\bpostgresql\b': ('PostgreSQL', 'Capitalized "PostgreSQL"'),
        r'\bmongodb\b': ('MongoDB', 'Capitalized "MongoDB"'),
        r'\bhtml\b': ('HTML', 'Capitalized "HTML"'),
        r'\bcss\b': ('CSS', 'Capitalized "CSS"'),
        r'\bapi\b': ('API', 'Capitalized "API"'),
        r'\bapis\b': ('APIs', 'Capitalized "APIs"'),
        r'\brestapi\b': ('REST API', 'Standardized "restapi" to "REST API"'),
        r'\brest api\b': ('REST API', 'Capitalized "REST API"'),
        r'\bgraphql\b': ('GraphQL', 'Capitalized "GraphQL"'),
        r'\bci/cd\b': ('CI/CD', 'Capitalized "CI/CD"'),
        r'\bcicd\b': ('CI/CD', 'Standardized "cicd" to "CI/CD"'),
        r'\bgithub\b': ('GitHub', 'Capitalized "GitHub"'),
        r'\bdevelopement\b': ('development', 'Fixed spelling of "developement"'),
        r'\brecieve\b': ('receive', 'Fixed spelling of "recieve"'),
        r'\bseperate\b': ('separate', 'Fixed spelling of "seperate"'),
        r'\bdefinately\b': ('definitely', 'Fixed spelling of "definately"'),
        r'\buntill\b': ('until', 'Fixed spelling of "untill"'),
        r'\buniversty\b': ('University', 'Fixed spelling of "universty"'),
        r'\bcolledge\b': ('College', 'Fixed spelling of "colledge"'),
        r'\bcertifcate\b': ('Certificate', 'Fixed spelling of "certifcate"'),
        r'\bexpereince\b': ('Experience', 'Fixed spelling of "expereince"'),
        r'\bengeneer\b': ('Engineer', 'Fixed spelling of "engeneer"'),
        r'\bmanagment\b': ('Management', 'Fixed spelling of "managment"'),
        r'\bsoftwer\b': ('software', 'Fixed spelling of "softwer"'),
        r'\bsoftwere\b': ('software', 'Fixed spelling of "softwere"'),
    }
    
    for pattern, (replacement, desc) in corrections_map.items():
        matches = re.findall(pattern, polished, flags=re.IGNORECASE)
        if matches:
            needs_change = False
            for m in matches:
                if m != replacement:
                    needs_change = True
                    break
            if needs_change:
                polished = re.sub(pattern, replacement, polished, flags=re.IGNORECASE)
                corrections_made.append(desc)

    # Capitalize sentences
    def capitalize_sentence_match(match):
        return match.group(1) + match.group(2).upper()

    sentence_pattern = r'(^|[\.\!\?\n]\s*)([a-z])'
    new_polished, count = re.subn(sentence_pattern, capitalize_sentence_match, polished)
    if count > 0:
        polished = new_polished
        corrections_made.append(f"Capitalized {count} sentence starter(s)")
        
    return polished, corrections_made

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'GET':
        return redirect(url_for('home'))
    
    name = request.form.get('name', '')
    title = request.form.get('title', '')
    profile_photo_url = request.form.get('profile_photo_url', '')
    location = request.form.get('location', '')
    email = request.form.get('email', '')
    client_email = request.form.get('client_email', '')
    professional_profiles = request.form.get('professional_profiles', '')
    about_me = request.form.get('about_me', '')
    education = request.form.get('education', '')
    projects = request.form.get('projects', '')
    qualifications = request.form.get('qualifications', '')
    certificates = request.form.get('certificates', '')
    languages = request.form.get('languages', '')
    skills = request.form.get('skills', '')

    # Apply AI Polish
    ai_corrections = []
    
    if name:
        name_title = name.title()
        if name != name_title:
            name = name_title
            ai_corrections.append("Standardized Full Name capitalization")
            
    if title:
        title_title = title.title()
        if title != title_title:
            title = title_title
            ai_corrections.append("Standardized Professional Title capitalization")

    about_me, ab_corr = polish_text(about_me)
    ai_corrections.extend([f"About Me: {c}" for c in ab_corr])

    education, ed_corr = polish_text(education)
    ai_corrections.extend([f"Education: {c}" for c in ed_corr])

    projects, pr_corr = polish_text(projects)
    ai_corrections.extend([f"Projects: {c}" for c in pr_corr])

    qualifications, ql_corr = polish_text(qualifications)
    ai_corrections.extend([f"Qualifications: {c}" for c in ql_corr])

    certificates, ct_corr = polish_text(certificates)
    ai_corrections.extend([f"Certifications: {c}" for c in ct_corr])

    languages, lg_corr = polish_text(languages)
    ai_corrections.extend([f"Languages: {c}" for c in lg_corr])

    skills, sk_corr = polish_text(skills)
    ai_corrections.extend([f"Skills: {c}" for c in sk_corr])

    return render_template(
        'resume.html',
        name=name,
        title=title,
        profile_photo_url=profile_photo_url,
        location=location,
        email=email,
        client_email=client_email,
        professional_profiles=professional_profiles,
        about_me=about_me,
        education=education,
        projects=projects,
        qualifications=qualifications,
        certificates=certificates,
        languages=languages,
        skills=skills,
        ai_corrections=ai_corrections
    )

@app.route('/send_resume', methods=['GET', 'POST'])
def send_resume():
    if request.method == 'GET':
        return redirect(url_for('home'))
    
    name = request.form.get('name', '')
    title = request.form.get('title', '')
    profile_photo_url = request.form.get('profile_photo_url', '')
    location = request.form.get('location', '')
    email = request.form.get('email', '')
    client_email = request.form.get('client_email', '')
    professional_profiles = request.form.get('professional_profiles', '')
    about_me = request.form.get('about_me', '')
    education = request.form.get('education', '')
    projects = request.form.get('projects', '')
    qualifications = request.form.get('qualifications', '')
    certificates = request.form.get('certificates', '')
    languages = request.form.get('languages', '')
    skills = request.form.get('skills', '')
    
    ai_corrections = []
    
    if name:
        name_title = name.title()
        if name != name_title:
            name = name_title
            ai_corrections.append("Standardized Full Name capitalization")
            
    if title:
        title_title = title.title()
        if title != title_title:
            title = title_title
            ai_corrections.append("Standardized Professional Title capitalization")

    about_me, ab_corr = polish_text(about_me)
    ai_corrections.extend([f"About Me: {c}" for c in ab_corr])

    education, ed_corr = polish_text(education)
    ai_corrections.extend([f"Education: {c}" for c in ed_corr])

    projects, pr_corr = polish_text(projects)
    ai_corrections.extend([f"Projects: {c}" for c in pr_corr])

    qualifications, ql_corr = polish_text(qualifications)
    ai_corrections.extend([f"Qualifications: {c}" for c in ql_corr])

    certificates, ct_corr = polish_text(certificates)
    ai_corrections.extend([f"Certifications: {c}" for c in ct_corr])

    languages, lg_corr = polish_text(languages)
    ai_corrections.extend([f"Languages: {c}" for c in lg_corr])

    skills, sk_corr = polish_text(skills)
    ai_corrections.extend([f"Skills: {c}" for c in sk_corr])

    # Render email template
    email_html = render_template(
        'resume_email.html',
        name=name,
        title=title,
        location=location,
        email=email,
        professional_profiles=professional_profiles,
        about_me=about_me,
        education=education,
        projects=projects,
        qualifications=qualifications,
        certificates=certificates,
        languages=languages,
        skills=skills
    )

    message = ""
    success = False
    try:
        msg = EmailMessage()
        msg['Subject'] = f"Resume of {name}"
        msg['From'] = EMAIL_FROM
        msg['To'] = client_email
        msg.set_content(f"Hello,\n\nPlease find the resume of {name} below.\n\nBest regards.")
        msg.add_alternative(email_html, subtype='html')

        # SMTP Sending
        if SMTP_USE_TLS:
            smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=5)
            smtp.starttls()
        else:
            smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=5)
        
        if SMTP_USERNAME and SMTP_PASSWORD:
            smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
            
        smtp.send_message(msg)
        smtp.quit()
        message = f"Successfully emailed resume to {client_email}!"
        success = True
    except Exception as e:
        print("\n" + "="*80)
        print(f"SMTP SEND FAILED: {e}")
        print(f"Local fallback: Printed email for {name} targeting {client_email}")
        print("-" * 80)
        print(email_html)
        print("="*80 + "\n")
        message = f"Email sending simulated. (SMTP offline, details printed to terminal: {e})"
        success = False

    return render_template(
        'resume.html',
        name=name,
        title=title,
        profile_photo_url=profile_photo_url,
        location=location,
        email=email,
        client_email=client_email,
        professional_profiles=professional_profiles,
        about_me=about_me,
        education=education,
        projects=projects,
        qualifications=qualifications,
        certificates=certificates,
        languages=languages,
        skills=skills,
        message=message,
        message_success=success,
        ai_corrections=ai_corrections
    )

if __name__ == '__main__':
    app.run(debug=True)