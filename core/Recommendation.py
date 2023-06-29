import os, requests, openai, time, numpy as np
from core.RedisClient import RedisSearchClient
openai.api_key='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' 

class CoreRecommendation:

    def __init__(self, api_url) -> None:
        self.api_url = api_url
        self.products = self.get_products()
        self.r_client = RedisSearchClient()

    def has_embbeddings(self):
        if os.path.exists('status.txt'):
            return True
        return False

    def get_products(self):
        try:
            response = requests.get(self.api_url)
            return response.json()
        except Exception as e:
            print(e)
            return None

    def get_text_for_product(self, product):
        """ 
        product fields: id, title, price, description, category, image, rating_rate, rating_count
        """
        text = ""
        text += f"title: {product['title']}\n"
        text += f"price: {product['price']}\n"
        text += f"description: {product['description']}\n"
        text += f"category: {product['category']}"
        text += f"rating rate: {product['rating']['rate']}"
        text += f"rating count: {product['rating']['count']}"
        return text
    
    def embedding_openai(self, text):
        try:
            time.sleep(0.5)
            response = openai.Embedding.create(
                input=text,
                model="text-embedding-ada-002"
            )
            embedding = response['data'][0]['embedding']
            array_embedding = np.array(embedding, dtype=np.float32)
            return array_embedding.tobytes()
        except Exception as e:
            print(e)
            return None
    
    def extension_products_vector(self):
        if self.products and len(self.products) != 0:
            print(f'Total products: {len(self.products)}')
            counter = 0
            for product in self.products:
                counter += 1
                print(f'product {counter} of {len(self.products)}')
                text = self.get_text_for_product(product)
                product['vector'] = self.embedding_openai(text)
            print('Complete embeddings!')
            return True
        print('Extension products vector EMPTY!')
        return False
    
    def format_redis_save(self, product):
        return {
            'id': product['id'],
            'title': product['title'],
            'price': product['price'],
            'description': product['description'],
            'category': product['category'],
            'image': product['image'],
            'rating_rate': product['rating']['rate'],
            'rating_count': product['rating']['count'],
            'vector': product['vector']
        }
        
    def save_redis_vectors(self):
        self.extension_products_vector()
        print('save product - redis')
        products_redis = [self.format_redis_save(product) for product in self.products]
        self.r_client.add_bulk_documents(products_redis)
        print("Items completed successfully!")
        with open('status.txt', 'w', encoding='utf-8') as f:
            f.write('True')

    def recommended_products(self, text, top_k=2):
        if not self.has_embbeddings():
            self.save_redis_vectors()
        print("Initializing the search")
        query_vector = self.embedding_openai(text)
        response = self.r_client.search_similar_documents(query_vector, top_k)
        print("Search finished")
        return response

    
    
    