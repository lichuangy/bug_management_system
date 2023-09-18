from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
import re
from django_redis import get_redis_connection

from .forms.register import RegisterModelForm
from .models import UserInfo

# Create your views here.

"""

需求：前端通过点击 获取验证码 按钮后，发送ajax请求携带参数，后端接受参数验证参数并发送验证码

前端 ：发送ajax 请假，参数：手机号和模板类型名

后端：
    1.接受请求：手机号和模板类型名

    2.业务逻辑：根据传输过来的手机号和模板类型名，验证数据是否为空，是否被注册过了，查询数据库验证

    3响应

    4.路由 GET  sendsms/

    5步骤
        接受手机号，模板类型名
        验证数据
        返回响应
"""

def sendsms(request):
    """
    发送短信
    """

    # 接收手机号，模板类型名

    # 获取手机号
    phone = request.GET.get('phone')
    # 获取模板
    tpl = request.GET.get('tpl')
    # 验证数据
    # 是否未空
    if not phone:
        return JsonResponse({'code':400,'err_msg':'参数缺失'})
    # 验证手机号是否合规
    form = RegisterModelForm(data={'mobile_phone':phone})
    if not form.is_valid():
        return JsonResponse({'code':400,'err_msg':'手机号不正确'})
    mobile_phone = form.cleaned_data['mobile_phone']
    if UserInfo.objects.filter(mobile_phone=mobile_phone).exists():
        return HttpResponse('手机号已存在！')
    # 返回响应
    return JsonResponse({'code':200,'err_msg':'ok'})