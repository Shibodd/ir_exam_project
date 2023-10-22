import json
import requests
from typing import Union
import logging

logger = logging.getLogger(__name__)

class InferenceAPIError(Exception):
  def __init__(self, status_code, response_content):
    self.status_code = status_code
    self.response_content = response_content

  def __str__(self) -> str:
    return f"Huggingface replied with status code {self.status_code}: {self.response_content}"


def classify_text(text: Union[list, str], model: str, wait_for_model=False, timeout=None):
  API_URL = f"https://api-inference.huggingface.co/models/{model}"
  API_TOKEN = "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"
  
  headers = {"Authorization": f"Bearer {API_TOKEN}"}
  data = { "inputs": text }
  if wait_for_model:
    data['options'] = { 'wait_for_model': True }

  response = requests.request("POST", API_URL, headers=headers, data=json.dumps(data), timeout=timeout)

  response_content = json.loads(response.content.decode("utf-8"))
  if response.status_code != 200:
    raise InferenceAPIError(response.status_code, response_content)
  
  return response_content


def blocking_classify_text(text: Union[list, str], model: str):
  wait_for_model = False

  while True:
    try:
      return classify_text(text, model, wait_for_model)
    except InferenceAPIError as e:
      # If the API throws a loading error, try again only once
      if wait_for_model or e.status_code != 503 or not e.response_content.contains('loading'):
        raise
      else:
        wait_for_model = True
        logger.warning("Inference model is loading...")