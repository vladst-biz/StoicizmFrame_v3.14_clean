"""
Builder — собирает структуру ролика из разобранных блоков.
"""

def build_structure(blocks: list) -> list:
    structure = []
    for i, block in enumerate(blocks):
        structure.append({
            "id": i + 1,
            "text": block,
            "visual_hint": f"visual_{i+1}",
            "voice_hint": f"voice_{i+1}"
        })
    return structure