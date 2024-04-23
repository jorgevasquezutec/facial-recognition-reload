import chromadb
# from chromadb.config import Settings
from chromadb import Documents, EmbeddingFunction, Embeddings
from app.config.constants import CHROMA_N_RESULTS,CHROMA_METADATA
from app.face_detector import FaceDetector
from chromadb.api.models.Collection import Collection
from app.config.settings import api_settings
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
        self.client = chromadb.HttpClient(host=api_settings.CHROMA_HOST,port=api_settings.CHROMA_PORT)
        # self.client = chromadb.PersistentClient(path=self.path,settings=Settings(allow_reset=True))
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
    
    def queryEmbedding(self,embedding,n_result = CHROMA_N_RESULTS):
        return self.collection.query(
            query_embeddings=embedding,
            n_results=n_result,
        )
    
    def queryImage(self,image,n_result = CHROMA_N_RESULTS):
        return self.collection.query(
            query_images=[image],
            n_results=n_result,
            include=['embeddings','distances']
        )
    
    def getById(self,id):
        return self.collection.get(
            ids=[id],
            include=['embeddings']
        )
    def upsertByIds(self,ids,embeddings):
        self.collection.upsert(
            ids=ids,
            embeddings=embeddings
        )
    def upsertByImage(self,images,ids):
        self.collection.upsert(
            images=images,
            ids=ids
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