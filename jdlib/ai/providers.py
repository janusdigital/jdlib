from openai import AsyncOpenAI as AsyncOpenAIClient
from openai import OpenAI as OpenAIClient


class OpenAI:
    """Wrapper around the OpenAI API client."""

    def __init__(self, api_key) -> None:
        self.client = OpenAIClient(api_key=api_key)
        self.async_client = AsyncOpenAIClient(api_key=api_key)

    def _build_messages(self, prompt, system=None):
        messages = []
        if system:
            messages.append({'role': 'system', 'content': system})
        messages.append({'role': 'user', 'content': prompt})
        return messages

    def _chat_params(self, messages, model='gpt-4o-mini', temperature=0.5, **kwargs):
        return {'model': model, 'messages': messages, 'temperature': temperature, **kwargs}

    def chat(self, messages, **kwargs):
        """Send a chat completion request and return the response content."""
        response = self.client.chat.completions.create(**self._chat_params(messages, **kwargs))
        return response.choices[0].message.content

    async def achat(self, messages, **kwargs):
        """Send an async chat completion request and return the response content."""
        response = await self.async_client.chat.completions.create(**self._chat_params(messages, **kwargs))
        return response.choices[0].message.content

    def complete(self, prompt, system=None, **kwargs):
        """Send a single prompt completion request."""
        return self.chat(self._build_messages(prompt, system), **kwargs)

    async def acomplete(self, prompt, system=None, **kwargs):
        """Send a single async prompt completion request."""
        return await self.achat(self._build_messages(prompt, system), **kwargs)
