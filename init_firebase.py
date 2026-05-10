import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

print("Đang kết nối tới Firebase...")
cred = credentials.Certificate("serviceAccountKey.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

sample_recipes = [
    {
        "name": "Trứng chiên hành",
        "ingredients": "trứng gà, hành lá, nước mắm, dầu ăn, hạt nêm",
        "instructions": "1. Hành lá rửa sạch, thái nhỏ. 2. Đập trứng vào bát, thêm hành và gia vị, đánh đều. 3. Làm nóng chảo với dầu ăn, đổ trứng vào chiên vàng hai mặt."
    },
    {
        "name": "Canh cà chua trứng",
        "ingredients": "trứng gà, cà chua, hành lá, muối, dầu ăn",
        "instructions": "1. Cà chua thái múi cau. 2. Xào cà chua với dầu ăn cho mềm, đổ nước vào đun sôi. 3. Đánh trứng đổ từ từ vào nồi nước đang sôi, khuấy nhẹ. 4. Rắc hành lá và tắt bếp."
    },
    {
        "name": "Thịt kho tàu",
        "ingredients": "thịt heo, trứng cút, nước dừa, nước mắm, đường, hành khô, tỏi",
        "instructions": "1. Thịt heo thái miếng vuông, ướp gia vị. 2. Thắng đường làm nước màu. 3. Cho thịt vào xào săn, đổ nước dừa và trứng cút luộc vào kho đến khi thịt mềm."
    },
    {
        "name": "Rau muống xào tỏi",
        "ingredients": "rau muống, tỏi, dầu ăn, nước mắm, muối",
        "instructions": "1. Rau muống nhặt sạch. 2. Phi thơm tỏi băm với dầu ăn. 3. Cho rau muống vào xào nhanh tay với lửa lớn, nêm gia vị vừa ăn rồi tắt bếp."
    },
    {
        "name": "Gà kho sả ớt",
        "ingredients": "thịt gà, sả, ớt, nước mắm, đường, tỏi, màu dầu điều",
        "instructions": "1. Gà chặt miếng vừa ăn, ướp sả ớt băm và gia vị. 2. Phi thơm tỏi và sả. 3. Cho gà vào xào săn, thêm ít nước rồi kho đến khi nước sệt lại."
    },
    {
        "name": "Canh rau ngót thịt băm",
        "ingredients": "thịt heo băm, rau ngót, muối, hạt nêm, hành khô",
        "instructions": "1. Rau ngót tuốt lá, vò sơ. 2. Phi hành, xào thịt băm. 3. Đổ nước vào đun sôi, cho rau ngót vào nấu chín, nêm lại gia vị."
    },
    {
        "name": "Bò lúc lắc",
        "ingredients": "thịt bò, hành tây, ớt chuông, tỏi, dầu hào, nước tương",
        "instructions": "1. Thịt bò thái quân cờ, ướp dầu hào. 2. Xào hành tây và ớt chuông trước. 3. Áp chảo thịt bò với lửa cực lớn cho cháy cạnh, trộn đều với rau củ."
    },
    {
        "name": "Đậu hũ sốt cà chua",
        "ingredients": "đậu hũ, cà chua, hành lá, nước mắm, đường",
        "instructions": "1. Đậu hũ cắt miếng, chiên vàng. 2. Xào nát cà chua với ít nước tạo sốt. 3. Cho đậu hũ vào rim cùng sốt cà chua, thêm hành lá."
    },
    {
        "name": "Sườn xào chua ngọt",
        "ingredients": "sườn non, hành tây, dứa, cà chua, giấm, đường, nước mắm",
        "instructions": "1. Sườn chặt nhỏ, chiên vàng. 2. Pha nước sốt chua ngọt từ giấm, đường, mắm. 3. Đảo sườn với nước sốt và rau củ cho đến khi thấm đều."
    },
    {
        "name": "Cá kho tộ",
        "ingredients": "cá lóc, thịt ba chỉ, hành tím, ớt, nước mắm, tiêu",
        "instructions": "1. Cá làm sạch, cắt khúc. 2. Lót thịt ba chỉ dưới đáy tộ, xếp cá lên trên. 3. Thêm gia vị, nước hàng và kho nhỏ lửa đến khi nước cạn gần hết."
    },
    {
        "name": "Canh bí đỏ nấu tôm",
        "ingredients": "bí đỏ, tôm tươi, hành lá, ngò gai, muối, tiêu",
        "instructions": "1. Bí đỏ gọt vỏ, cắt miếng. 2. Tôm bóc vỏ, giã sơ. 3. Nấu nước sôi, cho tôm và bí vào hầm đến khi bí mềm, rắc hành ngò."
    },
    {
        "name": "Thịt heo luộc",
        "ingredients": "thịt heo, muối, hành tím, gừng",
        "instructions": "1. Thịt heo rửa sạch. 2. Đun sôi nước với hành tím và gừng đập dập. 3. Cho thịt vào luộc chín tới, vớt ra ngâm nước lạnh rồi thái mỏng."
    },
    {
        "name": "Mực xào dứa",
        "ingredients": "mực tươi, dứa, cần tây, tỏi, dầu hào, tiêu",
        "instructions": "1. Mực làm sạch, khía vảy rồng. 2. Phi tỏi, xào mực với lửa lớn. 3. Cho dứa và cần tây vào đảo nhanh, nêm dầu hào rồi tắt bếp."
    },
    {
        "name": "Canh chua cá",
        "ingredients": "cá, dứa, cà chua, dọc mùng, giá đỗ, me, rau ngổ",
        "instructions": "1. Nấu nước me chua, cho cá vào nấu chín. 2. Thêm dứa, cà chua, dọc mùng vào nồi. 3. Cuối cùng cho giá và rau ngổ, nêm mắm muối cho vừa miệng."
    },
    {
        "name": "Tôm rim mặn ngọt",
        "ingredients": "tôm tươi, tỏi, đường, nước mắm, tiêu, dầu ăn",
        "instructions": "1. Tôm cắt bỏ râu. 2. Phi thơm tỏi băm. 3. Cho tôm vào đảo đỏ, thêm mắm và đường, rim đến khi vỏ tôm bóng giòn."
    }
]

print(f"Đang đẩy {len(sample_recipes)} món ăn lên Firestore...")
recipes_ref = db.collection("recipes")

for recipe in sample_recipes:
    query = recipes_ref.where("name", "==", recipe["name"]).get()
    if len(query) == 0:
        recipes_ref.add(recipe)
        print(f"Đã thêm: {recipe['name']}")
    else:
        print(f"Bỏ qua (đã có): {recipe['name']}")

print("Đã tải dữ liệu lên Firebase thành công!")