from fastapi import FastAPI, Form, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
import os
import shutil
import csv
import uuid
import uvicorn

# 🚫 Disable default Swagger & ReDoc docs
app = FastAPI(docs_url=None, redoc_url=None)

# Static & templates
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
templates = Jinja2Templates(directory="templates")

CSV_FILE = "attendance.csv"
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize CSV if it doesn't exist
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Full Name", "PID", "IP Address", "Image Filename"])

@app.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/submit", response_class=HTMLResponse)
async def submit_form(
    request: Request,
    full_name: str = Form(...),
    pid: str = Form(...),
    photo: UploadFile = File(...)
):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    ip = request.client.host

    # Save image
    ext = os.path.splitext(photo.filename)[-1]
    filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)

    # Log attendance
    with open(CSV_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, full_name.strip(), pid.strip(), ip, filename])

    return templates.TemplateResponse("success.html", {
        "request": request,
        "name": full_name,
        "time": timestamp,
        "image_url": f"/uploads/{filename}"
    })

# 🎣 Rick Roll instead of FastAPI docs
@app.get("/docs", response_class=HTMLResponse)
async def custom_docs(request: Request):
    return templates.TemplateResponse("rickroll.html", {"request": request})

@app.get("/redoc", response_class=HTMLResponse)
async def rickroll_redoc(request: Request):
    return templates.TemplateResponse("rickroll.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)