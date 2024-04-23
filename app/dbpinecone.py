from app.idbVector import IdbVector
from app.config.settings import api_settings
from pinecone import Pinecone
from app.config.constants import COLLECTION,N_RESULTS
from app.model import VectorMatched,ListMatched


class PineConeInstace():
    instance = None
    def __new__(cls)-> Pinecone:
        if cls.instance is None:
            cls.instance = Pinecone(api_key=api_settings.PINECONE_API_KEY)
        return cls.instance


class DbPinecone(IdbVector):
    db = PineConeInstace()
    index = db.Index(name=COLLECTION)
    
    def insert(self, ids, embeddings)->None:
        vectors = []
        for i, id in enumerate(ids):
            vectors.append({"id": id, "values": embeddings[i]})
        self.index.upsert(vectors=vectors)
        
            
    def query(self, embeding, n_result=N_RESULTS)->ListMatched:
        result = self.index.query(vector=embeding, top_k=n_result,include_values=True)
        matches =  result.get('matches', [])
        data = [VectorMatched(id=match['id'], embedding=match['values']) for match in matches]
        return ListMatched(items=data)
          
    def get(self, id)->VectorMatched:
        result = self.index.fetch(ids=[id])
        vectors = result.get('vectors', {})
        if len(vectors) == 0:
            return None
        vector = vectors.get(id, {})
        ##if not empty
        if vector:
            return VectorMatched(id=id, embedding=vector.get('values', []) )
        else:
            return None
    
    def update(self, id, embedding)->None:
        self.index.update(id=id, values=embedding)
    
    def delete(self, id)->None:
        return self.index.delete(ids=[id])
    
    # def get_all(self, page, size, ids, include):
    #     return self.index.list_paginated(
    #         limit=size,
    #     )