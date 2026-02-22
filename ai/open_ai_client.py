from __future__ import annotations

from openai import OpenAI


class OpenAIClient:
    """Thin wrapper around the OpenAI chat completion API."""

    def __init__(
        self,
        base_url: str = "http://localhost:5555/v1",
        api_key: str | None = None,
        model: str = "local-model",
        timeout: float = 60.0,
    ):
        self._client = OpenAI(base_url=base_url, api_key=api_key, timeout=timeout)
        self._model = model

    def chat(
        self,
        system_prompt: str,
        user_text: str,
        *,
        max_tokens: int = 256,
        temperature: float = 0.7,
        top_p: float = 0.9,
    ) -> str:
        """Send a chat completion request and return the response text."""
        completion = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
        )
        return self._extract_content(completion)

    @staticmethod
    def _extract_content(completion) -> str:
        choices = getattr(completion, "choices", None)
        if not choices:
            raise RuntimeError("No choices returned from completion")
        message = getattr(choices[0], "message", None)
        content = getattr(message, "content", None) if message is not None else None
        if content is None:
            raise RuntimeError("No message content returned from completion")
        return str(content).strip()