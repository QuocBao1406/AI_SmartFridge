import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, firestore
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

print("1. Đang khởi động Server API...")
try:
    cred = credentials.Certificate("serviceAccountKey.json")
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    db = firestore.client()
except Exception as e:
    print(f"Lỗi kết nối Firebase: {e}")

# Các biến toàn cục cho AI
df = None
vectorizer = None
tfidf_matrix = None

# ==========================================
# 2. HÀM TẢI DỮ LIỆU & HUẤN LUYỆN AI
# ==========================================
def load_and_train_ai():
    global df, vectorizer, tfidf_matrix
    print("2. Đang kết nối Firebase và tải công thức...")
    
    recipes_ref = db.collection("recipes").get()
    recipes_list = []
    
    for doc in recipes_ref:
        recipes_list.append(doc.to_dict())
        
    if not recipes_list:
        print("Cảnh báo: Không có công thức nào trên Firebase!")
        return

    print(f"-> Đã tải xong {len(recipes_list)} công thức nấu ăn!")
    
    # Đưa vào Pandas DataFrame
    df = pd.DataFrame(recipes_list)
    
    print("3. Đang huấn luyện AI...")
    # Huấn luyện mô hình TF-IDF dựa trên cột 'ingredients'
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df['ingredients'])
    
    print("-> AI đã sẵn sàng nhận yêu cầu!")

# Chạy hàm huấn luyện ngay khi khởi động Server
load_and_train_ai()

# ==========================================
# 3. ĐỊNH NGHĨA DỮ LIỆU ĐẦU VÀO TỪ ANDROID
# ==========================================
class RecipeRequest(BaseModel):
    ingredients: list[str]

# ==========================================
# 4. API KẾT NỐI (ENDPOINTS)
# ==========================================

# API Ping dùng cho Cron-job (Giữ Server thức 24/7)
@app.get("/api/ping")
def ping():
    return {"status": "AI Server is awake!"}

# API Chính: Nhận nguyên liệu và trả về Món ăn
@app.post("/api/suggest-recipe")
def suggest_recipe(request: RecipeRequest):
    global df, vectorizer, tfidf_matrix
    
    if df is None or df.empty:
        return {"success": False, "message": "Hệ thống AI chưa sẵn sàng hoặc không có dữ liệu."}

    if not request.ingredients:
        return {"success": False, "message": "Bạn chưa cung cấp nguyên liệu nào!"}

    # Gom đồ ăn user gửi lên thành 1 chuỗi để AI quét TF-IDF
    user_foods = [food.lower().strip() for food in request.ingredients]
    user_text = " ".join(user_foods)
    
    # AI bắt đầu tính điểm khớp (Cosine Similarity)
    user_vector = vectorizer.transform([user_text])
    similarities = cosine_similarity(user_vector, tfidf_matrix).flatten()
    
    best_match_idx = similarities.argmax()
    best_score = similarities[best_match_idx]

    # Nâng điểm sàn: Ít nhất phải khớp 15% từ khóa
    if best_score < 0.15:
        return {
            "success": False, 
            "message": "Không tìm thấy món nào đủ độ phù hợp với các nguyên liệu này."
        }

    # Lấy thông tin món ăn được AI chấm điểm cao nhất
    suggested_dish = df.iloc[best_match_idx]
    
    # ==========================================
    # ĐOẠN LOGIC CHẶN CỬA V3: TỈ LỆ BAO PHỦ 50%
    # ==========================================
    # Lấy nguyên liệu chính của món ăn (đã được dọn sạch gia vị trên Firebase)
    main_ingredients = [item.lower().strip() for item in suggested_dish['ingredients'].split(',')]
            
    # Đếm xem tủ lạnh user có bao nhiêu món khớp với nguyên liệu chính
    matched_count = 0
    for recipe_food in main_ingredients:
        if any(u_food in recipe_food or recipe_food in u_food for u_food in user_foods):
            matched_count += 1
            
    # Tính tỉ lệ
    total_main = len(main_ingredients)
    coverage_ratio = matched_count / total_main if total_main > 0 else 0
    
    # Nếu đồ trong tủ đáp ứng < 50% nguyên liệu chính -> Báo thiếu đồ
    if coverage_ratio < 0.5:
        return {
            "success": False, 
            "message": f"Món phù hợp nhất là '{suggested_dish['name']}', nhưng bạn chỉ có {matched_count}/{total_main} nguyên liệu chính. Không đủ đồ để nấu rồi, hãy đi chợ thêm nhé!"
        }
    # ==========================================

    # Nếu qua được vòng kiểm duyệt, trả kết quả về cho Android
    return {
        "success": True,
        "recipe_name": suggested_dish['name'],
        "ingredients": suggested_dish['ingredients'],
        "instructions": suggested_dish['instructions']
    }

@app.get("/api/ping")
def ping():
    return {"status:" "AI Server is awake!"}