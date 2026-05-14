import re
import statistics
from collections import Counter

ROLE_KEYWORDS = {
    'software engineer': ['python', 'java', 'data structures', 'algorithms', 'api', 'git'],
    'data scientist': ['python', 'machine learning', 'statistics', 'pandas', 'numpy', 'model'],
    'ai engineer': ['ai', 'deep learning', 'neural network', 'tensorflow', 'pytorch', 'nlp'],
    'cloud engineer': ['aws', 'azure', 'cloud', 'docker', 'kubernetes', 'devops'],
    'cybersecurity analyst': ['security', 'network', 'vulnerability', 'encryption', 'compliance'],
    'product manager': ['roadmap', 'stakeholder', 'agile', 'product', 'metrics', 'vision'],
}


def extract_resume_text(path):
    text = ''
    if path.lower().endswith('.pdf'):
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(path)
            text = '\n'.join(page.extract_text() or '' for page in reader.pages)
        except Exception:
            text = ''
    elif path.lower().endswith('.docx'):
        try:
            from docx import Document
            doc = Document(path)
            text = '\n'.join(paragraph.text for paragraph in doc.paragraphs)
        except Exception:
            text = ''
    return text


def normalize_text(text):
    return re.sub(r'[^a-z0-9 ]+', ' ', text.lower())


def count_keywords(text, keywords):
    normalized = normalize_text(text)
    return sum(1 for keyword in keywords if keyword in normalized)


def score_range(value, maximum):
    return min(100, round((100 * value) / maximum))


def build_recommendations(profile, coverage_scores):
    recommendations = []
    if profile['cgpa']:
        try:
            cgpa = float(profile['cgpa'])
            if cgpa < 7.0:
                recommendations.append('Polish academic projects and highlight strong coursework to offset CGPA concerns.')
        except ValueError:
            pass
    if len(profile['skills']) < 4:
        recommendations.append('Add more technical skills relevant to your target role and industry.')
    if not profile['resume_text']:
        recommendations.append('Upload your resume or paste its text to get a detailed resume audit.')
    if coverage_scores['ats'] < 65:
        recommendations.append('Include role-specific keywords in your resume and headline for better ATS compatibility.')
    if coverage_scores['communication'] < 70:
        recommendations.append('Practice concise, structured interview answers and reduce filler phrases.')
    if coverage_scores['linkedin'] < 70:
        recommendations.append('Complete your LinkedIn headline, summary, and experience sections with role keywords.')
    if coverage_scores['portfolio'] < 60:
        recommendations.append('Add project case studies and clear portfolio navigation for recruiters.')
    if not profile['certifications'] or len([c for c in profile['certifications'] if c.strip()] ) == 0:
        recommendations.append('Add at least one role-aligned certification to strengthen your profile.')
    if not recommendations:
        recommendations.append('You have strong fundamentals — focus on execution and interview practice to reach expert readiness.')
    return recommendations


def analyze_profile(profile):
    role = profile['role'].lower()
    keywords = ROLE_KEYWORDS.get(role, ROLE_KEYWORDS['software engineer'])

    resume_text = profile.get('resume_text', '') or ''
    skills_text = ' '.join(profile.get('skills', []))
    linkedin_text = ' '.join([profile.get('linkedin', ''), profile.get('portfolio', ''), profile.get('github', '')])
    answer_text = profile.get('answer', '')

    resume_quality = score_range(count_keywords(resume_text, keywords) + len(re.findall(r'education|experience|projects|certification|achievement', resume_text.lower())), 20)
    ats_score = score_range(count_keywords(resume_text, keywords) * 2 + len(re.findall(r'\bpython\b|\bjava\b|\bsql\b|\baws\b|\bmachine learning\b', resume_text.lower())), 30)
    technical_score = score_range(len([s for s in profile.get('skills', []) if s.strip()]) * 6 + len([l for l in profile.get('languages', []) if l.strip()]) * 3, 60)
    communication_score = score_range(len(re.findall(r'\w+', answer_text)) / 2 + 20, 100)
    confidence_score = score_range(min(len(answer_text) / 15, 8) * 10, 100)
    portfolio_score = score_range(len(profile.get('projects', [])) * 8 + len(profile.get('portfolio', '')) * 10, 100)
    github_score = score_range(len(profile.get('github', '')) * 10 + len(profile.get('projects', [])) * 5, 100)
    linkedin_score = score_range(len(profile.get('linkedin', '')) * 10 + len(profile['company']) * 2, 100)
    certification_score = score_range(len([c for c in profile.get('certifications', []) if c.strip()]) * 15, 100)
    alignment_score = score_range((count_keywords(profile.get('goals', ''), keywords) + count_keywords(profile.get('industry', ''), keywords)) * 10, 100)

    overall = round(
        0.30 * technical_score
        + 0.20 * ((resume_quality + ats_score) / 2)
        + 0.15 * ((communication_score + confidence_score) / 2)
        + 0.15 * ((portfolio_score + github_score + linkedin_score) / 3)
        + 0.10 * certification_score
        + 0.10 * alignment_score
    )

    dream_company_readiness = score_range(overall + len(profile['company']) * 2, 120)
    success_probability = min(99, round(overall * 0.96 + 4))
    days_to_ready = max(7, 90 - overall)

    coverage_scores = {
        'resume': resume_quality,
        'ats': ats_score,
        'technical': technical_score,
        'communication': communication_score,
        'confidence': confidence_score,
        'portfolio': portfolio_score,
        'github': github_score,
        'linkedin': linkedin_score,
        'certifications': certification_score,
        'alignment': alignment_score,
    }

    report = {
        'overall_score': overall,
        'category_scores': coverage_scores,
        'dream_company_readiness': min(100, dream_company_readiness),
        'success_probability': success_probability,
        'days_to_ready': days_to_ready,
        'recommendations': build_recommendations(profile, coverage_scores),
        'skill_badges': build_skill_badges(coverage_scores),
        'summary': build_recruiter_summary(overall, coverage_scores),
    }
    return report


def build_skill_badges(scores):
    badges = []
    if scores['resume'] >= 70 and scores['ats'] >= 65:
        badges.append('Resume Master')
    if scores['technical'] >= 75:
        badges.append('Coding Champion')
    if scores['communication'] >= 70 and scores['confidence'] >= 70:
        badges.append('Communication Pro')
    if scores['portfolio'] >= 65 and scores['github'] >= 65:
        badges.append('Portfolio Expert')
    if not badges:
        badges.append('Rising Talent')
    return badges


def build_recruiter_summary(overall, scores):
    if overall >= 90:
        level = 'Interview Ready Expert'
    elif overall >= 75:
        level = 'Strong Candidate'
    elif overall >= 50:
        level = 'Needs Improvement'
    else:
        level = 'Beginner'

    strengths = [name for name, score in scores.items() if score >= 75]
    weaknesses = [name for name, score in scores.items() if score < 60]

    return {
        'level': level,
        'strengths': strengths or ['Core technical foundation'],
        'weaknesses': weaknesses or ['Refine your narrative and polish your resume'],
        'recommendation': 'Focus on high-impact activities like interview practice, keyword optimization, and project storytelling.'
    }
