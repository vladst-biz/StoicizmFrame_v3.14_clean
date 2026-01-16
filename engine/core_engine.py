from typing import Any, Dict
from engine.engine_config import EngineConfig
from engine.engine_router import route_request
from engine.engine_logger import get_engine_logger

logger = get_engine_logger()

class CoreEngine:
    def __init__(self, config: EngineConfig | None = None) -> None:
        self.config = config or EngineConfig()

    def handle(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"ENGINE received payload: keys={list(payload.keys())}")

        if "scene_id" not in payload:
            payload["scene_id"] = self.config.default_scene_id

        result = route_request(payload)
        logger.info(f"ENGINE result status={result.get('status')}")
        return result
