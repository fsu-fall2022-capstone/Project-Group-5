import asyncio

from functools import wraps, partial

def async_wrapper(func):
    @wraps(func)
    async def run(*args, loop = None, executor = None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        partial_func = partial(executor, func)
        return await loop.run_in_executor(executor, partial_func)
    return run