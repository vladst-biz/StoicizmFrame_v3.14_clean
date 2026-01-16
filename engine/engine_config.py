from dataclasses import dataclass

@dataclass
class EngineConfig:
    default_scene_id: str = "SCENE_002"
    debug: bool = False
