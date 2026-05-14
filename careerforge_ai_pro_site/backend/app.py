import os
from flask import Flask, request, jsonify, send_file, send_from_directory
from werkzeug.utils import secure_filename
from modules.analysis import analyze_profile, extract_resume_text
from modules.reporting import generate_pdf_report, generate_qr_code_data_uri

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.normpath(os.path.join(BASE_DIR, '..', 'frontend'))
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')

os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR
app.config['MAX_CONTENT_LENGTH'] = 12 * 1024 * 1024
ALLOWED_EXTENSIONS = {'pdf', 'docx'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(os.path.join(FRONTEND_DIR, path)):
        return send_from_directory(FRONTEND_DIR, path)
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    data = request.form.to_dict()
    resume_text = ''
    file = request.files.get('resume')

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        resume_text = extract_resume_text(file_path)
    else:
        resume_text = data.get('resume_text', '')

    profile_data = {
        'name': data.get('name', '').strip(),
        'email': data.get('email', '').strip(),
        'college': data.get('college', '').strip(),
        'degree': data.get('degree', '').strip(),
        'year': data.get('year', '').strip(),
        'cgpa': data.get('cgpa', '').strip(),
        'role': data.get('role', '').strip(),
        'company': data.get('company', '').strip(),
        'github': data.get('github', '').strip(),
        'linkedin': data.get('linkedin', '').strip(),
        'portfolio': data.get('portfolio', '').strip(),
        'skills': data.get('skills', '').split(','),
        'languages': data.get('languages', '').split(','),
        'frameworks': data.get('frameworks', '').split(','),
        'certifications': data.get('certifications', '').split(','),
        'internships': data.get('internships', '').split(','),
        'projects': data.get('projects', '').split(','),
        'achievements': data.get('achievements', '').split(','),
        'goals': data.get('goals', '').strip(),
        'industry': data.get('industry', '').strip(),
        'answer': data.get('answer', '').strip(),
        'resume_text': resume_text,
    }

    report = analyze_profile(profile_data)
    return jsonify(report)


@app.route('/api/report', methods=['POST'])
def api_report():
    data = request.form.to_dict()
    if not data:
        return jsonify({'error': 'No data received'}), 400

    resume_text = ''
    file = request.files.get('resume')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        resume_text = extract_resume_text(file_path)
    else:
        resume_text = data.get('resume_text', '')

    profile_data = {
        'name': data.get('name', '').strip(),
        'email': data.get('email', '').strip(),
        'college': data.get('college', '').strip(),
        'degree': data.get('degree', '').strip(),
        'year': data.get('year', '').strip(),
        'cgpa': data.get('cgpa', '').strip(),
        'role': data.get('role', '').strip(),
        'company': data.get('company', '').strip(),
        'github': data.get('github', '').strip(),
        'linkedin': data.get('linkedin', '').strip(),
        'portfolio': data.get('portfolio', '').strip(),
        'skills': data.get('skills', '').split(','),
        'languages': data.get('languages', '').split(','),
        'frameworks': data.get('frameworks', '').split(','),
        'certifications': data.get('certifications', '').split(','),
        'internships': data.get('internships', '').split(','),
        'projects': data.get('projects', '').split(','),
        'achievements': data.get('achievements', '').split(','),
        'goals': data.get('goals', '').strip(),
        'industry': data.get('industry', '').strip(),
        'answer': data.get('answer', '').strip(),
        'resume_text': resume_text,
    }
    report = analyze_profile(profile_data)
    pdf_buffer = generate_pdf_report(profile_data, report)
    return send_file(pdf_buffer, mimetype='application/pdf', as_attachment=True, download_name='CareerForge_AI_Pro_Report.pdf')


@app.route('/api/qr', methods=['POST'])
def api_qr():
    data = request.form.to_dict()
    name = data.get('name', 'Candidate')
    company = data.get('company', 'Dream Company')
    role = data.get('role', 'Target Role')
    overall = data.get('overall_score', 'N/A')
    share_text = f"CareerForge AI Pro report for {name} - {role} readiness {overall}% towards {company}."
    qr_data_uri = generate_qr_code_data_uri(share_text)
    return jsonify({'qr': qr_data_uri})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8601))
    app.run(host='0.0.0.0', port=port, debug=True)
