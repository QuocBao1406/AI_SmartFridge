import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, firestore
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ==========================================
# 1. KHỞI TẠO APP VÀ KẾT NỐI FIREBASE
# ==========================================
app = FastAPI()

print("1. Đang khởi động Server API...")
try:
    cred = credentials.Certificate("serviceAccountKey.json")
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    db = firestore.client()
except Exception as e:
    print(f"❌ Lỗi kết nối Firebase: {e}")

# Các biến toàn cục lưu trữ bộ não AI
df = None
vectorizer = None
tfidf_matrix = None

# ==========================================
# 2. HUẤN LUYỆN AI TỪ DỮ LIỆU FIREBASE
# ==========================================
def load_and_train_ai():
    global df, vectorizer, tfidf_matrix
    print("2. Đang kết nối Firebase và tải công thức...")
    
    recipes_ref = db.collection("recipes").get()
    recipes_list = []
    
    for doc in recipes_ref:
        recipes_list.append(doc.to_dict())
        
    if not recipes_list:
        print("⚠️ Cảnh báo: Không có công thức nào trên Firebase!")
        return

    print(f"-> Đã tải xong {len(recipes_list)} công thức nấu ăn!")
    df = pd.DataFrame(recipes_list)
    
    print("3. Đang huấn luyện AI...")
    # AI học dựa trên cột 'ingredients' đã được bro dọn sạch gia vị
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df['ingredients'])
    
    print("-> AI đã sẵn sàng nhận yêu cầu!")

# Chạy huấn luyện ngay khi bật server
load_and_train_ai()

# ==========================================
# 3. MODEL DỮ LIỆU
# ==========================================
class RecipeRequest(BaseModel):
    ingredients: list[str]

# ==========================================
# 4. CÁC API ENDPOINTS
# ==========================================

# API Ping giữ mạng cho Render
@app.get("/api/ping")
def ping():
    return {"status": "AI Server is awake!"}

# API Gợi ý món ăn (Trả về DANH SÁCH)
@app.post("/api/suggest-recipe")
def suggest_recipe(request: RecipeRequest):
    global df, vectorizer, tfidf_matrix
    
    if df is None or df.empty:
        return {"success": False, "message": "Dữ liệu AI chưa sẵn sàng."}

    if not request.ingredients:
        return {"success": False, "message": "Tủ lạnh trống, không có gì để gợi ý!"}

    # Chuẩn hóa đầu vào từ Android
    user_foods = [food.lower().strip() for food in request.ingredients]
    user_text = " ".join(user_foods)
    
    # Tính toán độ tương đồng
    user_vector = vectorizer.transform([user_text])
    similarities = cosine_similarity(user_vector, tfidf_matrix).flatten()
    
    # Sắp xếp để lấy những món có điểm cao nhất (giảm dần)
    top_indices = similarities.argsort()[::-1]
    
    suggested_recipes = []
    
    for idx in top_indices:
        score = similarities[idx]
        
        # Nếu món ăn quá không liên quan (điểm < 0.1) thì bỏ qua các món sau luôn
        if score < 0.1:
            break
            
        dish = df.iloc[idx]
        
        # --- THUẬT TOÁN KIỂM TRA ĐỘ BAO PHỦ (COVERAGE) ---
        # Lấy list nguyên liệu chính của món ăn này
        recipe_main_ingredients = [item.lower().strip() for item in dish['ingredients'].split(',')]
        
        # Đếm số món trong tủ khớp với công thức
        matched_count = 0
        for r_food in recipe_main_ingredients:
            if any(u_food in r_food or r_food in u_food for u_food in user_foods):
                matched_count += 1
        
        # Tính tỷ lệ (Ví dụ: có 2/3 nguyên liệu chính = 66% -> ĐẠT)
        total_needed = len(recipe_main_ingredients)
        coverage_ratio = matched_count / total_needed if total_needed > 0 else 0
        
        # CHỈ CHỌN: Nếu người dùng có ít nhất 50% nguyên liệu chính của món đó
        if coverage_ratio >= 0.5:
            suggested_recipes.append({
                "recipe_name": dish['name'],
                "ingredients": dish['ingredients'],
                "instructions": dish['instructions']
            })
            
        # Dừng lại khi đã tìm đủ 4 món ngon nhất
        if len(suggested_recipes) >= 4:
            break

    # Trả kết quả về cho Android
    if not suggested_recipes:
        return {
            "success": False, 
            "message": "Không tìm thấy món nào đủ nguyên liệu chính. Bạn cần đi chợ thêm rồi!"
        }

    return {
        "success": True,
        "data": suggested_recipes # Trả về mảng các Object món ăn
    }

@app.get("/api/ping")
def ping():
    return {"status:" "AI Server is awake!"}