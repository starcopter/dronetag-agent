import asyncio
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from gateway import DronetagGateway
from oprn import OPRN

templates = Jinja2Templates(directory="templates")
static_files = StaticFiles(directory="static")

MAVLINK_IP = os.environ.get("MAVLINK_IP")
MAVLINK_PORT = int(os.environ.get("MAVLINK_PORT", 5790))
HIGHDRA = os.environ.get("HIGHDRA_SERIAL_NUMBER", "1715800000000")

try:
    SKYNODE = Path("/etc/skynode").read_text().strip().split("-")[-1]
except FileNotFoundError:
    SKYNODE = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    if MAVLINK_IP:
        gateway = DronetagGateway(MAVLINK_IP, MAVLINK_PORT)
        gateway_task = asyncio.create_task(gateway.run())

    yield

    if MAVLINK_IP:
        gateway_task.cancel()


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


@app.post("/oprn", response_class=HTMLResponse)
async def post_oprn(request: Request, oprn: Annotated[str, Form()]):
    global cached_oprn
    try:
        cached_oprn = OPRN(oprn)
    except ValueError as e:
        return templates.TemplateResponse(request, "blocks/oprn-form.html", {"oprn": oprn, "oprn_error": str(e)})
    return templates.TemplateResponse(
        request, "blocks/oprn-form.html", {"oprn": cached_oprn.public_part if cached_oprn else None}
    )


@app.delete("/oprn", response_class=HTMLResponse)
async def delete_oprn(request: Request):
    global cached_oprn
    cached_oprn = None
    return templates.TemplateResponse(request, "blocks/oprn-form.html")
