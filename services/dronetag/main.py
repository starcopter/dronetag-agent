from collections.abc import AsyncIterable
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

from async_libmav import AsyncLibmavConnection

templates = Jinja2Templates(directory="templates")
static_files = StaticFiles(directory="static")


def get_skynode_serial_number() -> str | None:
    try:
        return Path("/etc/skynode").read_text().strip().split("-")[-1]
    except FileNotFoundError:
        return None


last_messages: dict[tuple[int, int, str], datetime] = {}


async def handle_mavlink_messages(message_iterator: AsyncIterable[libmav.Message]):
    async for msg in message_iterator:
        key = (msg.header.system_id, msg.header.component_id, msg.name)
        now = datetime.now(timezone.utc)
        if key not in last_messages:
            print(
                f"New message: {msg.name} from {msg.header.system_id}.{msg.header.component_id}"
            )
        last_messages[key] = now


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


@app.get("/messages", response_class=HTMLResponse)
def read_messages(request: Request):
    now = datetime.now(timezone.utc)
    messages = [
        {
            "name": k[2],
            "system_id": k[0],
            "component_id": k[1],
            "age": (now - v).total_seconds(),
        }
        for k, v in sorted(last_messages.items(), key=lambda kv: kv[1], reverse=True)
    ]
    return templates.TemplateResponse(
        request,
        "messages.html",
        {"title": "Messages", "messages": messages},
    )
