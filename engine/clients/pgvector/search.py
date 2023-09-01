from typing import List, Tuple

import numpy as np
import vecs

from engine.base_client.search import BaseSearcher
from engine.clients.pgvector.config import DISTANCE_MAPPING, PG_CONNECTION_STRING


class PGVectorSearcher(BaseSearcher):
    search_params = {}
    client = None
    table = None
    distance = None

    @classmethod
    def init_client(cls, host, distance, connection_params: dict, search_params: dict):
        cls.client = vecs.create_client(PG_CONNECTION_STRING)
        cls.table = cls.client.get_collection("docs")
        cls.search_params = search_params
        cls.distance = DISTANCE_MAPPING[distance]

    @classmethod
    def search_one(cls, vector, meta_conditions, top) -> List[Tuple[int, float]]:
        results = cls.table.query(vector, top, None, cls.distance, True)

        # print("results", results)
        # product1 = np.linalg.norm(vector)
        return [(int(result[0]), float(result[1])) for result in results]
      
    @classmethod
    def search_one_another(cls, vector, meta_conditions, top) -> List[Tuple[int, float]]:
        results = cls.table.query(vector, top, None, "cosine_distance", True)

        # print("results", results)
        # product1 = np.linalg.norm(vector)
        return [(int(result[0]), float(result[1])) for result in results]
