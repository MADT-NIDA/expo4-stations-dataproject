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
    chat_id = '68282fbb-afad-437d-88ed-2c1476bb457b'
    if project_slug == 'lift':
        payload['yt_link'] = "https://www.youtube.com/embed/-WlWMp6UCQY?si=CcaBHcnieLbG4GAV"
        payload['slide_path'] = "/static/project/lift/MADT7204_Lift.pdf"
        payload['chat_id'] = '41677df2-3871-4e65-bc7d-935f12dc121a'

    if project_slug == 'carbonix':
        payload['yt_link'] = "https://www.youtube.com/embed/UgJ3B7ADTQQ?si=Pzog1MykCi6eiUMR"
        payload['slide_path'] = "/static/project/carbonix/Carbon Xchange Pitch Deck Presentation.pdf"
        payload['chat_id'] = '324dde45-e851-47c1-b9f1-3ef5f9f77ab0'

    if project_slug == 'finsure':
        payload['yt_link'] = "https://www.youtube.com/embed/PSU_pTzm08g?si=K60ZM_6gTYdOa6k8"
        payload['slide_path'] = "/static/project/carbonix/Carbon Xchange Pitch Deck Presentation.pdf"
        payload['chat_id'] = chat_id

    if project_slug == 'freshx':
        payload['yt_link'] = "https://www.youtube.com/embed/WeMnV-XJOQ8?si=jwxEgPWCG69kTA3V"
        payload['slide_path'] = "/static/project/carbonix/Carbon Xchange Pitch Deck Presentation.pdf"
        payload['chat_id'] = 'eabe90ce-b681-4bf7-a3da-0758d4515ed6'

    if project_slug == 'greenbridge':
        payload['yt_link'] = "https://www.youtube.com/embed/Kl6C-xaRCqo?si=LIBeQPDxvY_yfDOg"
        payload['slide_path'] = "/static/project/carbonix/Carbon Xchange Pitch Deck Presentation.pdf"
        payload['chat_id'] = chat_id

