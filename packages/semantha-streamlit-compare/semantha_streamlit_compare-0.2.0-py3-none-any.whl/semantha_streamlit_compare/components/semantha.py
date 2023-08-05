import json
import io
from typing import Dict, Optional, Tuple

import requests
import semantha_sdk

from types import SimpleNamespace


def _to_text_file(text: str):
    input_file = io.BytesIO(text.encode("utf-8"))
    input_file.name = "input.txt"
    return input_file


class Semantha:

    def __init__(
        self,
        server_base_url,
        api_key: Optional[str] = None,
    ):
        self.__semantha = semantha_sdk.login(server_base_url, api_key)

    def compare_with_omd(
        self, input_0: str, input_1: str, domain: str, document_type: str
    ) -> Tuple[float, bool]:
        document = self.__semantha.domains.get_one(domain).references.post(file= _to_text_file(input_1),
            reference_document= _to_text_file(input_0),
            simsimilarity_thresholdilaritythreshold= str(0.01),
            max_references= 1,
            document_type = document_type,
            with_context= False)
        if len(document.references) > 0:
            reference = document.pages[0].contents[0].paragraphs[0].references[0]
            contradictory = True if reference.has_opposite_meaning else False
            similarity = document.references[0].similarity
            return similarity, contradictory