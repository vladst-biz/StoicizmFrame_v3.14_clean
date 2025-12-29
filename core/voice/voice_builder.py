"""
Voice Builder — формирует сценарий озвучки на основе структуры ENGINE.
"""

def build_voice_script(structure: list) -> list:
    script = []
    for block in structure:
        script.append({
            "id": block["id"],
            "text": block["text"] if "text" in block else block.get("block", ""),
            "emotion": "neutral",
            "voice_profile": "default"
        })
    return script