import asyncio
import os
from collections import defaultdict
from collections.abc import AsyncIterable, Sequence
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Annotated

import libmav
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from async_libmav import AsyncLibmavConnection
from gateway import DronetagGateway
from oprn import OPRN

LAST_MESSAGES_MAX_AGE = timedelta(seconds=10)

templates = Jinja2Templates(directory="templates")
static_files = StaticFiles(directory="static")

MAVLINK_IP = os.environ.get("MAVLINK_IP")
MAVLINK_PORT = int(os.environ.get("MAVLINK_PORT", 5790))
HIGHDRA = os.environ.get("HIGHDRA_SERIAL_NUMBER", "1715800000000")

try:
    SKYNODE = Path("/etc/skynode").read_text().strip().split("-")[-1]
except FileNotFoundError:
    SKYNODE = None


class MessageEntry(BaseModel):
    system_id: int
    component_id: int
    message_id: int
    name: str
    timestamp: datetime

    @classmethod
    def from_mavlink_message(cls, msg: libmav.Message, timestamp: datetime | None = None):
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
    if MAVLINK_IP:
        conn_phy = libmav.TCPClient(MAVLINK_IP, MAVLINK_PORT)
        conn = AsyncLibmavConnection(conn_phy)
        runner = asyncio.create_task(conn.run())
        other_task = asyncio.create_task(handle_mavlink_messages(conn))

        gateway = DronetagGateway(MAVLINK_IP, MAVLINK_PORT)
        gateway_task = asyncio.create_task(gateway.run())

    yield

    if MAVLINK_IP:
        gateway_task.cancel()
        other_task.cancel()
        runner.cancel()


app = FastAPI(lifespan=lifespan)
app.mount("/static", static_files, name="static")

cached_oprn: OPRN | None = None


@app.get("/", response_class=HTMLResponse)
def get_index(request: Request):
    params = {
        "title": "Dronetag Agent",
        "highdra_serial_number": HIGHDRA,
        "skynode_serial_number": SKYNODE,
    }
    if cached_oprn:
        params["oprn"] = cached_oprn.public_part
    return templates.TemplateResponse(request, "index.html", params)


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


@app.post("/oprn")
async def post_oprn(request: Request, oprn: Annotated[str, Form()]):
    global cached_oprn
    try:
        cached_oprn = OPRN(oprn)
    except ValueError as e:
        return templates.TemplateResponse(request, "blocks/oprn-form.html", {"oprn": oprn, "oprn_error": str(e)})
    return templates.TemplateResponse(
        request, "blocks/oprn-form.html", {"oprn": cached_oprn.public_part if cached_oprn else None}
    )


@app.delete("/oprn")
async def delete_oprn(request: Request):
    global cached_oprn
    cached_oprn = None
    return templates.TemplateResponse(request, "blocks/oprn-form.html")
