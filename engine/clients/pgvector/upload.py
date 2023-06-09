from typing import List, Optional

import numpy as np
import vecs

from engine.base_client.upload import BaseUploader
from engine.clients.pgvector.config import PG_CONNECTION_STRING
from engine.clients.pgvector.config import DISTANCE_MAPPING


class PGVectorUploader(BaseUploader):
    client = None
    table = None
    upload_params = {}

    @classmethod
    def init_client(cls, host, distance, connection_params, upload_params):
        cls.client = vecs.create_client(PG_CONNECTION_STRING)
        cls.table = cls.client.get_collection("docs")
        cls.upload_params = upload_params

    @classmethod
    def upload_batch(
        cls, ids: List[int], vectors: List[list], metadata: Optional[List[dict]]
    ):
      vector_rows = []
      for i in range(len(ids)):
        vector_rows.append({
          'id': str(ids[i]),
          'vec': vectors[i],
          'metadata': metadata[i] if metadata else None
        })
      cls.table.upsert(vector_rows)

    @classmethod
    def post_upload(cls, distance):
        cls.table.create_index(measure=DISTANCE_MAPPING[distance])
        return {}
