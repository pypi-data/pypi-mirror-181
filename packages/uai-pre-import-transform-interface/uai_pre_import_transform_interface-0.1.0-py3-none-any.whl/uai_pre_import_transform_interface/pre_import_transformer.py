from abc import ABC, abstractmethod

from uai_uri_interface import URI


class PreImportTransformerInterface(ABC):
    @abstractmethod
    def transform(self, input_path: URI, output_path: URI) -> None:
        ...
