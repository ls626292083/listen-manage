from django.shortcuts import render
import xlwt
from io import BytesIO
from django.shortcuts import redirect
# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from .models import Employees
import os
from django.conf import settings
from django import forms

def allpage(request):
    #获取员表所有员工数据
    employeesList = Employees.objects.all()
    # 将数据传递给模板,模板在渲染页面，将渲染好的页面返回给游览器
    #return render(request, 'myApp/all1.html')
    return render(request,'myApp/all.html',{'ees':employeesList})

def addpage(request):
    return render(request, 'myApp/add.html')

def addees(request):
    #return redirect('/all')
    name = request.POST['eName']
    age = request.POST['eAge']
    gender =request.POST['eGender']
    part = request.POST['ePart']

    photofname = request.FILES['ePhoto']
    fname = os.path.join(settings.MEDIA_ROOT,photofname.name)
    with open(fname,'wb') as pic:
        for info in photofname.chunks():
            pic.write(info)

    photo = os.path.join("/static/media/", photofname.name)
    #a= type(photo)
    #print(type(name))
    #print(a)
    #print(name,age,gender,photofname.name)
    #ee = cls(ename=name, eage=age, egender=gender, ephoto=photo, epart_id=part)
    ee = Employees.createEmployee(name,age,gender,part,photo)
    ee.save()
    return HttpResponseRedirect('/all')
    #return render(request, 'myApp/add.html')
    #return HttpResponse("qqq")

def search(request):
    name = request.GET['q']
    ee=Employees.objects.filter(ename=name)
    return render(request, 'myApp/all.html', {'ees': ee})
    #print(ee)
    #return HttpResponseRedirect('/all')
    #return render(request, 'myApp/add.html')
    #return HttpResponse("qqq")

def delete(request,eid):
    Employees.objects.filter(id=eid).delete()
    return HttpResponseRedirect('/all')
    #return HttpResponse("qqq")

def getid(request,eid):
    ee=Employees.objects.filter(id=eid)
    #print(ee)
    content={'data':ee}
    #print(content)
    return render(request,'myApp/update.html', content)
    #return HttpResponse("qqq")

def update(request):
    id=request.POST['eid']
    #print(request.POST)
    name=request.POST['eName']
    age = request.POST['eAge']
    gender =request.POST['eGender']
    part = request.POST['ePart']
    photofname = request.FILES['ePhoto']
    fname = os.path.join(settings.MEDIA_ROOT, photofname.name)
    with open(fname, 'wb') as pic:
        for info in photofname.chunks():
            pic.write(info)
    photo = os.path.join("/static/media/", photofname.name)
    Employees.objects.filter(id=id).update(ename=name,eage=age,egender=gender,epart_id=part,ephoto=photo)
    return HttpResponseRedirect('/all')
    #return HttpResponse("qqq")


def index(request):
    return render(request, 'myApp/1.html')

def educe(request):
    #设置HTTPResponse的类型
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename = order.xls'
    #创建一个文件对象
    wb = xlwt.Workbook(encoding = 'utf8')
    #创建一个sheet对象
    sheet = wb.add_sheet('order-sheet')
    #设置文件头的样式
    style_heading = xlwt.easyxf("""
            font:
                name Arial,
                colour_index white,
                bold on,
                height 0xA0;
            align:
                wrap off,
                vert center,
                horiz center;
            pattern:
                pattern  solid,
                fore-colour 0x19;
            borders:
                left THIN,
                right THIN,
                top THIN,
                bottom THIN;
            
    """)
    #写入文件标题：
    sheet.write(0, 0, '姓名', style_heading)
    sheet.write(0, 1, '年龄', style_heading)
    sheet.write(0, 2, '性别', style_heading)
    sheet.write(0, 3, '部门', style_heading)
    #写入数据
    data_row = 1
    #查询
    for i in Employees.objects.all().select_related('epart'):
        sheet.write(data_row, 0, i.ename)
        sheet.write(data_row, 1, i.eage)
        sheet.write(data_row, 2, i.egender)
       # if(i.epart_id == 1):
         #   sheet.write(data_row, 3, "时间管理部门")
       # else:
            #sheet.write(data_row, 3, "人力资源部门")
        sheet.write(data_row, 3, i.epart.dname)
        data_row = data_row + 1
    #写错到IO
    output = BytesIO()
    wb.save(output)
    #重新定位到开始
    output.seek(0)
    response.write(output.getvalue())
    return response
    #return HttpResponseRedirect('/all')
    #pass
