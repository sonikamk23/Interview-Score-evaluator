def evaluate(answer: str) -> int:
    """Simple placeholder that returns a confidence score based on answer length.
    In a real implementation this would analyse voice tone, speaking speed, etc.
    """
    if not answer:
        return 0
    length = len(answer.split())
    # Scale length to 0-100 (capped)
    score = min(100, max(0, int((length / 100) * 100)))
    return score
