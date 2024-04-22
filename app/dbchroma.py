import chromadb
from chromadb.config import Settings
from chromadb import Documents, EmbeddingFunction, Embeddings
from app.config.constants import CHROMA_N_RESULTS,CHROMA_METADATA
from app.face_detector import FaceDetector
from chromadb.api.models.Collection import Collection
class DeepFaceEmbedding(EmbeddingFunction):
    
    def __init__(self,detector : FaceDetector):
        self.detector = detector
    def __call__(self, input: Documents) -> Embeddings:
        embeddings = []
        for doc in input:
            embeddings.append(self.detector.get_image_embedding(doc))
        return embeddings


class DbChroma:
    def __init__(self, 
                 path : str,
                 name_collection : str,
                 detector : FaceDetector
                 ):
        self.path = path
        self.name_collection = name_collection
        self.detector = detector
        self.client = chromadb.PersistentClient(path=self.path,settings=Settings(allow_reset=True))
        self.collection : Collection = self.client.get_or_create_collection(self.name_collection,
        embedding_function=DeepFaceEmbedding(self.detector), metadata=CHROMA_METADATA)

    def insertByImage(self,images, ids):
        self.collection.add(
            images=images,
            ids=ids
        )

    def insertByEmbedding(self,embeddings, ids):
        self.collection.add(
            embeddings=embeddings,
            ids=ids
        )
    
    def queryEmbedding(self,embedding):
        return self.collection.query(
            query_embeddings=embedding,
            n_results=CHROMA_N_RESULTS,
        )
    
    def queryImage(self,image):
        return self.collection.query(
            query_images=[image],
            n_results=CHROMA_N_RESULTS,
            include=['embeddings','distances']
        )
    
    def getById(self,id):
        return self.collection.get(
            ids=[id],
            include=['embeddings']
        )
    def upsertById(self,id,embedding):
        self.collection.upsert(
            ids=[id],
            embeddings=[embedding]
        )
    def upsertByImage(self,image,embedding):
        self.collection.upsert(
            images=[image],
            embeddings=[embedding]
        )
    
    def deleteById(self,id):
        self.collection.delete(
            ids=[id]
        )
    def count(self):
        return self.collection.count()
    

    def datatable(self, page=0, size=10 , ids: list[str] = [] , include: list[str] = []):
        data = self.collection.get(
            limit=size,
            offset=(page*size),
            ids=ids,
            include=include
        )
        total = self.collection.count()

        return {
            "items": data,
            "total": total,
            "page": page,
            "pages": (total+size-1)//size,
            "size": size
        }

    def getCollection(self):
        return self.collection