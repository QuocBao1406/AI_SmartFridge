import firebase_admin
from firebase_admin import credentials, firestore
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SPICES = [
    "nước mắm", "dầu ăn", "muối", "đường", "tiêu", "bột ngọt", "mì chính",
    "hạt nêm", "tỏi", "hành khô", "gừng", "nước tương", "xì dầu", "giấm", "ớt", "chanh"
]

def clean_for_ai(ingredients_data):
    if isinstance(ingredients_data, (list, tuple)):
        text = ", ".join(ingredients_data).lower()
    else:
        text = str(ingredients_data).lower()
    for spice in SPICES:
        text = text.replace(spice, "")
    text = text.replace(",", " ").replace(" ", " ").strip()
    return text

print("1. Đang khởi động Server API...")
print("2. Đang kết nối Firebase và tải công thức...")
cred = credentials.Certificate("serviceAccountKey.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()
docs = db.collection("recipes").stream()

recipe_list = []
for doc in docs:
    data = doc.to_dict()
    recipe_list.append({
        'id': doc.id,
        'name': data.get('name', ''),
        'ingredients': data.get('ingredients', ''),
        'instructions': data.get('instructions', '')
    })

df = pd.DataFrame(recipe_list)
print(f"-> Đã tải xong {len(df)} công thức nấu ăn!")

print("3. Đang huấn luyện AI...")

df['ai_text'] = df['ingredients'].apply(clean_for_ai)

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['ai_text'])

print("-> AI đã sẵn sàng nhận yêu cầu!")

app = FastAPI(title = "Smart Fridge AI API")

class RecipeRequest(BaseModel):
    ingredients: List[str]

@app.post("/api/suggest-recipe")
def suggest_recipe(request: RecipeRequest):
    if df.empty:
        return {"success": False, "message": "Database trống!"}
    
    input_str = ", ".join(request.ingredients)
    clean_input = clean_for_ai(input_str)

    input_vector = vectorizer.transform([clean_input])
    similarity_scores = cosine_similarity(input_vector, tfidf_matrix)

    best_match_idx = similarity_scores[0].argmax()
    best_score = similarity_scores[0][best_match_idx]

    if best_score < 0.3:
        return {
            "success": False,
            "message": "Không tìm thấy món ăn nào phù hợp với nguyên liệu"
        }
    
    suggest_dish = df.iloc[best_match_idx]

    return {
        "success": True,
        "match_score": round(best_score * 100, 2),
        "recipe_name": suggest_dish['name'],
        "ingredients": suggest_dish['ingredients'],
        "instructions": suggest_dish['instructions']
    }

@app.get("/api/ping")
def ping():
    return {"status:" "AI Server is awake!"}