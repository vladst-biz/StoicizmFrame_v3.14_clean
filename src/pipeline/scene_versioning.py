
from pathlib import Path
from datetime import datetime

class SceneVersionManager:
    """Управляет версиями сцен StoicizmFrame."""

    def __init__(self, base_dir="scenes"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def get_next_scene_id(self) -> str:
        scenes = [p for p in self.base_dir.iterdir() if p.is_dir()]
        if not scenes:
            return "SCENE_001"

        ids = sorted([int(p.name.split("_")[1]) for p in scenes])
        return f"SCENE_{ids[-1] + 1:03d}"

    def get_next_version(self, scene_dir: Path) -> str:
        versions = [p for p in scene_dir.iterdir() if p.is_dir()]
        if not versions:
            return "v1"

        nums = sorted([int(p.name[1:]) for p in versions])
        return f"v{nums[-1] + 1}"

    def create_scene_version(self):
        scene_id = self.get_next_scene_id()
        scene_dir = self.base_dir / scene_id
        scene_dir.mkdir(exist_ok=True)

        version = self.get_next_version(scene_dir)
        version_dir = scene_dir / version
        version_dir.mkdir(exist_ok=True)

        return scene_id, version, version_dir

"""
ROLLBACK: scene_versioning.py.rollback_before_creation
"""

