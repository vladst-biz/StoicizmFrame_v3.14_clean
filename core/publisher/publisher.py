"""
PUBLISHER — сборка итогового продукта фабрики.
"""

def publish(timeline, visual, voice) -> dict:
    return {
        "timeline": timeline,
        "visual": visual,
        "voice": voice,
        "meta": {
            "export": "ready",
            "version": "v3.23"
        }
    }
