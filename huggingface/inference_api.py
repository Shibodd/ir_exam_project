import json
import requests
from typing import Union

class InferenceAPIError(Exception):
  def __init__(self, status_code, response_content):
    self.status_code = status_code
    self.response_content = response_content

  def __str__(self) -> str:
    return f"Huggingface replied with status code {self.status_code}: {self.response_content}"


def classify_text(mandorla: Union[list, str], model: str):
  API_URL = f"https://api-inference.huggingface.co/models/{model}"
  API_TOKEN = "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"
  
  headers = {"Authorization": f"Bearer {API_TOKEN}"}
  data = json.dumps({"inputs": mandorla})
  response = requests.request("POST", API_URL, headers=headers, data=data)

  response_content = json.loads(response.content.decode("utf-8"))
  if response.status_code != 200:
    raise InferenceAPIError(response.status_code, response_content)
  
  return response_content
