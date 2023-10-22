from sentiment import SentimentVector
import huggingface
from typing import Union

def classify_text(text: Union[list, str]):
  data = huggingface.inference_api.blocking_classify_text(text, "j-hartmann/emotion-english-distilroberta-base")

  def parse_classification(classification):
    ans = SentimentVector()
    for sent in classification:
      ans.vector += SentimentVector(sent['label']).vector * sent['score']
    return ans

  return [parse_classification(classification) for classification in data]
