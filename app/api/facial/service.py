from fastapi import UploadFile
from app.dbchroma import DbChroma
from app.face_detector import FaceDetector
import numpy as np
import cv2




def datatable(
    db: DbChroma,
    page : int = 0,
    size : int = 10,
    ids: list[str] = [],
    include: list[str] = []
):
    return db.datatable(page, size,ids,include)


def get_image_array(image: UploadFile):
    contents = image.file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img_array = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img_array

def upload_face(db:DbChroma, image : UploadFile , document_number:str):
    img_array = get_image_array(image)
    db.insertByImage(images=[img_array],ids=[document_number])
    return {"message": "Facial Recognition Upload"}

def detect_face(db:DbChroma, detector:FaceDetector , image : UploadFile):
    image_array = get_image_array(image)
    found_faces = db.queryImage(image_array)
    image_embedding = detector.get_image_embedding(image_array)
    ids = found_faces['ids'][0]
    embeddings = found_faces['embeddings'][0]
    for i in range(len(ids)):
        verify = detector.verify_embeding(image_embedding,embeddings[i])
        if verify['verify']:
            return {
                    "message": "Se encontraron coincidencias", 
                    "document_number": ids[i]
                    }
       
    return {
            "message": "No se encontraron coincidencias", 
            "document_number": None            
    }

def delete_face(db:DbChroma,document_number:str):
    exists= db.getById(document_number)
    ids = exists['ids']
    if(len(ids)== 0):
        return {
            "message": "No se encontraron coincidencias", 
            "document_number": None            
        }
    id = ids[0]
    db.deleteById(id)
    return {
            "message": "Se elimino el registro", 
            "document_number": id            
    }
   
def update_face(db:DbChroma,image : UploadFile, document_number:str):
    image_array = get_image_array(image)
    db.upsertByImage(images=[image_array],ids=[document_number])

    