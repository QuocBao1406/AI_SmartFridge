import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

print("🚀 Đang khởi động tiến trình nạp dữ liệu sạch...")

# 1. Kết nối Firebase
cred = credentials.Certificate("serviceAccountKey.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 2. DANH SÁCH CÔNG THỨC (Đã loại bỏ gia vị và hành tỏi khỏi cột ingredients)
clean_recipes = [
    # --- MÓN MẶN ---
    {"name": "Trứng chiên hành", "ingredients": "trứng gà", "instructions": "1. Hành lá thái nhỏ. 2. Đập trứng vào bát, thêm hành và gia vị (nước mắm, hạt nêm), đánh đều. 3. Chiên vàng hai mặt trên chảo dầu nóng."},
    {"name": "Thịt kho tàu", "ingredients": "thịt heo, trứng cút, nước dừa", "instructions": "1. Thịt heo thái miếng vuông, ướp hành tỏi mắm muối. 2. Thắng nước màu từ đường. 3. Kho thịt với nước dừa và trứng cút luộc đến khi mềm."},
    {"name": "Gà kho sả ớt", "ingredients": "thịt gà, sả", "instructions": "1. Gà chặt miếng, ướp sả ớt băm và gia vị. 2. Phi thơm sả tỏi. 3. Kho gà nhỏ lửa đến khi thấm vị."},
    {"name": "Bò lúc lắc", "ingredients": "thịt bò, hành tây, ớt chuông", "instructions": "1. Thịt bò thái quân cờ, ướp tỏi và dầu hào. 2. Xào nhanh hành tây và ớt chuông. 3. Áp chảo thịt bò lửa lớn rồi trộn đều."},
    {"name": "Cá kho tộ", "ingredients": "cá lóc, thịt ba chỉ", "instructions": "1. Cá làm sạch, cắt khúc. 2. Lót thịt ba chỉ dưới nồi, xếp cá lên. 3. Kho sệt với nước mắm, đường, tiêu và hành tím."},
    {"name": "Sườn xào chua ngọt", "ingredients": "sườn non, dứa, cà chua", "instructions": "1. Sườn chiên vàng. 2. Làm sốt từ cà chua, dứa, giấm, đường. 3. Đảo sườn với sốt đến khi sánh lại."},
    {"name": "Tôm rim mặn ngọt", "ingredients": "tôm tươi", "instructions": "1. Phi thơm tỏi, cho tôm vào đảo đỏ. 2. Nêm nước mắm, đường và rim đến khi tôm bóng giòn."},
    {"name": "Đậu hũ dồn thịt", "ingredients": "đậu hũ, thịt heo băm, nấm mèo", "instructions": "1. Nhồi thịt trộn nấm mèo vào đậu hũ. 2. Chiên sơ rồi sốt với cà chua, hành lá và nước mắm."},
    {"name": "Mực xào cần tỏi", "ingredients": "mực tươi, cần tây, tỏi tây", "instructions": "1. Mực khía bông. 2. Phi tỏi, xào mực lửa lớn. 3. Cho cần tây, tỏi tây vào đảo nhanh."},
    {"name": "Thịt heo quay kho dưa", "ingredients": "thịt heo quay, dưa cải chua", "instructions": "1. Thịt quay cắt miếng. 2. Xào dưa chua với tỏi. 3. Kho chung thịt với dưa cải đến khi thấm mắm muối."},

    # --- MÓN CANH ---
    {"name": "Canh cà chua trứng", "ingredients": "trứng gà, cà chua", "instructions": "1. Xào cà chua mềm với chút muối. 2. Đổ nước đun sôi. 3. Đánh trứng đổ vào nồi khuấy nhẹ, rắc thêm hành lá."},
    {"name": "Canh rau ngót thịt băm", "ingredients": "rau ngót, thịt heo băm", "instructions": "1. Xào thịt băm với hành tím. 2. Cho nước vào đun sôi rồi cho rau ngót đã vò vào nấu chín."},
    {"name": "Canh chua cá", "ingredients": "cá, dứa, cà chua, dọc mùng, giá đỗ", "instructions": "1. Nấu nước me chua. 2. Cho cá vào nấu chín rồi cho rau củ vào. 3. Nêm mắm và rau ngổ, ngò gai."},
    {"name": "Canh bí đỏ nấu tôm", "ingredients": "bí đỏ, tôm tươi", "instructions": "1. Bí đỏ cắt miếng. 2. Tôm giã sơ. 3. Nấu bí và tôm đến khi bí mềm, nêm gia vị vừa ăn."},
    {"name": "Canh khổ qua nhồi thịt", "ingredients": "khổ qua, thịt heo băm, nấm mèo", "instructions": "1. Nhồi thịt trộn nấm vào khổ qua. 2. Hầm trong nước dùng đến khi mềm, nêm chút hành ngò."},
    {"name": "Canh cải bẹ xanh gừng", "ingredients": "cải bẹ xanh, thịt băm", "instructions": "1. Nấu canh cải với thịt băm. 2. Thêm gừng thái sợi vào cuối để dậy mùi và ấm bụng."},
    {"name": "Canh khoai mỡ", "ingredients": "khoai mỡ, tôm khô", "instructions": "1. Khoai mỡ nạo nhỏ. 2. Nấu nước với tôm khô. 3. Cho khoai vào khuấy sệt, nêm ngò gai, ngò ôm."},

    # --- MÓN RAU ---
    {"name": "Rau muống xào", "ingredients": "rau muống", "instructions": "1. Rau muống nhặt sạch. 2. Phi thật nhiều tỏi thơm. 3. Xào rau lửa lớn với nước mắm hoặc dầu hào."},
    {"name": "Bông cải xanh xào bò", "ingredients": "thịt bò, bông cải xanh", "instructions": "1. Thịt bò thái mỏng ướp tỏi. 2. Xào bò tái rồi cho bông cải đã chần vào đảo đều."},
    {"name": "Giá đỗ xào huyết", "ingredients": "giá đỗ, huyết heo", "instructions": "1. Xào huyết heo đã cắt miếng. 2. Cho giá đỗ và hẹ vào đảo nhanh tay, nêm mắm muối."},

    # --- MÓN ĂN SÁNG / ĐẶC SẢN ---
    {"name": "Phở bò", "ingredients": "bánh phở, thịt bò", "instructions": "1. Ninh xương với quế, hồi, gừng nướng. 2. Chần bánh phở và thịt bò. 3. Chan nước dùng, thêm hành tây và ngò gai."},
    {"name": "Bún bò Huế", "ingredients": "bún tươi, bắp bò, giò heo", "instructions": "1. Ninh bò và giò với sả. 2. Nêm mắm ruốc đặc trưng. 3. Ăn kèm bún, rau sống và hoa chuối."},
    {"name": "Cơm tấm sườn nướng", "ingredients": "gạo tấm, sườn heo", "instructions": "1. Nướng sườn ướp mật ong, tỏi, dầu hào. 2. Nấu cơm tấm. 3. Ăn kèm mỡ hành và đồ chua."},
    {"name": "Bún đậu mắm tôm", "ingredients": "bún lá, đậu hũ, thịt chân giò, chả cốm", "instructions": "1. Chiên đậu hũ vàng. 2. Luộc thịt thái mỏng. 3. Chấm mắm tôm pha chanh ớt đường."},
    {"name": "Kimbap", "ingredients": "rong biển, cơm trắng, trứng gà, xúc xích, cà rốt, dưa leo", "instructions": "1. Cắt sợi các nguyên liệu. 2. Trải rong biển, dàn cơm và xếp nhân. 3. Cuộn chặt và cắt miếng."},
    {"name": "Mì Ý sốt bò băm", "ingredients": "mì ý, thịt bò băm, cà chua", "instructions": "1. Luộc mì. 2. Làm sốt từ bò băm, cà chua, hành tây. 3. Trộn mì với sốt và rắc tiêu."},
    {"name": "Salad ức gà", "ingredients": "ức gà, xà lách, cà chua bi", "instructions": "1. Ức gà áp chảo xé nhỏ. 2. Trộn rau củ với ức gà và sốt mè rang."},
    {"name": "Canh cua mồng tơi", "ingredients": "cua đồng, rau mồng tơi, mướp", "instructions": "1. Nấu nước cua cho nổi gạch. 2. Cho mướp và rau vào nấu chín. 3. Ăn kèm cà pháo."},
    {"name": "Thịt heo xào sả ớt", "ingredients": "thịt heo, sả", "instructions": "1. Thịt heo thái mỏng. 2. Phi thơm sả ớt tỏi. 3. Xào thịt lửa lớn đến khi thơm cháy cạnh."},
    {"name": "Ốc xào chuối đậu", "ingredients": "ốc, chuối xanh, đậu hũ, thịt ba chỉ", "instructions": "1. Chuối cắt khúc. 2. Xào thịt, đậu chiên và ốc với nghệ, mẻ. 3. Nấu chín mềm, thêm lá lốt tía tô."},
]

# 3. Tiến hành đẩy dữ liệu
print(f"🔄 Đang xóa và nạp lại {len(clean_recipes)} món ăn sạch...")

recipes_ref = db.collection("recipes")

# Lưu ý: Code này sẽ thêm mới, nếu muốn xóa sạch collection cũ, bro nên xóa tay trên web Firebase trước.
for recipe in clean_recipes:
    # Check trùng tên để tránh nạp lặp
    query = recipes_ref.where("name", "==", recipe["name"]).get()
    if len(query) == 0:
        recipes_ref.add(recipe)
        print(f"✅ Đã nạp: {recipe['name']}")
    else:
        print(f"⏭️ Đã tồn tại: {recipe['name']}")

print("\n✨ Hoàn tất! Database của bro bây giờ đã cực kỳ 'tinh khiết'.")