import json
import os
import sys
# Django settings 설정 - models 정보 가져오기
import django
from django.conf import settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from aayo.models import Cafe, MenuItem

# 파일에서 JSON 데이터 가져오기
def load_json_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# MenuItem 객체 업데이트
def update_menu_items(cafe, json_data):
    for item in json_data:
        defaults = {
            'image_url': item['image_url'],
            'category': item.get('category', ''),  # 기본값 설정
            'note': item.get('note', '')  # 기본값 설정
        }
        # 메뉴 아이템을 생성하거나 가져오기
        menu_item, created = MenuItem.objects.get_or_create(
            cafe=cafe,
            name=item['menu_name'],
            defaults=defaults
        )
        # 만약 기존에 존재하는 메뉴 아이템이면 이미지 URL, category, note 업데이트
        if not created:
            menu_item.image_url = item['image_url']
            menu_item.category = item.get('category', menu_item.category)
            menu_item.note = item.get('note', menu_item.note)
            menu_item.save()

if __name__ == "__main__":
    # 데이터 디렉토리 경로 설정
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    cafes = Cafe.objects.all()
    
    # 각 카페에 대해 JSON 데이터를 사용하여 메뉴 아이템 업데이트
    for cafe in cafes:
        print(f"## 업데이트중: {cafe.name}...")
        file_name = f"{cafe.name_eng}.json"
        file_path = os.path.join(data_dir, file_name)
        if os.path.exists(file_path):
            json_data = load_json_data(file_path)
            update_menu_items(cafe, json_data)
        else:
            print(f"File {file_name} not found for cafe {cafe.name}")

    print("Data update complete.")