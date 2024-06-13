from fastapi.middleware.cors import CORSMiddleware
from routers.main import router as main_router
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from core.settings import settings
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "PUT", "POST", "PATCH", "DELETE"],
    allow_credentials=True,
    allow_headers=["*"],
)

app.include_router(main_router)


@app.get("/ping")
async def health():
    return "pong"


if not settings.DEV_MODE:
    templates = Jinja2Templates(directory="templates/spa/")

    app.mount("/assets", StaticFiles(directory="templates/spa/assets"), name="static")

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    async def main(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
