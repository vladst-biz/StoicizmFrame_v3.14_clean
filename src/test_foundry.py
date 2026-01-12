from ai.azure_foundry_client import AzureFoundryClient

client = AzureFoundryClient()

reply = client.chat([
    {"role": "user", "content": "Тест соединения. Ответь одним словом."}
])

print("Ответ модели:", reply)
