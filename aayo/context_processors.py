from django.conf import settings

def kakao_app_key(request):
    return {'KAKAO_APP_KEY': settings.KAKAO_APP_KEY}