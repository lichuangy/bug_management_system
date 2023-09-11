from django.db import models

# Create your models here.
from django.db import models

# Create your models here.


class UserInfo(models.Model):
    username = models.CharField(max_length=32,verbose_name='用户名')
    email = models.EmailField(verbose_name='邮箱',max_length=32)
    mobile_phone = models.CharField(verbose_name='手机号',max_length=11)
    password = models.CharField(verbose_name='密码',max_length=32)