import redis
from redis.commands.search.field import TagField, TextField, VectorField, NumericField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query

REDIS_HOST='localhost'
REDIS_PORT=6379
REDIS_PASSWORD=None
REDIS_DB=0

class RedisSearchClient:

    def __init__(self, index_name='products', doc_prefix="doc:", vector_dim=1536):
        self.r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB)
        self.index_name = index_name 
        self.doc_prefix = doc_prefix
        self.vector_dim = vector_dim
        self._create_index()
        self.pipe = self.r.pipeline()
    
    def _create_index(self):
        try:
            self.r.ft(self.index_name).info()
            print("Index already exists")
        except Exception as e:
            print("Creating index")
            schema = (
                TagField("id"),
                TagField("title"),
                TagField("category"),
                NumericField("price"),
                TextField("description"),
                TextField("image"),
                NumericField("rating_rate"),
                NumericField("rating_count"),
                VectorField("vector",
                    "FLAT", {
                        "TYPE": "FLOAT32",
                        "DIM": self.vector_dim,
                        "DISTANCE_METRIC": "COSINE",
                    }
                ),
            )
            definition = IndexDefinition(prefix=[self.doc_prefix], index_type=IndexType.HASH)
            self.r.ft(self.index_name).create_index(fields=schema, definition=definition)
        
    def delete_index(self):
        self.r.ft(self.index_name).dropindex(delete_documents=True)

    def count_documents(self):
        return int(self.r.ft(self.index_name).info()['num_docs'])

    def schema_document(self, id, doc): # doc debe estar en formato dict {}
        self.pipe.hset(f'{self.doc_prefix}{id}', mapping=doc) # key: value
    
    def add_document(self, id, doc):
        self.schema_document(id, doc)
        self.pipe.execute()

    def add_bulk_documents(self, docs): # docs: list [{},{},{}]
        [self.schema_document(doc['id'], doc) for doc in docs] 
        self.pipe.execute() # execute all commands in the pipeline

    def search_similar_documents(self, vector, topK=5, id=None):
        filter_query = '(@id:{'+'file_'+str(id)+'})' if id else '*'    
        query = (
            Query(f"{filter_query}=>[KNN {topK} @vector $vec as score]")
            .sort_by("score")
            .paging(0, topK)
            .return_fields("id", "title", "price", "description", "category", "image", "rating_rate", "rating_count", "score")   
            .dialect(2)
        )
        query_params = {"vec": vector}
        return self.r.ft(self.index_name).search(query, query_params).docs
    