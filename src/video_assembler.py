# src/video_assembler.py
# Кодировка: UTF-8 LF без BOM

def assemble_video(scene_files, audio_file, output_file):
    """
    Вместо локальной сборки через MoviePy формируем заявку для Foundry.
    """
    request = {
        "scenes": scene_files,
        "audio": audio_file,
        "output": output_file,
        "transitions": "dynamic",
        "effects": ["fade", "crossfade"]
    }
    # Логируем заявку в docs/SCENE_PIPELINE.md
    with open("docs/SCENE_PIPELINE.md", "w", encoding="utf-8") as f:
        f.write("# Foundry Video Assembly Request\n\n")
        f.write(str(request))
    print("Заявка на Foundry сформирована:", request)
    return request