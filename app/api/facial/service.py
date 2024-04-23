from fastapi import UploadFile
from app.dbchroma import DbChroma
from app.face_detector import FaceDetector
import numpy as np
import cv2
from app.idbVector import IdbVector
from app.face_detector import FaceDetector
from app.model import ListMatched




# def datatable(
#     db: DbChroma,
#     page : int = 0,
#     size : int = 10,
#     ids: list[str] = [],
#     include: list[str] = []
# ):
#     return db.datatable(page, size,ids,include)

def get_doc_embeding(db:IdbVector,document_number:str):
    exists = db.get(document_number)
    if exists is None:
        return {
            "message": "No se encontraron coincidencias", 
            "document_number": None            
        }
    return {
            "message": "Se encontraron coincidencias", 
            "document_number": exists.id,
            "embedding": exists.embedding
    }



def get_image_array(image: UploadFile):
    contents = image.file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img_array = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img_array

def upload_face(db:IdbVector,detector: FaceDetector, image : UploadFile , document_number:str):
    img_array = get_image_array(image)
    embeding = detector.get_image_embedding(img_array)
    db.insert(ids=[document_number],embeddings=[embeding])
    return {"message": "Facial Recognition Upload"}

def detect_face(db:IdbVector, detector:FaceDetector , image : UploadFile):
    image_array = get_image_array(image)
    img_emb = detector.get_image_embedding(image_array)
    querList : ListMatched = db.query(img_emb)
    image_embedding = detector.get_image_embedding(image_array)
    for item in querList.items:
        verify = detector.verify_embeding(image_embedding,item.embedding)
        if verify['verify']:
            return {
                    "message": "Se encontraron coincidencias", 
                    "document_number": item.id,
                    "distance": verify["distance"],
                    }
    return {
            "message": "No se encontraron coincidencias", 
            "document_number": None            
    }

def delete_face(db:IdbVector,document_number:str):
    exists = db.get(document_number)
    if exists is None:
        return {
            "message": "No se encontraron coincidencias", 
            "document_number": None            
        }
    id = exists.id
    db.delete(id)
    return {
            "message": "Se elimino el registro", 
            "document_number": id            
    }
   
def update_face(db:IdbVector,detector:FaceDetector,image : UploadFile, document_number:str):
    image_array = get_image_array(image)
    img_emb = detector.get_image_embedding(image_array)
    db.update(document_number,img_emb)

    