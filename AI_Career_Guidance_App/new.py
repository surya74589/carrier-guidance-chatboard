import requests

API_KEY = "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"  # use your real key

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

response = requests.get("https://openrouter.ai/api/v1/models", headers=headers)
models = response.json()

for model in models.get("data", []):
    print(model["id"])
