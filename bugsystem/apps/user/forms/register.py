from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.shortcuts import render
import re
from django_redis import get_redis_connection

# Create your views here.
from django import forms
from ..models import UserInfo
from utils.h256 import sha256_code


class RegisterModelForm(forms.ModelForm):
    mobile_phone = forms.CharField(label='手机号',validators=[RegexValidator(r'^1[3-9]\d{9}$', message='请输入正确的手机号')])
    password = forms.CharField(
        label='密码',
        min_length=6,
        max_length=256,
        error_messages={
            'min_length': "密码长度不能小于6个字符",
            'max_length': "密码长度不能大于256个字符"
        },
        widget=forms.PasswordInput()
    )

    confirm_password = forms.CharField(
        label='重复密码',
        min_length=6,
        max_length=256,
        error_messages={
            'min_length': "重复密码长度不能小于6个字符",
            'max_length': "重复密码长度不能大于256个字符"
        },
        widget=forms.PasswordInput())
    code = forms.CharField(label='验证码',widget=forms.TextInput())
    class Meta:
        model = UserInfo
        # fields = "__all__"
        fields = ['username','email','mobile_phone','password','confirm_password','code']


    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入%s' % field.label

    def clean_username(self):
        username = self.cleaned_data['username']
        exists = UserInfo.objects.filter(username=username).exists()
        if exists:
            raise ValidationError('用户名已存在')
            # self.add_error('username','用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        exists = UserInfo.objects.filter(email=email).exists()
        if exists:
            raise ValidationError('邮箱已存在')
        return email

    def clean_password(self):
        pwd = self.cleaned_data['password']
        # 加密 & 返回
        return sha256_code(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')

        confirm_pwd = sha256_code(self.cleaned_data['confirm_password'])

        if pwd != confirm_pwd:
            raise ValidationError('两次密码不一致')

        return confirm_pwd

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        exists = UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if exists:
            raise ValidationError('手机号已注册')
        return mobile_phone

    def clean_code(self):
        code = self.cleaned_data['code']

        # mobile_phone = self.cleaned_data['mobile_phone']

        mobile_phone = self.cleaned_data.get('mobile_phone')
        if not mobile_phone:
            return code

        conn = get_redis_connection()
        redis_code = conn.get(mobile_phone)
        if not redis_code:
            raise ValidationError('验证码失效或未发送，请重新发送')

        redis_str_code = redis_code.decode('utf-8')

        if code.strip() != redis_str_code:
            raise ValidationError('验证码错误，请重新输入')

        return code

# def register(request):
#     # connect_redis = get_redis_connection("default")
#     # connect_redis.set('a','12',ex=20)
#     if request.method == "GET":
#         form = RegisterModelForm()
#         return render(request,'html/register.html',{'form':form})