from fastapi import APIRouter, Request, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
import cv2
import numpy as np
import base64
from ..utils.camera import camera

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/face-reading")
async def face_reading(request: Request):
    return templates.TemplateResponse("face_reading.html", {"request": request})

@router.post("/start-camera")
async def start_camera():
    if camera.start():
        return JSONResponse(content={"message": "Camera started"})
    return JSONResponse(content={"error": "Failed to start camera"})

@router.post("/stop-camera")
async def stop_camera():
    camera.stop()
    return JSONResponse(content={"message": "Camera stopped"})

@router.post("/recognize-face")
async def recognize_face(data: dict):
    image_data = data['image'].split(',')[1]
    image_bytes = base64.b64decode(image_data)
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    faces_detected = camera.detect_faces(img)
    return JSONResponse(content={"faces_detected": faces_detected})

@router.post("/analyze-face")
async def analyze_face(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    analyzed_img, analysis = camera.analyze_face(img)

    _, buffer = cv2.imencode('.jpg', analyzed_img)
    img_base64 = base64.b64encode(buffer).decode('utf-8')

    return JSONResponse(content={"analysis": analysis, "image": img_base64})
