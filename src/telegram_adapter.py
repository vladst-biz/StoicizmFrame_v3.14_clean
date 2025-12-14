# telegram_adapter.py
# StoicizmFrame v3.14_clean — Telegram Adapter
# Кодировка: UTF-8 LF, без BOM

import requests

class TelegramAdapter:
    def __init__(self, api_key: str, chat_id: str):
        self.api_key = api_key
        self.chat_id = chat_id
        self.endpoint = f"https://api.telegram.org/bot{api_key}/sendMessage"

    def send_message(self, text: str):
        payload = {"chat_id": self.chat_id, "text": text}
        response = requests.post(self.endpoint, data=payload)
        return response.json()
