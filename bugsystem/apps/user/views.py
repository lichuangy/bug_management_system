from django.shortcuts import render

# Create your views here.
from django import forms
from .models import UserInfo

class RegisterModelForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = "__all__"


def register(request):
    form = RegisterModelForm()
    return render(request,'register.html',{'form':form})