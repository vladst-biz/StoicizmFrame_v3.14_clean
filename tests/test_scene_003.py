from engine.core_engine import CoreEngine

engine = CoreEngine()

if __name__ == "__main__":
    payload = {
        "scene_id": "SCENE_003",
        "text": "Это тестовая строка для структурированного вывода.",
        "mode": "text"
    }
    print(engine.handle(payload))
