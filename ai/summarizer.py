from __future__ import annotations

from dataclasses import dataclass

from ai.open_ai_client import OpenAIClient

_SYSTEM_PROMPT = (
    "You are a news summarization assistant.\n"
    "Summarize the user's text in Korean in AT MOST 3 lines.\n"
    "Each line must be ONE sentence.\n"
    "Be concise and remove redundancy.\n"
    "Do not add opinions or speculation. Use only information from the text.\n"
    "Do not include introductions, disclaimers, titles, or extra lines.\n"
    "If the text lacks information, summarize only what is present without guessing."
)

_CHUNK_PROMPT = (
    "You are a news summarization assistant.\n"
    "Summarize the user's text (a partial chunk of a longer article) in Korean in AT MOST 2 lines.\n"
    "Each line must be ONE sentence.\n"
    "Be concise. Facts only from the text. No speculation.\n"
    "No titles, no introductions, no disclaimers."
)


@dataclass(frozen=True)
class SummaryResult:
    """Parsed result for a summary request."""

    text: str


class Summarizer:
    """Summarizes news/article text into AT MOST 3 lines in Korean."""

    def __init__(
        self,
        client: OpenAIClient,
        *,
        max_input_chars: int = 12000,
        chunk_size_chars: int = 2000,
        chunk_overlap_chars: int = 200,
    ):
        self._client = client
        self._max_input_chars = max_input_chars
        self._chunk_size_chars = chunk_size_chars
        self._chunk_overlap_chars = chunk_overlap_chars

    def summarize(self, msg: str) -> SummaryResult:
        """Summarize a news/article text into AT MOST 3 lines in Korean."""
        if msg is None or not str(msg).strip():
            raise ValueError("msg must be a non-empty string")

        full_text = str(msg).strip()
        user_text = self._prepare_input(full_text)

        result = self._client.chat(
            system_prompt=_SYSTEM_PROMPT,
            user_text=user_text,
            max_tokens=140,
            temperature=0.2,
        )

        # Enforce AT MOST 3 lines; drop preamble lines (e.g. "Here's a summary:")
        lines = [ln.strip() for ln in result.splitlines() if ln.strip()]
        content = [ln for ln in lines if ln.startswith(("*", "-", "•")) or ln[0].isdigit()]
        result_lines = content if content else lines
        return SummaryResult(text="\n".join(result_lines[:3]))

    def _prepare_input(self, full_text: str) -> str:
        """Prepare input for summarization.

        - Short text: use directly.
        - Long text: split into chunks, summarize each (<=2 lines),
          then combine as input for the final summary call in summarize().
        """
        text = (full_text or "").strip()
        if len(text) <= self._max_input_chars:
            return text

        chunks = self._chunk_text(text)
        partial_summaries: list[str] = []
        for chunk in chunks:
            partial = self._client.chat(
                system_prompt=_CHUNK_PROMPT,
                user_text=chunk,
                max_tokens=120,
                temperature=0.2,
            )
            lines = [ln.strip() for ln in partial.splitlines() if ln.strip()]
            partial_summaries.append("\n".join(lines[:2]) if lines else "")

        return "\n".join(s for s in partial_summaries if s).strip()

    def _chunk_text(self, text: str) -> list[str]:
        """Split text into overlapping character chunks."""
        size = max(200, int(self._chunk_size_chars))
        overlap = max(0, min(int(self._chunk_overlap_chars), size // 2))
        chunks: list[str] = []
        start = 0
        n = len(text)
        while start < n:
            end = min(n, start + size)
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            if end >= n:
                break
            start = end - overlap
        return chunks[:20]