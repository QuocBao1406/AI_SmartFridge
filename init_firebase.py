import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

print("🚀 Đang kết nối tới Firebase...")
cred = credentials.Certificate("serviceAccountKey.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

# DANH SÁCH 40+ MÓN ĂN VIỆT NAM PHONG PHÚ
sample_recipes = [
    # --- NHÓM MÓN MẶN / CƠM GIA ĐÌNH ---
    {"name": "Trứng chiên hành", "ingredients": "trứng gà, hành lá, nước mắm, dầu ăn, hạt nêm", "instructions": "1. Hành lá rửa sạch, thái nhỏ. 2. Đập trứng vào bát, thêm hành và gia vị, đánh đều. 3. Làm nóng chảo với dầu ăn, đổ trứng vào chiên vàng hai mặt."},
    {"name": "Thịt kho tàu", "ingredients": "thịt heo, trứng cút, nước dừa, nước mắm, đường, hành khô, tỏi", "instructions": "1. Thịt heo thái miếng vuông, ướp gia vị. 2. Thắng đường làm nước màu. 3. Cho thịt vào xào săn, đổ nước dừa và trứng cút luộc vào kho đến khi thịt mềm."},
    {"name": "Gà kho sả ớt", "ingredients": "thịt gà, sả, ớt, nước mắm, đường, tỏi", "instructions": "1. Gà chặt miếng vừa ăn, ướp sả ớt băm. 2. Phi thơm tỏi sả. 3. Xào gà săn lại rồi kho nhỏ lửa đến khi thấm gia vị."},
    {"name": "Bò lúc lắc", "ingredients": "thịt bò, hành tây, ớt chuông, tỏi, dầu hào", "instructions": "1. Thịt bò thái quân cờ. 2. Xào nhanh hành tây và ớt chuông. 3. Áp chảo thịt bò lửa lớn, trộn đều với rau củ và dầu hào."},
    {"name": "Cá kho tộ", "ingredients": "cá lóc, thịt ba chỉ, hành tím, ớt, nước mắm, tiêu", "instructions": "1. Cá làm sạch, cắt khúc. 2. Lót thịt ba chỉ dưới nồi, xếp cá lên. 3. Kho nhỏ lửa với nước mắm và nước màu đến khi sệt lại."},
    {"name": "Sườn xào chua ngọt", "ingredients": "sườn non, cà chua, hành tây, dứa, giấm, đường", "instructions": "1. Sườn chiên vàng. 2. Làm sốt từ cà chua, dứa, giấm, đường. 3. Đảo sườn với sốt đến khi sánh lại."},
    {"name": "Tôm rim mặn ngọt", "ingredients": "tôm tươi, tỏi, nước mắm, đường, tiêu", "instructions": "1. Tôm làm sạch. 2. Phi tỏi thơm, cho tôm vào đảo đỏ. 3. Nêm mắm đường rim đến khi tôm bóng giòn."},
    {"name": "Đậu hũ dồn thịt", "ingredients": "đậu hũ, thịt heo băm, nấm mèo, cà chua, hành lá", "instructions": "1. Trộn thịt băm với nấm mèo, nhồi vào đậu hũ. 2. Chiên sơ đậu hũ nhồi. 3. Sốt với cà chua và hành lá."},
    {"name": "Mực xào cần tỏi", "ingredients": "mực tươi, cần tây, tỏi tây, tỏi, dầu ăn", "instructions": "1. Mực khía bông, cắt miếng. 2. Phi tỏi, xào mực lửa lớn. 3. Cho cần tây, tỏi tây vào đảo nhanh rồi tắt bếp."},
    {"name": "Thịt heo quay kho dưa", "ingredients": "thịt heo quay, dưa cải chua, tỏi, nước mắm", "instructions": "1. Thịt quay cắt miếng. 2. Xào dưa chua với tỏi. 3. Cho thịt quay vào kho cùng dưa cải đến khi thấm."},

    # --- NHÓM MÓN CANH ---
    {"name": "Canh cà chua trứng", "ingredients": "trứng gà, cà chua, hành lá, muối", "instructions": "1. Xào cà chua mềm. 2. Đổ nước đun sôi. 3. Đánh trứng đổ vào nồi khuấy nhẹ tạo vân, rắc hành."},
    {"name": "Canh rau ngót thịt băm", "ingredients": "rau ngót, thịt heo băm, hành tím", "instructions": "1. Vò rau ngót. 2. Xào thịt băm với hành. 3. Nấu nước sôi, cho rau vào nấu chín tới."},
    {"name": "Canh chua cá", "ingredients": "cá, dứa, cà chua, dọc mùng, giá đỗ, me, rau ngổ", "instructions": "1. Nấu nước me chua. 2. Cho cá vào nấu chín rồi cho rau củ vào. 3. Nêm mắm muối và rau ngổ."},
    {"name": "Canh bí đỏ nấu tôm", "ingredients": "bí đỏ, tôm tươi, hành lá", "instructions": "1. Bí đỏ cắt miếng. 2. Tôm giã sơ. 3. Nấu nước sôi, cho bí và tôm vào hầm mềm."},
    {"name": "Canh khổ qua nhồi thịt", "ingredients": "khổ qua, thịt heo băm, nấm mèo, hành tím", "instructions": "1. Khổ qua bỏ ruột. 2. Nhồi thịt trộn nấm mèo vào. 3. Hầm trong nước dùng đến khi mềm."},
    {"name": "Canh cải bẹ xanh gừng", "ingredients": "cải bẹ xanh, gừng, thịt băm hoặc tôm", "instructions": "1. Cải cắt khúc. 2. Gừng thái sợi. 3. Nấu canh với thịt/tôm, cho gừng vào cuối để dậy mùi."},
    {"name": "Canh khoai mỡ", "ingredients": "khoai mỡ, tôm khô hoặc thịt băm, ngò gai", "instructions": "1. Khoai mỡ nạo nhỏ. 2. Nấu nước với tôm/thịt. 3. Cho khoai vào khuấy đều đến khi sệt, rắc ngò gai."},

    # --- NHÓM MÓN RAU / XÀO ---
    {"name": "Rau muống xào tỏi", "ingredients": "rau muống, tỏi, dầu ăn, nước mắm", "instructions": "1. Rau muống nhặt sạch. 2. Phi nhiều tỏi. 3. Xào rau lửa lớn nhanh tay để giữ độ giòn xanh."},
    {"name": "Bông cải xanh xào thịt bò", "ingredients": "thịt bò, bông cải xanh, tỏi, dầu hào", "instructions": "1. Thịt bò thái mỏng ướp tỏi. 2. Chần sơ bông cải. 3. Xào thịt bò nhanh rồi cho bông cải vào đảo đều."},
    {"name": "Giá đỗ xào huyết", "ingredients": "giá đỗ, huyết heo, hành lá, hẹ", "instructions": "1. Huyết cắt miếng vừa ăn. 2. Xào huyết trước cho săn. 3. Cho giá và hẹ vào đảo nhanh rồi tắt bếp."},

    # --- NHÓM MÓN ĂN SÁNG / MÓN NƯỚC ---
    {"name": "Phở bò", "ingredients": "bánh phở, thịt bò, quế, hồi, thảo quả, hành tây, ngò gai", "instructions": "1. Ninh xương với gia vị hồi quế. 2. Chần bánh phở. 3. Xếp thịt bò lên trên, chan nước dùng nóng hổi."},
    {"name": "Bún bò Huế", "ingredients": "bún tươi, thịt bò bắp, giò heo, mắm ruốc, sả, ớt", "instructions": "1. Ninh bắp bò và giò heo với sả. 2. Nêm mắm ruốc đặc trưng. 3. Ăn kèm bún và rau sống."},
    {"name": "Mì Quảng", "ingredients": "mì quảng, tôm, thịt heo, đậu phộng, bánh tráng, củ nén", "instructions": "1. Xào tôm thịt với củ nén. 2. Nấu nước dùng ít nhưng đậm đà. 3. Trộn mì với nước dùng, đậu phộng, bánh tráng."},
    {"name": "Cơm tấm sườn nướng", "ingredients": "gạo tấm, sườn heo, mật ong, dầu hào, đồ chua", "instructions": "1. Nướng sườn ướp mật ong. 2. Nấu cơm tấm. 3. Ăn kèm nước mắm chua ngọt và mỡ hành."},
    {"name": "Bún chả", "ingredients": "bún tươi, thịt heo miếng, thịt băm, đu đủ xanh, cà rốt", "instructions": "1. Nướng chả trên than hoa. 2. Pha nước chấm chua ngọt có dưa góp. 3. Ăn kèm bún và rau thơm."},

    # --- NHÓM MÓN ĂN NHANH / HIỆN ĐẠI ---
    {"name": "Kimbap (Cơm cuộn)", "ingredients": "cơm trắng, rong biển, trứng chiên, xúc xích, dưa leo, cà rốt", "instructions": "1. Trứng xúc xích cắt sợi dài. 2. Trải rong biển, dàn cơm đều. 3. Xếp nhân và cuộn chặt tay, cắt miếng nhỏ."},
    {"name": "Salad ức gà", "ingredients": "ức gà, xà lách, cà chua bi, dưa leo, sốt mè rang", "instructions": "1. Ức gà áp chảo hoặc luộc xé nhỏ. 2. Thái rau củ vừa ăn. 3. Trộn tất cả với sốt mè rang."},
    {"name": "Mì Ý sốt bò băm", "ingredients": "mì ý, thịt bò băm, cà chua, hành tây, tỏi", "instructions": "1. Luộc mì. 2. Làm sốt từ thịt bò và cà chua. 3. Trộn mì với sốt và rắc tiêu."},
    {"name": "Bánh mì dân tổ", "ingredients": "bánh mì, trứng, xúc xích, pate, chả, bơ", "instructions": "1. Cho tất cả nhân vào chảo xào chung với bơ. 2. Kẹp hỗn hợp vào bánh mì. 3. Ăn kèm dưa chuột và tương ớt."},
    {"name": "Trứng hấp vân", "ingredients": "trứng gà, giò sống, mộc nhĩ, nấm hương", "instructions": "1. Tráng trứng mỏng. 2. Phết giò sống trộn nấm lên trên trứng. 3. Cuộn tròn lại và hấp chín, cắt lát."},

    # --- THÊM CÁC MÓN PHỔ BIẾN KHÁC ---
    {"name": "Cá thu sốt cà", "ingredients": "cá thu, cà chua, hành lá, tỏi", "instructions": "1. Chiên sơ cá thu. 2. Làm sốt cà chua. 3. Rim cá với sốt cà chua nhỏ lửa."},
    {"name": "Thịt bò xào thiên lý", "ingredients": "thịt bò, hoa thiên lý, tỏi, hạt nêm", "instructions": "1. Ướp thịt bò. 2. Phi tỏi thơm, xào thịt bò tái. 3. Cho hoa thiên lý vào đảo nhanh tay."},
    {"name": "Canh bí xanh nấu tôm", "ingredients": "bí xanh, tôm tươi, hành lá, gừng", "instructions": "1. Bí xanh gọt vỏ, thái miếng. 2. Tôm giã dập. 3. Nấu canh bí với tôm, thêm lát gừng cho thơm."},
    {"name": "Cơm chiên dương châu", "ingredients": "cơm nguội, trứng, đậu hà lan, cà rốt, lạp xưởng", "instructions": "1. Cắt nhỏ lạp xưởng, rau củ. 2. Chiên cơm với trứng cho tơi. 3. Trộn đều nhân vào cơm chiên."},
    {"name": "Gỏi cuốn", "ingredients": "bánh tráng, tôm luộc, thịt heo luộc, bún, rau sống, hẹ", "instructions": "1. Sắp xếp tôm, thịt, bún, rau lên bánh tráng. 2. Cuộn chặt lại kèm lá hẹ trang trí. 3. Chấm mắm nêm hoặc tương đậu."},
    {"name": "Bún đậu mắm tôm", "ingredients": "bún lá, đậu hũ, thịt chân giò, mắm tôm, chả cốm", "instructions": "1. Chiên đậu hũ vàng giòn. 2. Luộc thịt chân giò thái mỏng. 3. Ăn kèm bún lá, rau thơm và mắm tôm pha chanh đường."},
    {"name": "Miến xào lòng gà", "ingredients": "miến, lòng gà, mộc nhĩ, hành tây, hành lá", "instructions": "1. Ngâm miến cho mềm. 2. Xào lòng gà với mộc nhĩ. 3. Cho miến vào đảo cùng gia vị đến khi sợi miến trong lại."},
    {"name": "Canh cua mồng tơi", "ingredients": "cua đồng, rau mồng tơi, rau đay, mướp", "instructions": "1. Lọc nước cua đun sôi cho nổi gạch. 2. Cho mướp và rau vào nấu chín. 3. Ăn kèm cà pháo muối là ngon nhất."},
    {"name": "Thịt heo xào sả ớt", "ingredients": "thịt heo, sả, ớt, tỏi, hành tím", "instructions": "1. Thịt heo thái mỏng. 2. Phi thơm sả ớt. 3. Xào thịt heo lửa lớn đến khi cháy cạnh và thơm mùi sả."},
    {"name": "Ốc xào chuối đậu", "ingredients": "ốc, chuối xanh, đậu hũ, thịt ba chỉ, lá lốt, tía tô", "instructions": "1. Chuối tước vỏ cắt khúc. 2. Xào thịt, đậu chiên và ốc. 3. Nấu chín mềm chuối, thêm lá lốt tía tô vào cuối."},
]

print(f"🔄 Đang đẩy {len(sample_recipes)} món ăn lên Firestore...")
recipes_ref = db.collection("recipes")

for recipe in sample_recipes:
    # Kiểm tra trùng lặp theo tên món
    query = recipes_ref.where("name", "==", recipe["name"]).get()
    if len(query) == 0:
        recipes_ref.add(recipe)
        print(f"✅ Đã thêm: {recipe['name']}")
    else:
        print(f"⏭️ Bỏ qua (đã có): {recipe['name']}")

print("\n✨ Hoàn tất! Hệ thống của bro đã có một kho tàng ẩm thực thực thụ.")