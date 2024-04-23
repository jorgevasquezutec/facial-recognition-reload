from enum import Enum

class ModelType(Enum):
    VGG_Face = "VGG-Face"
    Facenet = "Facenet"
    Facenet512 = "Facenet512"
    OpenFace = "OpenFace"
    # DeepFace = "DeepFace"
    DeepID = "DeepID"
    ArcFace = "ArcFace"
    Dlib = "Dlib"
    SFace = "SFace"
    GhostFaceNet = "GhostFaceNet"


class BackendType(Enum):
    opencv = "opencv"
    ssd = "ssd"
    dlib = "dlib"
    mtcnn = "mtcnn"
    fastmtcnn = "fastmtcnn"
    retinaface = "retinaface"
    mediapipe = "mediapipe"
    yolov8 = "yolov8"
    yunet = "yunet"
    centerface = "centerface"
    
class NormalizationType(Enum):
    base = "base"
    raw = "raw"
    Facenet = "Facenet"
    Facenet2018 = "Facenet2018"
    VGGFace = "VGGFace"
    VGGFace2 = "VGGFace2"
    ArcFace = "ArcFace"

class DistanceMetricType(Enum):
    cosine = "cosine"
    euclidean = "euclidean"
    euclidean_l2 = "euclidean_l2"

CHROMA_PATH = './db'
COLLECTION = 'faces'
N_RESULTS = 3
CHROMA_METADATA={"hnsw:space": "cosine"}

AUTH_PREFIX = '/auth'
FACIAL_PREFIX = '/facial'
MAX_FILE_SIZE = 2097152 # 2MB
ALOWED_FILE_TYPES = ["image/png", "image/jpeg", "image/jpg", "png", "jpeg", "jpg"]