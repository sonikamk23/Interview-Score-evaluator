import random

def evaluate(url: str) -> int:
    """Return a mock LinkedIn score between 60 and 100.
    Real implementation would fetch the profile and analyse headline, summary, endorsements, etc.
    """
    if not url:
        return 0
    return random.randint(60, 100)
