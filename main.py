from fastapi import FastAPI, Request, Body, Response, status, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from model.chart_project import ChatRequest

from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel


DATABASE_URL = "postgresql://madt_expo_usr:asdfasdf@34.143.247.40:5432/madt_expo_db"
engine = create_engine(DATABASE_URL)  # SQLite-specific
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


class StampTable(Base):
    __tablename__ = "StampTable"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String)
    action = Column(String)
    projects = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class StampIn(BaseModel):
    session_id: str
    project: str
class ActionSummary(BaseModel):
    action: str
    projects: str
    session_count: int

    class Config:
        orm_mode = True
class ActionView(Base):
    __tablename__ = "view_unique_action_per_session"
    __table_args__ = {"extend_existing": True}  # เผื่อซ้ำกับ model อื่น

    action = Column(String, primary_key=True)
    projects = Column(String, primary_key=True)
    session_count = Column(Integer)


Base.metadata.create_all(bind=engine)

BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
    })


@app.get("/display", response_class=HTMLResponse)
async def read_display(request: Request):
    return templates.TemplateResponse("display.html", {
        "request": request,
    })



@app.post("/records/scan", status_code=202)
async def create_record_scans(item: StampIn):
    db = SessionLocal()
    try:
        record = StampTable(session_id=item.session_id, projects=item.project, action='scan')
        db.add(record)
        db.commit()
        db.refresh(record)
        return {"message": "Accepted", "id": record.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()




@app.post("/records/views", status_code=202)
async def create_record_view(item: StampIn):
    db = SessionLocal()
    try:
        record = StampTable(session_id=item.session_id, projects=item.project, action='view')
        db.add(record)
        db.commit()
        db.refresh(record)
        return {"message": "Accepted", "id": record.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.post("/records/chat", status_code=202)
async def create_record_chat(item: StampIn):
    db = SessionLocal()
    try:
        record = StampTable(session_id=item.session_id, projects=item.project, action='chat')
        db.add(record)
        db.commit()
        db.refresh(record)
        return {"message": "Accepted", "id": record.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.post("/records/love", status_code=202)
async def create_record_love(item: StampIn):
    db = SessionLocal()
    try:
        record = StampTable(session_id=item.session_id, projects=item.project, action='love')
        db.add(record)
        db.commit()
        db.refresh(record)
        return {"message": "Accepted", "id": record.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

from collections import defaultdict
@app.get("/records/summary")
def get_summary():
    db = SessionLocal()
    try:
        data = db.query(ActionView).all()
        # fixed order of projects
        # fixed order of projects (lower case to match)
        project_order = ['carbonix', 'freshx', 'finsure', 'lift', 'green bridge', 'airsniff']
        actions = ['view', 'chat', 'love']

        # prepare summary dictionary
        # print(data)
        scan = 0 
        summary = defaultdict(lambda: defaultdict(int))
        for row in data:
            action = row.action.lower()
            project = row.projects.strip().lower()

            if action == 'scan':
                scan += 1

            if project and action in actions:
                summary[action][project] += row.session_count
        # build output
        output = {
            # "labels": [p.title() for p in project_order]
        }
        for action in actions:
            output[action] = [summary[action].get(p, 0) for p in project_order]


        output['scan'] = scan
        return output
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/projects/{project_slug}", response_class=HTMLResponse)
async def read_projects(request: Request, project_slug: str):
    payload = {
        "request": request,
    }
    chat_id = '68282fbb-afad-437d-88ed-2c1476bb457b'
    if project_slug == 'lift':
        payload['yt_link'] = "https://www.youtube.com/embed/-WlWMp6UCQY?si=CcaBHcnieLbG4GAV"
        payload['slide_path'] = "/static/project/lift/MADT7204_Lift.pdf"
        payload['chat_id'] = "5b281a85-57b5-4cc8-9102-d86176166264"
        payload['project'] = 'lift'

    if project_slug == 'carbonix':
        payload['yt_link'] = "https://www.youtube.com/embed/UgJ3B7ADTQQ?si=Pzog1MykCi6eiUMR"
        payload['slide_path'] = "/static/project/carbonix/Carbon Xchange Pitch Deck Presentation.pdf"
        payload['chat_id'] = "5b281a85-57b5-4cc8-9102-d86176166264"
        payload['project'] = 'carbonix'

    if project_slug == 'finsure':
        payload['yt_link'] = "https://www.youtube.com/embed/PSU_pTzm08g?si=JdZJL0yPjOucQ5MH"
        payload['slide_path'] = "/static/project/carbonix/Carbon Xchange Pitch Deck Presentation.pdf"
        payload['chat_id'] = "5b281a85-57b5-4cc8-9102-d86176166264"
        payload['project'] = 'finsure'

    if project_slug == 'freshx':
        payload['yt_link'] = "https://www.youtube.com/embed/WeMnV-XJOQ8?si=jwxEgPWCG69kTA3V"
        payload['slide_path'] = "/static/project/carbonix/Carbon Xchange Pitch Deck Presentation.pdf"
        payload['chat_id'] = "5b281a85-57b5-4cc8-9102-d86176166264"
        payload['project'] = 'freshx'

    if project_slug == 'greenbridge':
        payload['yt_link'] = "https://www.youtube.com/embed/Kl6C-xaRCqo?si=LIBeQPDxvY_yfDOg"
        payload['slide_path'] = "/static/project/carbonix/Carbon Xchange Pitch Deck Presentation.pdf"
        payload['chat_id'] = "5b281a85-57b5-4cc8-9102-d86176166264"
        payload['project'] = 'greenbridge'

    if project_slug == 'airsniff':
        payload['yt_link'] = "https://www.youtube.com/embed/ZVnXIAjEXYU?si=j1lIljm_vRT69Ck0"
        payload['slide_path'] = "/static/project/carbonix/Carbon Xchange Pitch Deck Presentation.pdf"
        payload['chat_id'] = "5b281a85-57b5-4cc8-9102-d86176166264"
        payload['project'] = 'airsniff'

    return templates.TemplateResponse("project_templates.html", payload)
