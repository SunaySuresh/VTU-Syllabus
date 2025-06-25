import cv2
import numpy as np
from deepface import DeepFace

proto_path = "models/deploy.prototxt"
model_path = "models/res10_300x300_ssd_iter_140000.caffemodel"
net = cv2.dnn.readNetFromCaffe(proto_path, model_path)

def detect_face(image):
    """ Detect face using OpenCV DNN and return cropped face. """
    h, w = image.shape[:2]
    blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104, 177, 123), swapRB=False, crop=False)
    net.setInput(blob)
    detections = net.forward()
    
    max_confidence, best_face = 0, None
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > max_confidence:
            max_confidence = confidence
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            best_face = image[startY:endY, startX:endX]
    
    return best_face if best_face is not None else None

def compare_faces(captured_face_path, document_face_path):
    """ Compare captured and document faces using DeepFace (Facenet). """
    try:
        result = DeepFace.verify(img1_path=captured_face_path, img2_path=document_face_path, model_name="Facenet")
        return result["distance"] < 0.4
    except Exception as e:
        print("Face comparison error:", e)
        return False
