from collections.abc import AsyncIterable, Sequence
from collections import defaultdict
from contextlib import asynccontextmanager
import os
from datetime import datetime, timezone, timedelta
from pathlib import Path
from fastapi import FastAPI, Request
import libmav
import asyncio

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from async_libmav import AsyncLibmavConnection

LAST_MESSAGES_MAX_AGE = timedelta(seconds=10)

templates = Jinja2Templates(directory="templates")
static_files = StaticFiles(directory="static")


def get_skynode_serial_number() -> str | None:
    try:
        return Path("/etc/skynode").read_text().strip().split("-")[-1]
    except FileNotFoundError:
        return None


class MessageEntry(BaseModel):
    system_id: int
    component_id: int
    message_id: int
    name: str
    timestamp: datetime

    @classmethod
    def from_mavlink_message(
        cls, msg: libmav.Message, timestamp: datetime | None = None
    ):
        return cls(
            system_id=msg.header.system_id,
            component_id=msg.header.component_id,
            name=msg.name,
            message_id=msg.id,
            timestamp=timestamp or datetime.now(timezone.utc),
        )


class MessageRate(BaseModel):
    name: str
    system_id: int
    component_id: int
    message_id: int
    rate: float


def calculate_rates(messages: Sequence[MessageEntry]) -> list[MessageRate]:
    count: defaultdict[tuple[int, int, int, str], int] = defaultdict(int)
    for msg in messages:
        count[(msg.system_id, msg.component_id, msg.message_id, msg.name)] += 1

    message_rates = [
        MessageRate(
            name=k[3],
            system_id=k[0],
            component_id=k[1],
            message_id=k[2],
            rate=v / LAST_MESSAGES_MAX_AGE.total_seconds(),
        )
        for k, v in count.items()
    ]
    return sorted(
        message_rates,
        key=lambda x: (-x.rate, x.system_id, x.component_id, x.message_id),
    )


message_buffer_lock = asyncio.Lock()
message_buffer: list[MessageEntry] = []


async def handle_mavlink_messages(message_iterator: AsyncIterable[libmav.Message]):
    async for msg in message_iterator:
        now = datetime.now(timezone.utc)
        entry = MessageEntry.from_mavlink_message(msg, now)
        async with message_buffer_lock:
            message_buffer.append(entry)
            drop_index = 0
            for i, msg in enumerate(message_buffer):
                if msg.timestamp < now - LAST_MESSAGES_MAX_AGE:
                    drop_index = i
                else:
                    break
            del message_buffer[:drop_index]


@asynccontextmanager
async def lifespan(app: FastAPI):
    ip = "172.17.0.1" if get_skynode_serial_number() else "10.41.0.1"
    conn_phy = libmav.TCPClient(ip, 5790)
    conn = AsyncLibmavConnection(conn_phy)
    runner = asyncio.create_task(conn.run())
    other_task = asyncio.create_task(handle_mavlink_messages(conn))

    yield

    other_task.cancel()
    runner.cancel()


app = FastAPI(lifespan=lifespan)
app.mount("/static", static_files, name="static")


@app.get("/", response_class=HTMLResponse)
def get_index(request: Request):
    params = {
        "HIGHDRA Serial Number": os.environ.get("HIGHDRA_SERIAL_NUMBER"),
        "Skynode Serial Number": get_skynode_serial_number(),
    }
    return templates.TemplateResponse(
        request, "index.html", {"title": "Dronetag Agent", "metadata": params}
    )


@app.get("/env")
def read_env():
    return dict(os.environ)


async def get_message_table_context() -> dict:
    async with message_buffer_lock:
        rates = calculate_rates(message_buffer)
    return {"title": "Messages", "messages": rates}


@app.get("/messages/table", name="message_table", response_class=HTMLResponse)
async def get_message_table(request: Request):
    context = await get_message_table_context()
    return templates.TemplateResponse(request, "blocks/message-table.html", context)


@app.get("/messages", response_class=HTMLResponse)
async def read_messages(request: Request):
    context = await get_message_table_context()
    return templates.TemplateResponse(request, "messages.html", context)
