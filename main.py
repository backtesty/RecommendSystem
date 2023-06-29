from core.Recommendation import CoreRecommendation


def get_recommend_items(text, top_k=2):
    api_url = 'https://fakestoreapi.com/products'
    c_search = CoreRecommendation(api_url)
    items = c_search.recommended_products(text, top_k)
    return items


text_search = 'I need Men casual t-shits'
items = get_recommend_items(text_search, top_k=5)
print(items)