# Lecture Attendance Tracking WebApp

This repository contains a small FastAPI application that records lecture attendance. Students enter their name and PID, take a webcam photo, and the data is logged locally.

## Features
- Web form for entering a full name and PID.
- Captures a selfie using the browser's webcam API.
- Stores images under `uploads/` and logs entries in `attendance.csv`.
- Simple, single page interface styled with CSS.
- Replaces the default FastAPI docs with a playful Rick Astley video at `/docs` and `/redoc`.

## Requirements
- Python 3.8 or higher
- `pip` to install dependencies

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/ece140-attendance-tracking.git
   cd ece140-attendance-tracking
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the app
Start the server with:
```bash
python main.py
```
The application will run on `http://localhost:8000`.

## Usage
1. Open `http://localhost:8000` in your browser.
2. Enter your full name and PID (`A` followed by 8 digits).
3. Allow access to your camera, take a picture, and submit the form.
4. A success page confirms your check‑in and shows the captured image.

Each submission adds a line to `attendance.csv` with the timestamp, name, PID, IP address, and image filename. Photos are saved in the `uploads/` folder. These files are excluded from version control via `.gitignore`.

### Directory structure
```
main.py             # FastAPI application
requirements.txt    # Python dependencies
static/style.css    # Page styling
templates/          # HTML templates
uploads/            # Generated folder for photos
attendance.csv      # Generated log file
```

## Notes
- The application disables FastAPI's automatic documentation. Visiting `/docs` or `/redoc` serves the `rickroll.html` template.
- Restart the server after modifying templates or static files to see updates.

This simple project demonstrates handling form data and file uploads with FastAPI. Feel free to adapt it for your own attendance tracking needs.
