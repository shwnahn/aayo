import os
import json
from django.conf import settings
from aayo.models import Cafe, MenuItem

def update_data():
    data_dir = os.path.join(settings.BASE_DIR, 'data')
    for filename in os.listdir(data_dir):
        if filename.endswith('.json'):
            cafe_name = filename.replace('.json', '')
            with open(os.path.join(data_dir, filename), 'r', encoding='utf-8') as f:
                data = json.load(f)
                cafe, created = Cafe.objects.get_or_create(name=cafe_name)
                for item in data:
                    MenuItem.objects.update_or_create(
                        cafe=cafe,
                        name=item['menu_name'],
                        defaults={'image_url': item.get('image_url')}
                    )