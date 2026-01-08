# src/content_pipeline.py
# StoicizmFrame v3.14 — Content Pipeline
# Кодировка: UTF-8 LF без BOM

import os
from contentgenerationmodule import load_donors, build_scene, save_scene
from video_assembler import assemble_video

def run_pipeline():
    donors = load_donors()
    scene = build_scene(donors)
    save_scene(scene, "docs/SCENE_PIPELINE.md")

    # Заявка для Foundry: абстрактные идентификаторы сцен и аудио
    scene_files = ["SCENE_001", "SCENE_002"]
    audio_file = "VOICEOVER_001"

    if not os.path.exists("output"):
        os.makedirs("output")

    result = assemble_video(scene_files, audio_file, "output/final_scene.mp4")
    print(f"Заявка на Foundry отправлена: {result}")

if __name__ == "__main__":
    run_pipeline()
