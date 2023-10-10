import json
import random

from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
import re

from django.views.decorators.csrf import csrf_exempt
from django_redis import get_redis_connection

from .forms.account import RegisterModelForm,LoginForm,LoginSMSFORM
from .models import UserInfo
from django.db.models import Q
import re

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

    #发送短信模块
    import bugsystem.settings
    #获取模板编号
    template_id = bugsystem.settings.TENCENT_SMS_TEMPLATE.get(tpl)
    if template_id == bugsystem.settings.TENCENT_SMS_TEMPLATE.get('register'):
        # 校验数据库是否有手机号,如果有不让注册
        if UserInfo.objects.filter(mobile_phone=phone).exists():
            return JsonResponse({'code': 400, 'err_msg': ['手机号已存在']})
        print(template_id)
        from utils.tencent.sms import send_sms_single
        code = random.randrange(1000, 9999)
        sms = send_sms_single(phone, template_id, [code])
        if sms["result"] != 0:
            print('错误信息', sms["result"])
            return JsonResponse({"code": 400, "err_msg": "发送失败"})
        cnn = get_redis_connection('sms')
        cnn.set(phone, code, ex=120)
        return JsonResponse({"code": 200, 'msg': 'send sms successtify'})
    else:
        # 校验数据库是否有手机号,如果没有不让登录
        if not UserInfo.objects.filter(mobile_phone=phone).exists():
            return JsonResponse({'code':400,'err_msg':'手机号未注册，请先注册再登录！'})
        print(template_id)
        from utils.tencent.sms import send_sms_single
        code = random.randrange(1000,9999)
        sms = send_sms_single(phone,template_id,[code,2])
        if sms["result"] !=0:
            print('错误信息',sms["result"])
            return JsonResponse({"code":400,"err_msg":"发送失败"})
        cnn = get_redis_connection('sms')
        cnn.set(phone,code,ex=120)
        return JsonResponse({"code":200,'msg':'send sms successtify'})


def image_code(request):
    """生成图片验证码"""
    from utils.img_code.img_code import check_code

    image_object,code = check_code()
    print(code)
    # session存储验证码数据，设置过期时间
    request.session['image_code'] = code
    request.session.set_expiry(60)

    # 3. 写入内存(Python3) **在web项目开发中一般将生成的图片写入内存而不是写入文件保存起来**
    from io import BytesIO
    stream = BytesIO()
    image_object.save(stream, 'png')
    # stream.getvalue()
    return HttpResponse(stream.getvalue())



def register(request):
    if request.method == "GET":
        form = RegisterModelForm()
        return render(request, 'html/register.html', {'form': form})

    if request.method == "POST":
        form = RegisterModelForm(data=request.POST)
        print(len(request.POST.get('password')))
        if form.is_valid():
            instance = form.save()
            return JsonResponse({"code":200,"err_msg":"/login"})
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


def login_sms(request):
    """登录"""
    if request.method == 'GET':
        form = LoginSMSFORM()
        return render(request, 'html/login_sms.html', {'form': form})

    if request.method == "POST":
        form = LoginSMSFORM(request.POST)
        if form.is_valid():
            mobile_phone = form.cleaned_data['mobile_phone']
            user_object = UserInfo.objects.filter(Qusername=mobile_phone)
            request.session['user_id'] = user_object.id
            request.session.set_expiry(60*60*24*14)
            return JsonResponse({"code":200,"err_msg":"index"})

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
            return JsonResponse({"code": 400, "err_msg": error_msg})

def login(request):
    if request.method=='GET':
        form = LoginForm(request)
        return render(request,'html/login.html',{'form':form})
    form = LoginForm(request,data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        pwd = form.cleaned_data['password']
        user_object = UserInfo.objects.filter(Q(username=username, password=pwd)|Q(email=username, password=pwd)).first()
        if not user_object:
            form.add_error('username','用户名或密码错误')
        else:
            request.session['user_id'] = user_object.id
            request.session.set_expiry(60*60*24*14)
            return redirect('index')
    return render(request,'html/login.html',{'form':form})


def index(request):
    return render(request,'html/index.html')


def logout(request):
    request.session.flush()
    return redirect('index')