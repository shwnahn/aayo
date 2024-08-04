import json
import os
import sys
import django
from django.conf import settings

# Django settings 설정
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from aayo.models import Cafe, MenuItem  # 여기서 myapp은 실제 앱 이름으로 변경해야 합니다

def load_json_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def update_menu_items(cafe_name, json_data):
    cafe, created = Cafe.objects.get_or_create(name=cafe_name)
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
    for file_name in os.listdir(data_dir):
        if file_name.endswith('.json'):
            cafe_name = os.path.splitext(file_name)[0]
            file_path = os.path.join(data_dir, file_name)
            json_data = load_json_data(file_path)
            update_menu_items(cafe_name, json_data)

    print("Data update complete.")