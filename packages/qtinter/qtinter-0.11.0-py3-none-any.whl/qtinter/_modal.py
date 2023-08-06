"""Implement helper function modal"""

import asyncio
import functools
from ._base_events import QiBaseEventLoop


__all__ = 'modal',


def modal(fn):

    @functools.wraps(fn)
    async def modal_wrapper(*args, **kwargs):
        loop = asyncio.get_running_loop()
        if not isinstance(loop, QiBaseEventLoop):
            raise RuntimeError(f'qtinter.modal() requires QiBaseEventLoop, '
                               f'but got {loop!r}')

        def modal_fn():
            try:
                result = fn(*args, **kwargs)
            except BaseException as exc:
                future.set_exception(exc)
            else:
                future.set_result(result)

        future = asyncio.Future()
        loop.exec_modal(modal_fn)
        return await asyncio.shield(future)

    return modal_wrapper
