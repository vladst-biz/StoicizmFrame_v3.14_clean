# ============================================================
#  StoicizmFrame — Foundry Adapter v3.15
#  Guided Storyboard Assembly — управляемая видеогенерация
# ============================================================

import time
import json
from pathlib import Path
import requests


class FoundryAdapter:
    """
    Адаптер для Azure Foundry.
    Работает в режиме Guided Storyboard Assembly:
    - принимает таймлайн
    - принимает аудио
    - принимает визуальные подсказки
    - формирует Foundry JSON
    - запускает рендер
    - отслеживает статус
    """

    def __init__(self, endpoint: str, api_key: str):
        self.endpoint = endpoint.rstrip("/")
        self.api_key = api_key

    # ------------------------------------------------------------
    #  Формирование JSON для Foundry
    # ------------------------------------------------------------
    def build_storyboard(self, timeline, entry_audio, body_audio, legacy_audio):
        """
        timeline — объект от LayoutComposer
        entry_audio, body_audio, legacy_audio — пути к аудиофайлам
        """

        return {
            "mode": "guided_storyboard",
            "scenes": [
                {
                    "id": "ENTRY",
                    "audio": str(entry_audio),
                    "duration": timeline.entry_duration,
                    "visual_prompt": timeline.entry_visual_prompt,
                    "transition": timeline.entry_transition,
                },
                {
                    "id": "BODY",
                    "audio": str(body_audio),
                    "duration": timeline.body_duration,
                    "visual_prompt": timeline.body_visual_prompt,
                    "transition": timeline.body_transition,
                },
                {
                    "id": "LEGACY",
                    "audio": str(legacy_audio),
                    "duration": timeline.legacy_duration,
                    "visual_prompt": timeline.legacy_visual_prompt,
                    "transition": timeline.legacy_transition,
                }
            ],
            "output": {
                "resolution": "1080p",
                "format": "mp4"
            }
        }

    # ------------------------------------------------------------
    #  Запуск рендера
    # ------------------------------------------------------------
    def render(self, storyboard: dict, output_dir: Path) -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        # 1. Отправляем задачу
        response = requests.post(
            f"{self.endpoint}/render",
            headers=headers,
            data=json.dumps(storyboard)
        )
        response.raise_for_status()

        job_id = response.json()["job_id"]

        # 2. Ожидаем завершения
        while True:
            status = requests.get(
                f"{self.endpoint}/status/{job_id}",
                headers=headers
            ).json()

            if status["state"] == "completed":
                break

            if status["state"] == "failed":
                raise RuntimeError(f"Foundry render failed: {status}")

            time.sleep(2)

        # 3. Скачиваем результат
        video_url = status["result_url"]
        output_path = output_dir / "final_video.mp4"

        video_data = requests.get(video_url)
        with open(output_path, "wb") as f:
            f.write(video_data.content)

        return output_path
