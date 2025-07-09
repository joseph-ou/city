import pymysql
from  .celery import app as celery_app

pymysql.install_as_MySQLdb()

__all__=['celery_app'] #表示这个模块只对外暴露 celery_app，其他导入的模块（如 pymysql）或方法（如 install_as_MySQLdb）不会被 import * 导入