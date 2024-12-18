import asyncio
import queue
import threading

import libmav


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
            message_set = libmav.MessageSet("mavlink/common.xml")

        self.message_set = message_set
        identifier = libmav.Identifier(system_id, component_id)
        if heartbeat is not None:
            self._runtime = libmav.NetworkRuntime(identifier, message_set, heartbeat, phy)
        else:
            self._runtime = libmav.NetworkRuntime(identifier, message_set, phy)

        self._loop = asyncio.get_event_loop()
        self._worker: asyncio.Future | None = None

        self._shutdown_request = threading.Event()
        self._running = asyncio.Event()
        self._tx_queue: queue.Queue[libmav.Message] = queue.Queue()
        self._rx_queue: asyncio.Queue[libmav.Message] = asyncio.Queue()

    def start(self):
        if self._worker is not None and not self._worker.done():
            raise RuntimeError("Worker already running")
        self._worker = self._loop.run_in_executor(None, self._worker_task)

    def stop(self):
        self._shutdown_request.set()
        if self._worker:
            self._worker.cancel()

    def __aiter__(self):
        return self

    async def __anext__(self):
        return await self._rx_queue.get()

    def _worker_task(self):
        conn = self._runtime.await_connection(5000)

        def _message_callback(msg: libmav.Message):
            asyncio.run_coroutine_threadsafe(self._rx_queue.put(msg), self._loop)

        conn.add_message_callback(_message_callback)

        while not self._shutdown_request.is_set():
            try:
                msg = self._tx_queue.get(0.1)
                conn.send(msg)
            except queue.Empty:
                pass
