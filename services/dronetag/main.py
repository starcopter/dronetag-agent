import os
from pathlib import Path
from fastapi import FastAPI, Request

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


def get_skynode_serial_number() -> str | None:
    try:
        return Path("/etc/skynode").read_text().strip().split("-")[-1]
    except FileNotFoundError:
        return None


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
