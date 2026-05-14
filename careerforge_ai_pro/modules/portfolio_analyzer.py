import random

def evaluate(url: str) -> int:
    """Return a mock portfolio score between 60 and 100.
    In production this would scrape the site and analyse project descriptions.
    """
    if not url:
        return 0
    return random.randint(60, 100)
