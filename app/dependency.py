
from app.config.constants import ModelType, DistanceMetricType, NormalizationType, BackendType
from app.face_detector import FaceDetector
from app.config.constants import CHROMA_PATH, CHROMA_COLLECTION, CHROMA_N_RESULTS, CHROMA_METADATA
from app.dbchroma import DbChroma

model = ModelType.Facenet.value
distance_metric = DistanceMetricType.cosine.value
backend = BackendType.retinaface.value
normalization = NormalizationType.ArcFace.value

class DetectorInstance:
    instance = None
    def __new__(cls) -> FaceDetector:
        if cls.instance is None:
            cls.instance = FaceDetector(model, distance_metric, backend, normalization)
        return cls.instance
    
class ChromaInstance:
    instance = None
    def __new__(cls)-> DbChroma:
        if cls.instance is None:
            cls.instance = DbChroma(path=CHROMA_PATH,name_collection=CHROMA_COLLECTION,detector=DetectorInstance())
        return cls.instance


db : DbChroma  = ChromaInstance()
detector : FaceDetector = DetectorInstance()

async def get_db():
    return db

async def get_face_detector():
    return detector