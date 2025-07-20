from fastapi import FastAPI, Request, Body
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from model.chart_project import ChatRequest


app = FastAPI()
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
    })



# @app.get("/projects/carbonix", response_class=HTMLResponse)
# async def read_home(request: Request):
#     return templates.TemplateResponse("project_carbonix.html", {
#         "request": request,
#     })

# @app.get("/projects/lift", response_class=HTMLResponse)
# async def read_home(request: Request):
#     return templates.TemplateResponse("project_lift.html", {
#         "request": request,
#     })


@app.get("/projects/{project_slug}", response_class=HTMLResponse)
async def read_projects(request: Request, project_slug: str):
    payload = {
        "request": request,
    }
    if project_slug == 'lift':
        payload['yt_link'] = "https://www.youtube.com/embed/-WlWMp6UCQY?si=CcaBHcnieLbG4GAV"
        payload['slide_path'] = "/static/project/lift/MADT7204_Lift.pdf"
        payload['chat_id'] = '748f7d75-434f-4108-8453-cf1dac178f99'

    if project_slug == 'carbonix':
        payload['yt_link'] = "https://www.youtube.com/embed/UgJ3B7ADTQQ?si=Pzog1MykCi6eiUMR"
        payload['slide_path'] = "/static/project/carbonix/Carbon Xchange Pitch Deck Presentation.pdf"
        payload['chat_id'] = '748f7d75-434f-4108-8453-cf1dac178f99'

    return templates.TemplateResponse("project_templates.html", payload)