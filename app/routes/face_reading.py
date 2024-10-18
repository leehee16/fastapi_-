from fastapi import APIRouter, Request, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, StreamingResponse
import cv2
import numpy as np
import base64
from ..utils.camera import camera

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def generate_frames():
    while True:
        frame = camera.get_frame()
        if frame is None:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@router.get("/face-reading")
async def face_reading(request: Request):
    return templates.TemplateResponse("face_reading.html", {"request": request})

@router.get("/video-feed")
async def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@router.post("/analyze-face")
async def analyze_face(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    analyzed_img, analysis = camera.analyze_face(img)

    _, buffer = cv2.imencode('.jpg', analyzed_img)
    img_base64 = base64.b64encode(buffer).decode('utf-8')

    return JSONResponse(content={"analysis": analysis, "image": img_base64})

@router.post("/start-camera")
async def start_camera():
    if camera.start():
        return JSONResponse(content={"message": "Camera started"})
    return JSONResponse(content={"error": "Failed to start camera"})

@router.post("/stop-camera")
async def stop_camera():
    camera.stop()
    return JSONResponse(content={"message": "Camera stopped"})
