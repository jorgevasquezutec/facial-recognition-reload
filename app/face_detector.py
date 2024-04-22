from deepface import DeepFace
from app.exeptions import *

class FaceDetector:
    def __init__(self, 
                 model, 
                 distance_metric,
                 backend
                 ):
        self.model = model
        self.distance_metric = distance_metric
        self.backend = backend

    
    def get_image_embedding(self, image_path):
        try:
            image_embeding_obj= DeepFace.represent(image_path, model_name=self.model , detector_backend=self.backend,enforce_detection=False)
            count_image = len(image_embeding_obj)
            if count_image > 1:
                raise ManyFacesFound(f'Many faces found in the image: {image_path}')
            elif count_image == 0:
                raise FaceNotFound(f'Face not found in the image: {image_path}')
            image_embedding = image_embeding_obj[0]["embedding"]
            return image_embedding
        except ManyFacesFound as e:
            raise e
        except FaceNotFound as e:
            raise e
        except Exception as e:
            print(e)
            raise FaceNotFound(f'Face not found in the image: {image_path}')
    
    def verify_embeding(self, image1_embedding, image2_embedding):
        distance = DeepFace.verification.find_distance(image1_embedding, image2_embedding, self.distance_metric)
        threshold = DeepFace.verification.find_threshold(self.model, self.distance_metric)
        respObj = {
        "verify": distance <= threshold,
        "distance": distance,
        "threshold": threshold
        }   
        return respObj

