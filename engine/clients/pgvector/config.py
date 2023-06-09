from engine.base_client.distances import Distance

DISTANCE_MAPPING = {
      Distance.L2: "l2_distance",
      Distance.COSINE: "cosine_distance",
      Distance.DOT: "max_inner_product",
    }

PG_CONNECTION_STRING="postgresql://postgres:postgres@localhost:54322/postgres"