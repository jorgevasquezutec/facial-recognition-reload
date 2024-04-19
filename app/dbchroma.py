import chromadb
from chromadb.config import Settings
from app.dependency import detector
from chromadb import Documents, EmbeddingFunction, Embeddings
from app.config.constants import n_results

class DeepFaceEmbedding(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        embeddings = []
        for doc in input:
            embeddings.append(detector.get_image_embedding(doc))
        return embeddings


class DbChroma:
    def __init__(self, path,name_collection):
        self.path = path
        self.name_collection = name_collection
        self.client = chromadb.PersistentClient(path=self.path,settings=Settings(allow_reset=True))
        self.collection = self.client.get_or_create_collection(self.name_collection,
        embedding_function=DeepFaceEmbedding(), metadata={"hnsw:space": "cosine"})

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
            n_results=n_results,
        )
    
    def queryImage(self,image):
        return self.collection.query(
            query_images=[image],
            n_results=n_results,
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