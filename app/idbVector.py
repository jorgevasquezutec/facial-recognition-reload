
from abc import ABC, abstractmethod
from app.model  import VectorMatched,ListMatched

class IdbVector(ABC):
    @abstractmethod
    def insert(self, images, ids)->None:
        pass
    @abstractmethod
    def query(self, query, n_result)->ListMatched:
        pass
    @abstractmethod
    def get(self, id)->VectorMatched:
        pass
    
    @abstractmethod
    def update(self, id, embedding)->None:
        pass
    
    @abstractmethod
    def delete(self, id)->None:
        pass
    
    @abstractmethod
    def datatable(self, page, size, ids, include):
        pass
    # @abstractmethod
    # def get_all(self, page, size, ids, include):
    #     pass
        