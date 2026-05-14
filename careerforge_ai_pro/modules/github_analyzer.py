import random

def evaluate(url: str) -> int:
    """Return a mock GitHub score between 60 and 100.
    Real implementation would analyse repos, README quality, commit frequency, etc.
    """
    if not url:
        return 0
    return random.randint(60, 100)
