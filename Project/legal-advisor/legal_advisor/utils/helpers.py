import re
from typing import Union
from langchain.schema import Document

class Cleaner:
    def __init__(self, docs: Union[list[Document], str]):
        self.docs = docs

    def combiner(self) -> "Cleaner":
        if isinstance(self.docs, list):
            self.docs = " ".join([content.page_content for content in self.docs])
        return self

    def clean_legal_text(self) -> "Cleaner":
        """Clean and normalize legal text."""
        if not isinstance(self.docs, str):
            raise TypeError("Run combiner() first to convert docs into text.")

        text = self.docs
        text = re.sub(r'Page \d+ of \d+', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\b\d+\s*/\s*\d+\b', '', text)
        text = re.sub(r'\b(Confidential|Draft|Proprietary)\b', '', text, flags=re.IGNORECASE)
        text = text.replace("\n", " ")
        text = re.sub(r'[_*•·]+', ' ', text)
        text = re.sub(r'\.{2,}', '.', text)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\x00-\x7F]+', '', text)

        self.docs = text.strip()
        return self
