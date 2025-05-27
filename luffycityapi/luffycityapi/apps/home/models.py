# from django.db import models

# from luffycityapi.utils.models import models,BaseModel
from models import models,BaseModel

# # Create your models here.
# #父类 复用某些表格结构用
# class BaseModel(models.Model):
#     """
#     公共模型
#     保存项目中的所有模型的公共属性和公共方法的声明
#     """
#     
#     orders=models.IntegerField(default=0,verbose_name='显示顺序')
#     name = models.CharField(max_length=255,default='',verbose_name='标题/名称')
#     
#     is_deleted=models.BooleanField(default=False,verbose_name='是否默认被删除')
#     # auto_now_add=True 当数据被创建时，以当前时间作为默认值写入当前字段
#     # auto_now=True 当数据被更新时，以当前时间作为值写入当前字段
#     created_time=models.DateTimeField(auto_now_add=True,verbose_name='添加时间')
#     updated_time=models.DateTimeField(auto_now=True,verbose_name='更新时间')
#     is_show=models.BooleanField(default=True,verbose_name='是否显示')
#     
#     class Meta:
#         # 设置当前模型类并非真正的模型，而是一种保存公共代码的抽象模型类
#         # 这种模型在数据迁移中不会被当做数据模型来创建数据表
#         abstract = True #不创建表结构


class Nav(BaseModel):
    '''导航菜单'''
    # 字段选项
    # 模型对象.<字段名>  ---> 实际数据
    # 模型对象.get_<字段名>_display()  --> 文本提示
    POSITION_OPTION=(
        (0,"头部导航"),
        (1,"底部导航"),
    )
    

    link=models.CharField(max_length=255,verbose_name='导航链接')
    is_http=models.BooleanField(default=False,verbose_name='是否是外部链接')
    position=models.IntegerField(choices=POSITION_OPTION,default=0,verbose_name='导航位置')

    
    class Meta:
        db_table = "lf_nav"
        verbose_name = "导航菜单"
        verbose_name_plural = verbose_name


class Banner(BaseModel):
    '''轮播图'''
    image=models.ImageField(upload_to='banner/%Y/%m',verbose_name='轮播图地址')
    link=models.CharField(max_length=500,verbose_name='链接地址')
    note=models.CharField(max_length=150,verbose_name='备注信息')
    is_http=models.BooleanField(default=False,verbose_name='是否外部链接', help_text="站点链接地址：http://www.baidu.com/book<br>站点链接地址：/book/")

    class Meta:
        db_table = "lf_banner"
        verbose_name = "轮播广告"
        verbose_name_plural = verbose_name


