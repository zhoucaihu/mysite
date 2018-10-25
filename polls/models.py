from django.db import models

# Create your models here.

class Inter(models.Model):
    name = models.CharField(max_length=32, verbose_name='模型名')
    interface  = models.CharField(max_length=32, verbose_name='接口名')
    supplier = models.CharField(max_length=32, verbose_name='供应商')
    is_model = models.BooleanField(verbose_name='是否模型')
    rely = models.ManyToManyField('self',blank=True,null=True, verbose_name='依赖接口')
    inter = models.ManyToManyField('Qparam', verbose_name='参数')

    def __str__(self):
        return self.name

class Qparam(models.Model):
    name = models.CharField(max_length=32, verbose_name='参数名')
    param = models.CharField(max_length=32, verbose_name='参数字段')

    def __str__(self):
        return self.name

