import io
import re
from typing import Any, Callable, Dict, List, TypeVar

from pypdf import PdfReader

T = TypeVar("T", bound=Callable[..., Any])


class PyPDFLibrary:
    def __init__(self):
        self._fh: io.FileIO | None = None
        self._reader: PdfReader | None = None

    def _validate_reader(func: T) -> T:
        def wrapper(self: "PyPDFLibrary", *args: Any, **kwargs: Any):
            if not self._reader:
                raise ValueError("Open PDF file first")
            return func(self, *args, **kwargs)

        return wrapper

    def open_pdf(self, file_path: str) -> None:
        self._fh = open(file_path, "rb")
        self._reader = PdfReader(self._fh)

    @_validate_reader
    def parse_text(self) -> Dict[int, str]:
        pages = {}
        for page_index, page in enumerate(self._reader.pages):
            pages[page_index] = page.extract_text()
        return pages

    @staticmethod
    def flatten(nested: List[any]) -> List[str]:
        return [
            element
            for sublist in nested
            for element in (sublist if isinstance(sublist, tuple) else (sublist,))
        ]

    @_validate_reader
    def find_matches(self, pattern: re.Pattern) -> List[str]:
        matches = []
        for page in self._reader.pages:
            text = page.extract_text()
            match = re.findall(pattern, text, re.MULTILINE)
            if match:
                matches.extend(self.flatten(match))
        return matches

    def close(self) -> None:
        if self._fh:
            self._fh.close()
