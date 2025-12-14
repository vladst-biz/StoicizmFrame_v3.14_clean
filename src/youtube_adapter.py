# youtube_adapter.py
# StoicizmFrame v3.14_clean — YouTube Adapter
# Кодировка: UTF-8 LF, без BOM

import requests

class YouTubeAdapter:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.upload_endpoint = "https://www.googleapis.com/upload/youtube/v3/videos"

    def upload_video(self, file_path: str, title: str, description: str, tags: list):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {"part": "snippet,status"}
        files = {
            "snippet": (
                None,
                {"title": title, "description": description, "tags": tags},
                "application/json"
            ),
            "video": open(file_path, "rb")
        }
        response = requests.post(self.upload_endpoint, headers=headers, params=params, files=files)
        return response.json()
