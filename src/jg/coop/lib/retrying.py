import logging
from collections.abc import Callable
from functools import partial
from typing import Any, Protocol, TypeVar, cast

from tenacity import (
    before_sleep_log,
    retry as tenacity_retry,
    stop_after_attempt,
    wait_random_exponential,
)
from tenacity.retry import RetryBaseT
from tenacity.stop import StopBaseT
from tenacity.wait import WaitBaseT

from jg.coop.lib import loggers


logger = loggers.from_path(__file__)


WrappedFn = TypeVar("WrappedFn", bound=Callable[..., Any])


class RetryDecorator(Protocol):
    def __call__(
        self,
        *,
        retry: RetryBaseT = ...,
        stop: StopBaseT = ...,
        wait: WaitBaseT = ...,
        reraise: bool = ...,
        before_sleep: Callable[..., Any] | None = ...,
        retry_error_callback: Callable[..., Any] | None = ...,
        **kwargs: Any,
    ) -> Callable[[WrappedFn], WrappedFn]: ...


retry = cast(
    RetryDecorator,
    partial(
        tenacity_retry,
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_random_exponential(max=60),
        before_sleep=before_sleep_log(logger, logging.DEBUG),
    ),
)
