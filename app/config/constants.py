from enum import Enum

class ModelType(Enum):
    VGG_Face = "VGG-Face"
    Facenet = "Facenet"
    Facenet512 = "Facenet512"
    OpenFace = "OpenFace"
    DeepFace = "DeepFace"
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

class DistanceMetricType(Enum):
    cosine = "cosine"
    euclidean = "euclidean"
    euclidean_l2 = "euclidean_l2"


CromadbPath = './db'
collection128 = 'faces128'
collection512 = 'faces512'
n_results = 1

AUTH_PREFIX = '/auth'
FACIAL_PREFIX = '/facial'