import asyncio
from contextlib import asynccontextmanager
from logging import getLogger
from typing import Annotated

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2_fragments.fastapi import Jinja2Blocks

from gateway import DronetagGateway
from settings import Settings

logger = getLogger("uvicorn.error")

templates = Jinja2Blocks(directory="templates")
static_files = StaticFiles(directory="static")

app_settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app_settings.save()

    try:
        gateway = DronetagGateway(app_settings)
    except ConnectionError as e:
        logger.error(f"Failed to start gateway: {e}")
        gateway_task = None
    else:
        gateway_task = asyncio.create_task(gateway.run())

    yield

    if gateway_task:
        gateway_task.cancel()


app = FastAPI(lifespan=lifespan)
app.mount("/static", static_files, name="static")


@app.get("/", response_class=HTMLResponse)
def get_index(request: Request):
    context = {
        "request": request,
        "title": "Dronetag Agent",
        "uas_id": app_settings.uas_id,
        "skynode": app_settings.skynode_id,
    }
    if app_settings.oprn:
        context["oprn"] = app_settings.oprn.public_part
    # TODO(sponsfreixes/jinja2-fragments#39): refactor context
    return templates.TemplateResponse("index.html", context)


@app.get("/settings", response_model=Settings)
def read_settings():
    return app_settings


@app.post("/oprn", response_class=HTMLResponse)
async def post_oprn(request: Request, oprn: Annotated[str, Form()]):
    context = {"request": request}
    try:
        app_settings.oprn = oprn
        app_settings.save()
    except ValueError:
        context |= {"oprn": oprn, "oprn_error": "This number is not valid."}
        # We cannot return a 422 status code here, because HTMX (or Bootstrap) will reject it.
    else:
        context |= {"oprn": app_settings.oprn.public_part, "oprn_success": "OPRN successfully uploaded."}
    # TODO(sponsfreixes/jinja2-fragments#39): refactor context
    return templates.TemplateResponse("index.html", context, block_name="oprn_form")


@app.delete("/oprn", response_class=HTMLResponse)
async def delete_oprn(request: Request):
    app_settings.oprn = None
    app_settings.save()
    context = {"request": request, "message": "OPRN successfully reset."}
    # TODO(sponsfreixes/jinja2-fragments#39): refactor context
    return templates.TemplateResponse("index.html", context, block_name="oprn_form")


@app.get("/api/status")
def dummy_api():
    """Hotfix for #13"""
    return {"status": "ok"}
