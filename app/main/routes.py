from flask import render_template, flash, redirect, url_for, request
from . import main
from .forms import ResumeForm
from models.resume_parser import parse_resume, extract_text_from_docx
from models.job_description_parser import parse_job_description
from models.resume_scorer import score_resume, generate_feedback
from werkzeug.utils import secure_filename
import os
from PyPDF2 import PdfReader

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

@main.route('/', methods=['GET', 'POST'])
def index():
    form = ResumeForm()
    results = None
    if form.validate_on_submit():
        resume_file = form.resume.data
        job_title = form.job_title.data
        job_description = form.job_description.data
        job_responsibilities = form.job_responsibilities.data
        job_experience = form.job_experience.data
        job_skills = form.job_skills.data
        job_education = form.job_education.data

        if resume_file and allowed_file(resume_file.filename):
            filename = secure_filename(resume_file.filename)
            file_extension = filename.rsplit('.', 1)[1].lower()

            if file_extension in {'doc', 'docx'}:
                resume_text = extract_text_from_docx(resume_file)
            elif file_extension == 'pdf':
                resume_text = extract_text_from_pdf(resume_file)
            else:
                resume_text = resume_file.read().decode('utf-8', errors='ignore')

            resume_data = parse_resume(resume_text)
            job_description_data = parse_job_description(
                job_description, job_responsibilities, job_experience, job_skills, job_education
            )
            scores = score_resume(resume_data, job_description_data)
            feedback = generate_feedback(resume_data, job_description_data)

            results = {
                'total_score': scores['total_score'],
                'structure_score': scores['structure_score'],
                'skills_score': scores['skills_score'],
                'experience_score': scores['experience_score'],
                'education_score': scores['education_score'],
                'feedback': feedback
            }
            flash('Resume analysis completed successfully!', 'success')
            # Return to the same page with results
            return render_template('index.html', form=form, results=results)

    return render_template('index.html', form=form, results=results)