import sys
import os

# Добавляем корень проекта в sys.path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

"""
run_pipeline — первый рабочий конвейер фабрики StoicizmFrame.
Поток:
LLM → REFRAMER → ENGINE → VISUAL CONTROL → VOICE CONTROL → PUBLISHER → ANALYTICS
"""

import json

# --- Импорты модулей фабрики ---
from adapters.llm_client import generate_scene
from core.reframer.reframer import reframe
from core.engine.engine import build_timeline
from core.visual.control.presets import PRESETS as VISUAL_PRESETS
from core.voice.control.presets import PRESETS as VOICE_PRESETS
from core.publisher.publisher import publish
from core.analytics.analytics import analyze


def run(topic: str):
    print("STEP 1: LLM → RAW SCENE")
    raw = generate_scene(topic)
    print("RAW:", raw)

    print("\nSTEP 2: REFRAMER")
    reframed = reframe(raw["raw_scene"])
    print("REFRAMED:", reframed)

    print("\nSTEP 3: ENGINE → TIMELINE")
    timeline = build_timeline(reframed)
    print("TIMELINE:", timeline)

    print("\nSTEP 4: VISUAL & VOICE PRESETS")
    visual = VISUAL_PRESETS.get("stoic_calm", {})
    voice = VOICE_PRESETS.get("stoic_calm", {})
    print("VISUAL:", visual)
    print("VOICE:", voice)

    print("\nSTEP 5: PUBLISHER → PRODUCT")
    product = publish(timeline, visual, voice)
    print("PRODUCT:", product)

    print("\nSTEP 6: ANALYTICS")
    analytics = analyze(product)
    print("ANALYTICS:", analytics)

    print("\nSTEP 7: SAVE output.json")
    output = {
        "topic": topic,
        "raw": raw,
        "reframed": reframed,
        "timeline": timeline,
        "visual": visual,
        "voice": voice,
        "product": product,
        "analytics": analytics
    }

    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=4)

    print("\nPipeline complete. Output saved to output.json")


if __name__ == "__main__":
    run("Тестовая тема")
