import chromadb
# from chromadb.config import Settings
from chromadb import Documents, EmbeddingFunction, Embeddings
from app.config.constants import N_RESULTS,CHROMA_METADATA
from app.face_detector import FaceDetector
from chromadb.api.models.Collection import Collection
from app.config.settings import api_settings
from app.idbVector import IdbVector
from app.model import VectorMatched,ListMatched
class DeepFaceEmbedding(EmbeddingFunction):
    
    def __init__(self,detector : FaceDetector):
        self.detector = detector
    def __call__(self, input: Documents) -> Embeddings:
        embeddings = []
        for doc in input:
            embeddings.append(self.detector.get_image_embedding(doc))
        return embeddings


class DbChroma(IdbVector):
    def __init__(self, 
                 path : str,
                 name_collection : str,
                 detector : FaceDetector
                 ):
        self.path = path
        self.name_collection = name_collection
        self.detector = detector
        self.client = chromadb.HttpClient(host=api_settings.HOST_CHROMA,port=api_settings.PORT_CHROMA)
        # self.client = chromadb.PersistentClient(path=self.path,settings=Settings(allow_reset=True))
        self.collection : Collection = self.client.get_or_create_collection(self.name_collection,
        embedding_function=DeepFaceEmbedding(self.detector), metadata=CHROMA_METADATA)


    def insert(self, ids, embeddings):
        self.collection.add(
            embeddings=embeddings,
            ids=ids
        )
    
    def query(self, embedding, n_result = N_RESULTS):
        result = self.collection.query(
            query_embeddings=[embedding],
            n_results=n_result,
            include=['embeddings']
        )
        ids = result['ids'][0]
        if(len(ids) == 0):
            return ListMatched(items=[])
        embeddings = result['embeddings'][0]
        items = [VectorMatched(id=ids[i], embedding=embeddings[i]) for i in range(len(ids))]
        return ListMatched(items=items)
    
            
    def get(self, id):
        exists = self.collection.get(
            ids=[id],
            include=['embeddings']
        )
        ids = exists['ids']
        if(len(ids) == 0):
            return None
        embeddings = exists['embeddings'][0]
        return VectorMatched(id=ids[0], embedding=embeddings)
        
        
    def update(self, id, embedding):
        self.collection.upsert(
            ids=[id],
            embeddings=[embedding]
        )
        
    def delete(self, id):
        self.collection.delete(
            ids=[id]
        )
    
    def insert_by_images(self, ids, images):
        self.collection.add(
            images=images,
            ids=ids
        )



    # def insertByImage(self,images, ids):
    #     self.collection.add(
    #         images=images,
    #         ids=ids
    #     )

    # def insertByEmbedding(self,embeddings, ids):
    #     self.collection.add(
    #         embeddings=embeddings,
    #         ids=ids
    #     )
    
    # def queryEmbedding(self,embedding,n_result = N_RESULTS):
    #     return self.collection.query(
    #         query_embeddings=embedding,
    #         n_results=n_result,
    #     )
    
    # def queryImage(self,image,n_result = N_RESULTS):
    #     return self.collection.query(
    #         query_images=[image],
    #         n_results=n_result,
    #         include=['embeddings','distances']
    #     )
    
    # def getById(self,id):
    #     return self.collection.get(
    #         ids=[id],
    #         include=['embeddings']
    #     )
    # def upsertByIds(self,ids,embeddings):
    #     self.collection.upsert(
    #         ids=ids,
    #         embeddings=embeddings
    #     )
    # def upsertByImage(self,images,ids):
    #     self.collection.upsert(
    #         images=images,
    #         ids=ids
    #     )
    
    # def deleteById(self,id):
    #     self.collection.delete(
    #         ids=[id]
    #     )
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

    # def getCollection(self):
    #     return self.collection