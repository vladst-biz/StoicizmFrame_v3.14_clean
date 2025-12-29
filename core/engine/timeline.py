"""
Timeline — создаёт таймкоды для ролика.
"""

def create_timeline(structure: list) -> list:
    timeline = []
    current_time = 0.0

    for block in structure:
        duration = max(2.0, len(block["text"]) / 20)
        timeline.append({
            "id": block["id"],
            "start": round(current_time, 2),
            "end": round(current_time + duration, 2)
        })
        current_time += duration

    return timeline