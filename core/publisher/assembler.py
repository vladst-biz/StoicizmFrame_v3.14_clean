"""
Assembler — объединяет визуал, голос и таймлайн в единый объект.
Работает с уникализированным текстом (REFRAMER → ENGINE).
"""

def assemble_product(structure: dict) -> dict:
    return {
        "timeline": structure.get("timeline", []),
        "visual": structure.get("visual", []),
        "voice": structure.get("voice", []),
        "meta": {
            "version": "v3.21",
            "status": "assembled",
            "source": "REFRAMER → ENGINE → VISUAL → VOICE"
        }
    }