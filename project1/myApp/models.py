from django.db import models

# Create your models here.
class Departments(models.Model):
    dname = models.CharField(max_length=20)
    dboynum = models.IntegerField()
    dgirlnum = models.IntegerField()
    class Meta:
        db_table = 'departments'
        ordering =['id']
    def __str__(self):
        return self.dname
    #定义一个类方法创建对象
    #@classmethod
   # def createEmployee(cls,name,age,gender):
       # ee = cls(ename = name,eage = age,egender = gender)
        #return ee

class Employees(models.Model):
    ename = models.CharField(max_length=20)
    eage = models.IntegerField()
    egender = models.CharField(max_length=20)
    ephoto = models.ImageField(upload_to='static/media')
    epart = models.ForeignKey("Departments", on_delete=models.CASCADE)
    class Meta:
        db_table = 'employees'
        ordering =['id']
    #定义一个类方法创建对象
    @classmethod
    def createEmployee(cls,name,age,gender,part,photo):
        ee = cls(ename = name,eage = age,egender = gender,epart_id = part,ephoto= photo )
        return ee

