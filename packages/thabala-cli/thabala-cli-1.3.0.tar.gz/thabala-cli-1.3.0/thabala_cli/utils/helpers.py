from itertools import filterfalse
from itertools import tee
from typing import Callable
from typing import Dict
from typing import Iterable

from thabala_cli.exceptions import ThabalaCliApiException


def partition(pred: Callable, iterable: Iterable):
    """User a predicate to partition entries into false entries and true entries"""
    iter_1, iter_2 = tee(iterable)
    return filterfalse(pred, iter_1), filter(pred, iter_2)


def raise_thabala_cli_api_exc(err: Exception, response_json: Dict = None) -> None:
    title = None
    detail = None

    if response_json:
        title = response_json.get("title") or ""
        detail = response_json.get("detail") or ""

    raise ThabalaCliApiException(
        f"{err} - {title} - {detail}" if title or detail else err
    )
