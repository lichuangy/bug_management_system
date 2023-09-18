from django.core.validators import RegexValidator
from django.shortcuts import render
import re
from django_redis import get_redis_connection

# Create your views here.
from django import forms
from ..models import UserInfo

class RegisterModelForm(forms.ModelForm):
    mobile_phone = forms.CharField(label='手机号',validators=[RegexValidator(r'^1[3-9]\d{9}$', message='请输入正确的手机号')])
    password = forms.CharField(label='密码',widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='密码',widget=forms.PasswordInput)
    code = forms.CharField(label='验证码')
    class Meta:
        model = UserInfo
        fields = "__all__"
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入%s' % field.label

def register(request):
    # connect_redis = get_redis_connection("default")
    # connect_redis.set('a','12',ex=20)
    form = RegisterModelForm()
    return render(request,'html/register.html',{'form':form})