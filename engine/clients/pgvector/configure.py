import vecs

from benchmark.dataset import Dataset
from engine.base_client.configure import BaseConfigurator
from engine.clients.pgvector.config import PG_CONNECTION_STRING


class PGVectorConfigurator(BaseConfigurator):
    def __init__(self, host, collection_params: dict, connection_params: dict):
        super().__init__(host, collection_params, connection_params)

        self.client = vecs.create_client(PG_CONNECTION_STRING)

    def clean(self):
        try: 
          table = self.client.get_collection("docs")
          table._drop()
          print("collection dropped")
        except:
          print("collection not found")

    def recreate(self, dataset: Dataset, collection_params):
        self.clean()
        print("creating collection: ")
        print("dataset", dataset.config)
        if not hasattr(dataset, "dimension"):
          if not hasattr(dataset.config, "vector_size"):
              dataset.dimension = 100
          else:
              dataset.dimension = dataset.config.vector_size
        self.table = self.client.create_collection("docs", dataset.dimension)

if __name__ == "__main__":
    pass
