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

    suggest_dish = df.iloc[best_match_idx]

    user_foods = [food.lower().strip() for food in request.ingredients]
    
    original_ingredients = suggest_dish['ingredients'].split(',')
    
    # 3. Lọc ra danh sách "Nguyên liệu chính" (Bỏ qua mắm, muối, hành, tỏi...)
    main_ingredients = []
    for item in original_ingredients:
        item_clean = item.lower().strip()
        # Nếu món này không chứa từ nào trong Blacklist -> Nó là nguyên liệu chính
        if not any(spice in item_clean for spice in SPICES):
            main_ingredients.append(item_clean)
            
    # 4. Đếm số lượng nguyên liệu chính mà user ĐANG CÓ trong tủ
    matched_count = 0
    for recipe_food in main_ingredients:
        # Nếu đồ trong tủ khớp với đồ của công thức (VD: "chuối" khớp "chuối xanh")
        if any(u_food in recipe_food or recipe_food in u_food for u_food in user_foods):
            matched_count += 1
            
    # 5. Tính Tỉ lệ (Ví dụ: Có 1 món trên tổng số 4 nguyên liệu chính -> 25%)
    total_main = len(main_ingredients)
    coverage_ratio = matched_count / total_main if total_main > 0 else 0
    
    # 6. PHÁN QUYẾT: Nếu có ít hơn 50% nguyên liệu chính -> Chặn!
    if coverage_ratio < 0.5:
        return {
            "success": False, 
            "message": f"Món phù hợp nhất là '{suggest_dish['name']}', nhưng bạn chỉ có {matched_count}/{total_main} nguyên liệu chính. Không đủ đồ để nấu rồi, hãy đi chợ thêm nhé!"
        }
    
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