"""
Storyboard — строит визуальный план ролика на основе структуры ENGINE.
"""

def build_storyboard(structure: list) -> list:
    storyboard = []
    for block in structure:
        storyboard.append({
            "id": block["id"],
            "text": block["text"] if "text" in block else block.get("block", ""),
            "background": "default_bg",
            "overlay": "default_overlay",
            "style": "default_style"
        })
    return storyboard