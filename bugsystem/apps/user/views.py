import json
import random

from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
import re
from django_redis import get_redis_connection

from .forms.register import RegisterModelForm
from .models import UserInfo
import re

# Create your views here.


def register(request):
        if request.method == "GET":
            form = RegisterModelForm()
            return render(request, 'html/register.html', {'form': form})

        if request.method == "POST":
            form = RegisterModelForm(data=request.POST)
            if form.is_valid():
                return JsonResponse({"code":200,"err_msg":"/logoin"})
            else:
                # form.errors 中存储了错误信息
                errors = form.errors.get_json_data()

                error_msg = []
                # 遍历错误信息
                for k, v in errors.items():
                    # v 是个列表,取第一个元素
                    error_msg.append(v[0]['message'])
                    # error_msg = v[0]['message']
                    # error_msg 就是表单字段验证错误的提示信息
                    print(error_msg)
                return JsonResponse({"code":400,"err_msg":error_msg})
    #
    # print(request.POST)
    # return JsonResponse({'code':200})
    # form = RegisterModelForm(data=request.POST)
    # if form.is_valid():
    #     print(form.cleaned_data)
    # else:
    #     print(form.errors)
    # return JsonResponse({})






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
        return JsonResponse({'code':400,'err_msg':['参数缺失']})
    # 验证手机号是否合规
    # 方法一
    # form = RegisterModelForm(data={'mobile_phone':phone})
    # if form.is_valid():
    #     return JsonResponse({'code':400,'err_msg':'手机号不正确'})
    # # phone = form.cleaned_data['mobile_phone']
    # 方法二
    if not re.match(r'1[3-9]\d{9}$',phone):
        return JsonResponse({'code': 400, 'err_msg': ['手机号不正确']})
    #校验数据库是否有手机号
    if UserInfo.objects.filter(mobile_phone=phone).exists():
        return JsonResponse({'code': 400, 'err_msg': ['手机号已存在']})
    #发送短信模块
    import bugsystem.settings
    template_id = bugsystem.settings.TENCENT_SMS_TEMPLATE.get(tpl)
    print(template_id)
    from utils.tencent.sms import send_sms_single
    code = random.randrange(1000,9999)
    sms = send_sms_single(phone,template_id,[code,])
    if sms["result"] !=0:
        print('错误信息',sms["result"])
        return JsonResponse({"code":400,"err_msg":"发送失败"})
    cnn = get_redis_connection('sms')
    cnn.set(phone,code,ex=120)
    return JsonResponse({"code":200,'msg':'send sms successtify'})

