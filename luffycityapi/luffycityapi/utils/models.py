from django.db import models
# Create your models here.
# 父类 复用某些表格结构用
class BaseModel(models.Model):
    """
    公共模型
    保存项目中的所有模型的公共属性和公共方法的声明
    """

    orders = models.IntegerField(default=0, verbose_name='显示顺序')
    name = models.CharField(max_length=255, default='', verbose_name='标题/名称')

    is_deleted = models.BooleanField(default=False, verbose_name='是否默认被删除')
    # auto_now_add=True 当数据被创建时，以当前时间作为默认值写入当前字段
    # auto_now=True 当数据被更新时，以当前时间作为值写入当前字段
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_show = models.BooleanField(default=True, verbose_name='是否显示')

    class Meta:
        # 设置当前模型类并非真正的模型，而是一种保存公共代码的抽象模型类
        # 这种模型在数据迁移中不会被当做数据模型来创建数据表
        abstract = True  # 不创建表结构