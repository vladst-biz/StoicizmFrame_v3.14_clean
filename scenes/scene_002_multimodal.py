from typing import Any, Dict
from .scene_base import BaseScene

class Scene002Multimodal(BaseScene):
    SCENE_ID = "SCENE_002"

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        text_input = payload.get("text")
        mode = payload.get("mode", "text")

        return {
            "scene_id": self.SCENE_ID,
            "mode": mode,
            "input_preview": str(text_input)[:200] if text_input else None,
            "status": "OK",
            "message": "SCENE_002 executed as stub.",
        }
