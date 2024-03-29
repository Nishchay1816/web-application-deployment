from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Use Jinja2Templates to render HTML templates
templates = Jinja2Templates(directory="templates")

# Define a model for a note
class Note(BaseModel):
    content: str

# In-memory database to store notes
notes_db: List[Note] = []

# Route to serve the home page
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "notes": notes_db})

# Route to create a new note
@app.post("/notes/", response_class=HTMLResponse)
async def create_note(request: Request, content: str = Form(...)):
    note = Note(content=content)
    notes_db.append(note)
    return templates.TemplateResponse("index.html", {"request": request, "notes": notes_db})

# Route to reset the list of notes
@app.post("/reset/", response_class=HTMLResponse)
async def reset_notes(request: Request):
    notes_db.clear()
    return templates.TemplateResponse("index.html", {"request": request, "notes": notes_db})

# Error handling for route not found
@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("404.html", {"request": request})

# Error handling for general server errors
@app.exception_handler(Exception)
async def server_error_exception_handler(request: Request, exc: Exception):
    return templates.TemplateResponse("500.html", {"request": request})
