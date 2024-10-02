import os
import re
from typing import Any, Sequence
from langchain_core.documents import BaseDocumentTransformer, Document
from langchain_core.language_models.llms import LLM
from .prompt import SYSTEM_PROMPT, HUMAN_PROMPT
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.runnables import RunnableLambda
from langchain_core.messages.ai import AIMessage


class LumberChunker(BaseDocumentTransformer):
    def __init__(
        self,
        llm: LLM,
        separators: list[str] = ["\n\n", "\n", "。"],
        max_tokens: int = 500,
        prompt: str = None,
    ):
        self.llm = llm
        self.pattern = "|".join(map(re.escape, separators))

        self.prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT),
                HumanMessagePromptTemplate.from_template(HUMAN_PROMPT),
            ]
        )
        output_parser = RunnableLambda(self.__extract_id)
        self.chain = self.prompt | self.llm | output_parser
        self.max_tokens = max_tokens

    def split_text(
        self,
        text: str,
    ) -> list[str]:
        texts = self.__split(text)

        results = []
        current_idx = 0
        for _ in range(len(texts)):
            context = self.__create_context(texts, current_idx)
            if not context:
                break

            id = self.chain.invoke({"context": context})
            next_idx = int(id) + 1
            if current_idx >= len(texts) or next_idx == current_idx:
                break

            text = "".join(texts[current_idx:next_idx])
            if text:
                results.append(text)

            current_idx = next_idx

        return results

    def transform_documents(
        self, documents: Sequence[Document], **kwargs: Any
    ) -> Sequence[Document]: ...

    def __split(self, text: str):
        texts = re.split(f"({self.pattern})", text)

        result = []
        buffer = ""

        for part in texts:
            if part in self.pattern:
                buffer += re.sub(r"^[ \t]+", "", part)
                if buffer:
                    result.append(self.__normalize_text(buffer))
                buffer = ""
            else:
                if buffer:
                    result.append(self.__normalize_text(buffer))
                buffer = re.sub(r"^[ \t]+", "", part)

        if buffer:
            result.append(self.__normalize_text(buffer))

        return result

    def __count_words(self, text_size: int) -> int:
        return round(3 * text_size)

    def __create_context(self, texts: list[str], idx: int) -> str:
        total_words = 0
        context = ""
        for id, text in enumerate(texts[idx:], start=idx):
            total_words += self.__count_words(len(text))
            if total_words < self.__count_words(self.max_tokens):
                context += f"ID {id:04}: {text}{os.linesep}"
            else:
                break

        return context

    def __normalize_text(self, text: str) -> str:
        return text.replace("\u3000", " ")

    def __extract_id(self, result: AIMessage) -> int | None:
        pattern = r".*?ID\s*.*?(\d+)"
        match = re.match(pattern, result.content)
        if match:
            return int(match.group(1))
        else:
            return None
