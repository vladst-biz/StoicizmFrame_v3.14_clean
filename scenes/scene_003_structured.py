from typing import Dict, Any
from scenes.scene_base import BaseScene


class StructuredOutputScene(BaseScene):
    SCENE_ID = "SCENE_003"

    """
    SCENE_003 — структурированный вывод.
    """

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        # ENGINE вызывает run(), поэтому логика здесь
        return self.execute(payload)

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        text = payload.get("text", "")

        keywords = [w for w in text.split() if len(w) > 3]
        intent = "statement" if text.endswith(".") else "request"

        structure = {
            "length": len(text),
            "words": len(text.split()),
            "keywords": keywords[:5],
        }

        return {
            "scene_id": self.SCENE_ID,
            "mode": payload.get("mode", "text"),
            "input_preview": text[:50],
            "intent": intent,
            "structure": structure,
            "status": "OK",
        }
