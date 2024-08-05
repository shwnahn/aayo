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

def load_json_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def update_menu_items(cafe, json_data):
    for item in json_data:
        menu_item, created = MenuItem.objects.get_or_create(
            cafe=cafe,
            name=item['menu_name'],
            defaults={'image_url': item['image_url']}
        )
        if not created:
            menu_item.image_url = item['image_url']
            menu_item.save()

if __name__ == "__main__":
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    cafes = Cafe.objects.all()
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