import json
import requests

def valuta_testo(mandorla):
    API_TOKEN = "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"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    API_URL = "https://api-inference.huggingface.co/models/SamLowe/roberta-base-go_emotions"
    def query(payload):
        data = json.dumps(payload)
        response = requests.request("POST", API_URL, headers=headers, data=data)
        return json.loads(response.content.decode("utf-8"))
    data = query({"inputs": mandorla})
    return data