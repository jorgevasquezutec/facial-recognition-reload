
from app.config.constants import ModelType, DistanceMetricType, BackendType
from app.face_detector import FaceDetector

model = ModelType.GhostFaceNet.value
distance_metric = DistanceMetricType.cosine.value
backend = BackendType.fastmtcnn.value
detector = FaceDetector(model, distance_metric, backend)
