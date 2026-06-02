from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', '管理员'),
        ('project_manager', '项目经理'),
        ('staff', '普通员工'),
    ]
    
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='联系电话')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff', verbose_name='角色')
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
