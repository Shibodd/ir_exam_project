import aiohttp
from typing import Union
import logging
import asyncio
logger = logging.getLogger(__name__)

class InferenceAPIError(Exception):
  def __init__(self, status_code, response_content):
    self.status_code = status_code
    self.response_content = response_content

  def __str__(self) -> str:
    return f"Huggingface replied with status code {self.status_code}: {self.response_content}"


async def classify_text(text: Union[list, str], model: str, wait_for_model=False, timeout=None):
  API_URL = f"https://api-inference.huggingface.co/models/{model}"
  API_TOKEN = "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"
  
  headers = { "Authorization": f"Bearer {API_TOKEN}" }
  data = { "inputs": text }
  if wait_for_model:
    data['options'] = { 'wait_for_model': True }

  async with aiohttp.ClientSession() as session:
    async with session.post(API_URL, headers=headers, json=data, timeout=timeout) as response:
      content = await response.json(encoding="utf-8")
      if response.status != 200:
        raise InferenceAPIError(response.status, content)
      return content


async def blocking_classify_text(text: Union[list, str], model: str):
  wait_for_model = False

  while True:
    try:
      return await classify_text(text, model, wait_for_model)
    except:
      logger.warning("Inference model exception")
      asyncio.sleep(1)
      pass
    #except InferenceAPIError as e:
    #  # If the API throws a loading error, try again only once
    #  if wait_for_model or e.status_code != 503 or 'loading' not in e.response_content['error']:
    #    raise
    #  else:
    #    wait_for_model = True
    #    logger.warning("Inference model is loading...")