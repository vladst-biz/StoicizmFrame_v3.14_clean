"""
ENGINE — модуль структурирования текста в таймлайн.
"""

def build_timeline(text: str) -> list:
    if not text:
        return []

    sentences = [s.strip() for s in text.split('.') if s.strip()]

    timeline = []
    for i, sentence in enumerate(sentences, start=1):
        timeline.append({
            "id": i,
            "text": sentence,
            "duration": 5
        })

    return timeline
