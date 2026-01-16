from typing import Any, Dict
from scenes.scene_registry import get_scene_class
from engine.engine_logger import get_engine_logger

logger = get_engine_logger()

def route_request(payload: Dict[str, Any]) -> Dict[str, Any]:
    scene_id = payload.get("scene_id") or "SCENE_002"
    scene_cls = get_scene_class(scene_id)

    logger.info(f"Routing request to scene_id={scene_id}")

    if scene_cls is None:
        logger.error(f"Unknown scene_id={scene_id}")
        return {
            "scene_id": scene_id,
            "status": "ERROR",
            "message": f"Unknown scene_id={scene_id}",
        }

    scene = scene_cls()
    try:
        result = scene.run(payload)
        logger.info(f"Scene {scene_id} executed successfully")
        return result
    except Exception as exc:
        logger.exception(f"Error in scene {scene_id}: {exc}")
        return {
            "scene_id": scene_id,
            "status": "ERROR",
            "message": str(exc),
        }
