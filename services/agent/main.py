import asyncio
from contextlib import asynccontextmanager
from logging import getLogger
from typing import Annotated

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from gateway import DronetagGateway
from settings import Settings

logger = getLogger("uvicorn.error")

templates = Jinja2Templates(directory="templates")
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
    params = {
        "title": "Dronetag Agent",
        "uas_id": app_settings.uas_id,
        "skynode": app_settings.skynode_id,
    }
    if app_settings.oprn:
        params["oprn"] = app_settings.oprn.public_part
    return templates.TemplateResponse(request, "index.html", params)


@app.get("/settings", response_model=Settings)
def read_settings():
    return app_settings


@app.post("/oprn", response_class=HTMLResponse)
async def post_oprn(request: Request, oprn: Annotated[str, Form()]):
    try:
        app_settings.oprn = oprn
        app_settings.save()
    except ValueError:
        params = {"oprn": oprn, "oprn_error": "This number is not valid."}
        # We cannot return a 422 status code here, because HTMX (or Bootstrap) will reject it.
    else:
        params = {"oprn": app_settings.oprn.public_part, "oprn_success": "OPRN successfully uploaded."}
    return templates.TemplateResponse(request, "blocks/oprn-form.html", params)


@app.delete("/oprn", response_class=HTMLResponse)
async def delete_oprn(request: Request):
    app_settings.oprn = None
    app_settings.save()
    return templates.TemplateResponse(request, "blocks/oprn-form.html", {"message": "OPRN successfully reset."})
