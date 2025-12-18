# tests/test_media.py
# StoicizmFrame v3.14 — Foundry Tests
# Кодировка: UTF-8 LF без BOM

def test_foundry_request():
    from video_assembler import assemble_video
    result = assemble_video(["SCENE_001"], "VOICEOVER_001", "output/test.mp4")
    assert "scenes" in result
    assert "audio" in result
    assert "output" in result
    assert "transitions" in result
    assert "effects" in result