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
        print("distance", distance)
        cls.distance = DISTANCE_MAPPING[distance]
        print("distance", cls.distance)

    @classmethod
    def search_one(cls, vector, meta_conditions, top) -> List[Tuple[int, float]]:
        results = cls.table.query(vector, top, None, cls.distance, True)

        print("results", results)
        return [(int(result[0]), float(result[1])) for result in results]
