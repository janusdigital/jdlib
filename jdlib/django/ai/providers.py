from django.conf import settings
from django.utils.functional import SimpleLazyObject

from jdlib.ai.providers import OpenAI as BaseOpenAI


class OpenAI(BaseOpenAI):
    def __init__(self):
        super().__init__(settings.OPENAI_API_KEY)


openai = SimpleLazyObject(lambda: OpenAI())
