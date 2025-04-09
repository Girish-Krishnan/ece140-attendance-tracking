from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
import csv
import os
import uvicorn

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

# Setup static and template directories
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

CSV_FILE = "attendance.csv"

# Initialize CSV file if not already created
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Full Name", "PID", "IP Address"])

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/submit", response_class=HTMLResponse)
async def submit_form(request: Request, full_name: str = Form(...), pid: str = Form(...)):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    client_host = request.client.host

    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, full_name.strip(), pid.strip(), client_host])

    return templates.TemplateResponse("success.html", {
        "request": request,
        "name": full_name,
        "time": timestamp
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)