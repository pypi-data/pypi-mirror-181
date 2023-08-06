"""
Utilities to implement functional retry policies for coroutines.
"""

import logging
import time
from functools import wraps
from typing import Awaitable, Callable, Sequence, Type, TypeVar

from typing_extensions import ParamSpec

P = ParamSpec("P")
T = TypeVar("T")


logger = logging.getLogger(__name__)


class RetryLimitExceeded(Exception):
    """Function raised more exceptions than allowed."""


def retry_policy(
    min_retry_interval_seconds: float = 1,
    max_retry_interval_seconds: float = 60,
    max_retry_count: int = 10,
    retryable_exceptions: Sequence[Type[Exception]] = (Exception,),
) -> Callable[[Callable[P, Awaitable[T]]], Callable[P, Awaitable[T]]]:
    """Decorate function to execute in managed retry environment."""

    def coroutine_with_retry_policy(
        coroutine: Callable[P, Awaitable[T]]
    ) -> Callable[P, Awaitable[T]]:
        @wraps(coroutine)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            retry_count = 0
            retry_interval_seconds = min_retry_interval_seconds

            while True:
                try:
                    return await coroutine(*args, **kwargs)
                except tuple(retryable_exceptions) as e:
                    if retry_count >= max_retry_count:
                        # Construct dynamically created exception which subclasses from
                        # RetryLimitExceeded and the exception raised from the callable
                        # to preserve exception handling behavior of the caller.
                        raise type("RetryFailed", (RetryLimitExceeded, type(e)), {})

                    logger.warning("Retrying exception: %s", repr(e))
                    time.sleep(retry_interval_seconds)

                    retry_count += 1
                    retry_interval_seconds = min(
                        retry_interval_seconds * 2, max_retry_interval_seconds
                    )

        return wrapper

    return coroutine_with_retry_policy
