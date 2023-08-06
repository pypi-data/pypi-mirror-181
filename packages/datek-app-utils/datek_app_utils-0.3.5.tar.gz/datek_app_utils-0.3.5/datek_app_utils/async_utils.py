from abc import abstractmethod
from asyncio import Task, sleep, CancelledError, create_task, gather, Future
from functools import wraps
from typing import Callable, Optional


class AsyncWorker:
    def __init__(self):
        self._task: Optional[Task] = None
        self._started = Future()

    @abstractmethod
    async def run(self):  # pragma: no cover
        pass

    @abstractmethod
    async def handle_error(self, error: Exception):  # pragma: no cover
        pass

    def start(self):
        self._task = create_task(self._run_forever())

    async def wait_started(self):
        await self._started

    def stop(self):
        if self._task and not self._task.done():
            self._task.cancel()

    async def _run_forever(self):
        self._started.set_result(1)

        while True:
            try:
                await self.run()
            except CancelledError:
                return
            except Exception as error:
                await self.handle_error(error)

    def __await__(self):
        return self._task.__await__()


def async_timeout(seconds: float):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            timeout_task: Optional[Task] = None
            main_task: Optional[Task] = None

            async def raise_timeout_error():
                try:
                    await sleep(seconds)
                except CancelledError:
                    return

                if main_task:
                    main_task.cancel()

                raise TimeoutError

            async def main():
                try:
                    return await func(*args, **kwargs)
                except Exception:
                    raise
                finally:
                    if timeout_task:
                        timeout_task.cancel()

            timeout_task = create_task(raise_timeout_error())
            main_task = create_task(main())

            result, _ = await gather(main_task, timeout_task)
            return result

        return wrapper

    return decorator
