import asyncio
from functools import partial, wraps


def async_wrapper(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        partial_function = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, partial_function)

    return run
