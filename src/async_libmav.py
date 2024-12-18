import asyncio
import functools
import logging
from pathlib import Path

import libmav

DEFAULT_MESSAGE_SET_LOCATION = Path(__file__).parent / "mavlink/common.xml"

logger = logging.getLogger(__name__)


class AsyncLibmavConnection:
    def __init__(
        self,
        phy: libmav.NetworkInterface,
        message_set: libmav.MessageSet | None = None,
        system_id: int = 1,
        component_id: int = 52,
        heartbeat: libmav.Message | None = None,
    ):
        if message_set is None:
            message_set = libmav.MessageSet(str(DEFAULT_MESSAGE_SET_LOCATION))

        self.message_set = message_set
        identifier = libmav.Identifier(system_id, component_id)
        if heartbeat is not None:
            self._runtime = libmav.NetworkRuntime(identifier, message_set, heartbeat, phy)
        else:
            self._runtime = libmav.NetworkRuntime(identifier, message_set, phy)

        self._loop = asyncio.get_running_loop()
        self._tx_queue: asyncio.Queue[libmav.Message] = asyncio.Queue()
        self._rx_queue: asyncio.Queue[libmav.Message] = asyncio.Queue()

    def __aiter__(self):
        return self

    async def __anext__(self):
        return await self._rx_queue.get()

    async def run(self):
        conn = await asyncio.to_thread(self._runtime.await_connection, 10000)
        logger.info("libmav connected")

        callback = functools.partial(self._loop.call_soon_threadsafe, self._rx_queue.put_nowait)
        conn.add_message_callback(callback)

        while True:
            try:
                msg = await self._tx_queue.get()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.exception("tx queue get failed: %s", e, exc_info=True)
                continue
            else:
                conn.send(msg)

        return
