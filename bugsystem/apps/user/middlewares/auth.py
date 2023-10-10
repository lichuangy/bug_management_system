
from django.utils.deprecation import MiddlewareMixin
from ..models import UserInfo

class AuthMiddelware(MiddlewareMixin):

    def process_request(self,request):
        """如果用户已登录，request中赋值"""
        user_id = request.session.get('user_id')

        user_object = UserInfo.objects.filter(id=user_id)
        request.user = user_object
