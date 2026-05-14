import random

def analyze(resume_file, target_role=None):
    """Mock resume analysis returning a random ATS compatibility score (60-95)."""
    return random.randint(60, 95)
