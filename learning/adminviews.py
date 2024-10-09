import base64
from datetime import timezone
from django.shortcuts import render ,get_object_or_404 , redirect

from lms_main import settings
from lms_main.settings import BASE_DIR 
from . models import *
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from django.urls import reverse


# def sidenavbar(request):
   
#     data = Schools.objects.filter(usernumber=request.user.id).first()

#     plans=Teachers.objects.filter(schoolid=data)
#     std=Student.objects.filter(schoolid=data)
#     teacher_count = Teachers.objects.filter(schoolid__usernumber=request.user.id).count()
#     student_count=Student.objects.filter(schoolid__usernumber=request.user.id).count()
  


#     am=admin_main.objects.all()
#     k=MenuItem.objects.filter(parent_category=None)
#     return render(request,'admin-template/adminsidebar.html',{'student_count':student_count,'teacher_count':teacher_count,'std':std,'plans':plans,'k':k,'am':am})

from django.utils import timezone
from django.shortcuts import render

def sidenavbar(request): 
    all_schools = Schools.objects.filter(usernumber=request.user.id).first() 
    pending_leave_count = all_schools.leave_set.filter(is_status=0, read=0).count()
    k1 = all_schools.leave_set.filter(read=0) 
    k2 = all_schools.leave_set.filter(user_type=2, read=0)  
    k4 = all_schools.leave_set.filter(user_type=3, read=0)
    
    k = MenuItem.objects.filter(parent_category=None)
    teachers_count, teaching_staff_count, non_teaching_staff_count = get_teachers_count(request) 
    student_count, classes_count = get_student_class_count(request) 
    current_time = timezone.now()  # Get the current time in UTC

    context = {
        'teachers_count': teachers_count,
        'teaching_staff_count': teaching_staff_count,
        'non_teaching_staff_count': non_teaching_staff_count,
        'k': k,
        'k4': k4,
        'k2': k2,
        "k1": k1,
        'pending_leave_count': pending_leave_count,
        'student_count': student_count,
        'classes_count': classes_count,
        'current_time': current_time,
        'registered_plan': all_schools.plan_id.name if all_schools else None,
    }
    return render(request, 'admin-template/adminsidebar.html', context)





def Leave_Management(request):
    k=MenuItem.objects.filter(parent_category=None)

    j=leavemanagement.objects.all()
    return render(request,'admin-template/Leave Management.html',{'k':k,'j':j})


def Leave_Management2(request):
    k1=leavestype.objects.all()
    k=MenuItem.objects.filter(parent_category=None)

    if request.method=="POST":
        leavetype=request.POST['leavetype']
        Noofleaves=request.POST['Noofleaves']
        leavecategory=request.POST['leavecategory']
        k3=leavestype(leavetype=leavetype,Noofleaves=Noofleaves,leavecategory=leavecategory)
        k3.save()
    return render(request,'admin-template/Leave Management2.html',{'k1':k1,'k':k})



def Leave_type_edit(request,id):
    if request.method=="GET":
        k=MenuItem.objects.filter(parent_category=None)
        k1=leavestype.objects.get(id=id)
        return render(request,"admin-template/Leave_type_update.html",{'k1':k1,'k':k})

def Leave_type_update(request,id):
    if request.method=="POST":
       
        leavetype=request.POST['leavetype']
        Noofleaves= request.POST['Noofleaves']
        leavecategory= request.POST['leavecategory']

    
        k=leavestype.objects.get(id=id)
       
        k.leavetype=leavetype
        k.Noofleaves=Noofleaves
        k.leavecategory=leavecategory
        

        k.save()
        return redirect("/Leave_Management2/")
    return render(request,"admin-template/Leave_type_update.html")


def Leave_type_delete(request,id):
    if request.method=="GET":
        k=leavestype.objects.get(id=id)
        k.delete()
        return redirect("/Leave_Management2/")
    # return render(request,"admin-template/leavedatadelete.html")  

def admin_attendance(request):
    j=Attendancemenu.objects.all()
    k=MenuItem.objects.filter(parent_category=None)

    return render(request,'admin-template/teacher_attendance.html',{'j':j,'k':k})   

def Teacher_leaves_view(request):
    k=MenuItem.objects.filter(parent_category=None)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
    p=leave.objects.filter(user_type=2)
    k2=leave.objects.filter(user_type=2,read=0)

    pending_leave_count = leave.objects.filter(is_status=0,user_type=2,read=0).count()

    k3=leavestype.objects.all()
    return render(request,'admin-template/view_teacher_apply_leave.html',{'k2':k2,'p':p,'k':k,'k3':k3,'pending_leave_count':pending_leave_count})     

def Student_leaves_view(request):
    k=MenuItem.objects.filter(parent_category=None)    
    p=leave.objects.filter(user_type=3)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
    k4=leave.objects.filter(user_type=3,read=0)
    pending_leave_count = leave.objects.filter(is_status=0,user_type=3,read=0).count()

    k3=leavestype.objects.all()

    # items_per_page = 1 


    # paginator = Paginator(k4, items_per_page)

    # page = request.GET.get('page')

    # try:
    #     k4 = paginator.page(page)
    # except PageNotAnInteger:
    #     k4 = paginator.page(1)
    # except EmptyPage:
    #     k4 = paginator.page(paginator.num_pages)

    return render(request,'admin-template/view_student_apply_leave.html',{'p':p,'k':k,'k3':k3,'k4':k4,'pending_leave_count':pending_leave_count})

def leave_approve(request,id):
    k2=leave.objects.get(id=id)
    k2.is_status=1
    k2.save()
    return HttpResponseRedirect(reverse("Teacher_leaves_view"))

def leave_disapprove(request,id):
    k2=leave.objects.get(id=id)
    k2.is_status=2
    k2.save()

    return HttpResponseRedirect(reverse("Teacher_leaves_view"))


def leave_approve1(request,id):
    k2=leave.objects.get(id=id)
    k2.is_status=1
    k2.save()
    return HttpResponseRedirect(reverse("Student_leaves_view"))

def leave_disapprove1(request,id):
    k2=leave.objects.get(id=id)
    k2.is_status=2
    k2.save()

    return HttpResponseRedirect(reverse("Student_leaves_view"))


def mark_all_as_read(request):
    leave.objects.all().update(read=True)
    return HttpResponseRedirect('/sidenavbar') 

    
    
def mark_as_read(request, leave_id):
    leave_obj = get_object_or_404(leave, id=leave_id)
    leave_obj.read = True
    leave_obj.save()
    return HttpResponseRedirect('/Teacher_leaves_view')
    
def mark_as_read1(request, leave_id):
    leave_obj = get_object_or_404(leave, id=leave_id)
    leave_obj.read = True
    leave_obj.save()
    return HttpResponseRedirect('/Student_leaves_view')     

from .models import teacherattendance
def Teacher_Attendance_display(request):
    k=MenuItem.objects.filter(parent_category=None)

    k1=teacherattendance.objects.all()
    return render(request, "admin-template/Teacher_Attendance_display.html",{'k':k,'k1':k1})


def create_Teacher_shifts(request):

    k4=different_shifts.objects.all()
    k6=Teachers.objects.all()
    if request.method=="POST":
        name=request.POST.get('shift_name')
        weekly_off=request.POST.get('weekly_off')
        in_time=request.POST.get('in_time')
        late_mark_time=request.POST.get('late_mark_time')
        out_time=request.POST.get('out_time')
        half_daytime=request.POST.get('half_daytime')
        first_name=request.POST.get('facult_name')
        shift_instance=get_object_or_404(different_shifts,name=name)
        name_instance=get_object_or_404(Teachers,first_name=first_name)
        k=Teacher_Shifts(shift_name=shift_instance,weekly_off=weekly_off,in_time=in_time,late_mark_time=late_mark_time,out_time=out_time,half_daytime=half_daytime,facult_name=name_instance)
        k.save()
    return render(request, "admin-template/create_Teacher_shifts.html",{'k4':k4,'k6':k6,})
          
              

def create_Teacher_shifts_display(request):
    if request.method=="GET":
        k=Teacher_Shifts.objects.all()
        return render(request,'admin-template/create_Teacher_shifts_display.html',{'k':k})
    

def create_Teacher_shifts_edit(request,id):
    if request.method=="GET":
        k=Teacher_Shifts.objects.get(id=id)
        return render(request,"admin-template/create_Teacher_shifts_edit.html",{'k':k})



def create_Teacher_shifts_update(request,id):
    if request.method=="POST":       
        shift_name=request.POST['shift_name']
        weekly_off= request.POST['weekly_off'] 
        in_time= request.POST.get('in_time')   
        late_mark_time= request.POST.get('late_mark_time')    
        out_time= request.POST.get('out_time')
        half_daytime= request.POST.get('half_daytime')  
        facult_name= request.POST['facult_name']    
        k=Teacher_Shifts.objects.get(id=id)       
        k.shift_name=shift_name
        k.weekly_off=weekly_off
        k.in_time=in_time
        k.late_mark_time=late_mark_time
        k.out_time=out_time
        k.half_daytime=half_daytime
        k.facult_name=facult_name
        k.save()
        return redirect("/create_Teacher_shifts_display/")
    return render(request,"admin-template/create_Teacher_shifts_edit.html")



def create_Teacher_shifts_delete(request,id):
    if request.method=="GET":
        k=Teacher_Shifts.objects.get(id=id)
        k.delete()
        return HttpResponse("data is deleted")
    return render(request,"admin-template/create_Teacher_shifts_delete.html")  

from django.shortcuts import get_object_or_404

from django.shortcuts import get_object_or_404
from django.contrib import messages 

def compose_message12(request):  
    k=MenuItem.objects.filter(parent_category=None) 
    scc=Schools.objects.filter(usernumber=request.user.id).first() 
    k1=Teachers.objects.filter(schoolid=scc) 
    k3=Student.objects.filter(schoolid=scc) 
    k5=Student.objects.filter(student_class=1,schoolid=scc) 
    k6=Student.objects.filter(student_class=2,schoolid=scc) 
    k7=Student.objects.filter(student_class=3,schoolid=scc) 
    k8=Student.objects.filter(student_class=4,schoolid=scc) 
    k9=Student.objects.filter(student_class=5,schoolid=scc) 
    k10=Student.objects.filter(student_class=6,schoolid=scc) 
    k11=Student.objects.filter(student_class=7,schoolid=scc) 
    k12=Student.objects.filter(student_class=8,schoolid=scc) 
    k4=Student.objects.filter(student_class=9,schoolid=scc) 
 
    k13=Student.objects.filter(student_class=10,schoolid=scc) 
    k14=Student.objects.filter(student_class=11,schoolid=scc)  
    k15=Student.objects.filter(student_class=12,schoolid=scc)        
 
    if request.method == "POST":  
        MessageType = request.POST.get('MessageType') 
        Message = request.POST.get('Message')    

        if MessageType and Message:    
            if 'all_teachers' in request.POST: 
                for teacher in k1:              
                   k2 = compose_message(teachername=teacher,schoolid=scc, MessageType=MessageType, Message=Message)
                   k2.save()    


         
            if 'all_students' in request.POST:   
                for student in k3:     
                    k2 = compose_message(studentname=student,schoolid=scc, MessageType=MessageType, Message=Message)
                    k2.save()  


                
                    
            if '1st_class' in request.POST:      
                for student in k5:   
                    k2 = compose_message(studentname=student,schoolid=scc, MessageType=MessageType, Message=Message)
                    k2.save()   
                    


            if '2nd_class' in request.POST:   
                for student in k6:  
                    k2 = compose_message(studentname=student,schoolid=scc, MessageType=MessageType, Message=Message)
                    k2.save()               



            if '3rd_class' in request.POST:   
                for student in k7:  
                    k2 = compose_message(studentname=student,schoolid=scc, MessageType=MessageType, Message=Message)
                    k2.save()   


    
            if '4th_class' in request.POST:   
                for student in k8:  
                    k2 = compose_message(studentname=student,schoolid=scc, MessageType=MessageType, Message=Message)
                    k2.save()   



            if '5th_class' in request.POST:   
                for student in k9:  
                    k2 = compose_message(studentname=student,schoolid=scc, MessageType=MessageType, Message=Message)
                    k2.save()   


        
            if '6th_class' in request.POST:   
                for student in k10:  
                    k2 = compose_message(studentname=student,schoolid=scc, MessageType=MessageType, Message=Message)
                    k2.save()  

            
            if '7th_class' in request.POST:   
                for student in k11:  
                    k2 = compose_message(studentname=student,schoolid=scc, MessageType=MessageType, Message=Message)
                    k2.save() 

            
            if '8th_class' in request.POST:   
                for student in k12:  
                    k2 = compose_message(studentname=student,schoolid=scc, MessageType=MessageType, Message=Message)
                    k2.save()  


            if '9th_class' in request.POST:   
                for student in k4:   
                    k2 = compose_message(studentname=student,schoolid=scc, MessageType=MessageType, Message=Message)
                    k2.save() 
        
            
            if '10th_class' in request.POST:   
                for student in k13:   
                    k2 = compose_message(studentname=student,schoolid=scc, MessageType=MessageType, Message=Message)
                    k2.save()                                            
            

        
            if '11th_class' in request.POST:   
                for student in k14:  
                    k2 = compose_message(studentname=student,schoolid=scc, MessageType=MessageType, Message=Message)
                    k2.save()    

                
        
            if '12th_class' in request.POST:                     
                for student in k15:                                                     
                    k2 = compose_message(studentname=student,schoolid=scc, MessageType=MessageType, Message=Message)
                    k2.save()                                        
            messages.success(request,"Data is inserted for selected categories")
            return redirect('/compose_message12')  
        else:
            messages.error(request," Please Select  the Type Field")                                         
 
        

    return render(request, 'admin-template/composemessage.html', {'k': k, 'k1': k1, 'k3': k3,'k4':k4,'k5':k5,'k6':k6,'k7':k7,'k8':k8,'k9':k9,'k10':k10,'k11':k11,'k12':k12,'k13':k13,'k14':k14,'k15':k15})  





def teachdata(request):
    data = Schools.objects.filter(usernumber=request.user.id).first()
    data1=data.id
    plans=Teachers.objects.filter(schoolid=data1)
    return render(request,'admin-template/teacherdata.html',{'plans':plans})



def teachercount(request):
    k=MenuItem.objects.filter(parent_category=None)  
    sch = Schools.objects.filter(usernumber=request.user.id).first()
    plans = Teachers.objects.filter(schoolid=sch)
    teca=Teacher_Class_sub.objects.all()
    # teacher_class_subs = Teacher_Class_sub.objects.filter(teacher__in=teachers).order_by('teacher__id')
    # grouped_data = []

    # for teacher, entries in groupby(teacher_class_subs, key=attrgetter('teacher')):
    #     entries_by_subject = {}
    #     for entry in entries:
    #         subject_name = entry.subject.name
    #         if subject_name not in entries_by_subject:
    #             entries_by_subject[subject_name] = []
    #         entries_by_subject[subject_name].append(entry)

    #     grouped_data.append({
    #         'teacher': teacher,
    #         'entries_by_subject': entries_by_subject,
    #     })

    return render(request, 'admin-template/count.html',{'plans': plans,'k':k,'teca':teca})



def alldata(request):
    data = Schools.objects.filter(usernumber=request.user.id).first()
    plans=Student.objects.filter(schoolid=data)
    k = MenuItem.objects.filter(parent_category=None)
    return render(request, 'admin-template/all.html', {'plans':plans,'k':k})




from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models.functions import Cast, Length
from django.db.models import IntegerField
from .models import Schools, cls_name, Subject, Teachers, Teacher_Class_sub, MenuItem

def assign_subjects_classes(request):
    k = MenuItem.objects.filter(parent_category=None)
    sch = Schools.objects.filter(usernumber=request.user.id).first()
    school_count = Schools.objects.filter(usernumber=request.user.id).count()

    teachers = Teachers.objects.filter(schoolid=sch)
    classes = cls_name.objects.filter(school_id=sch).order_by(Cast('classes', output_field=IntegerField()))  
    message = ''

    if request.method == 'POST':
        teacher_id = request.POST['teacher']
        subject_id = request.POST['subject']
        class_ids = request.POST.getlist('classes')

        teacher = Teachers.objects.get(id=teacher_id)
        subject = Subject.objects.get(id=subject_id)

        for class_id in class_ids:
            class_name = get_object_or_404(cls_name, id=class_id)
            Teacher_Class_sub.objects.create(
                teacher=teacher,
                class_name=class_name,
                subject=subject,
                school_id=sch
            )
        message = 'Successfully Submitted.'

    return render(request, 'admin-template/assign_subjects_classes.html', {
        'teachers': teachers,
        'classes': classes,
        'message': message,
        'k': k,
        'school_count': school_count
    })

def get_subjects_for_class(request, class_id):
    subjects = Subject.objects.filter(class_name__id=class_id).order_by('name')  
    data = [{'id': subject.id, 'name': subject.name} for subject in subjects]
    return JsonResponse(data, safe=False)# views.py
   
from itertools import groupby  
from operator import attrgetter
from django.shortcuts import render
from .models import Teacher_Class_sub, Teachers  

def view_teacher_sub_class(request):
    k=MenuItem.objects.filter(parent_category=None)  
    sch = Schools.objects.filter(usernumber=request.user.id).first()
    teachers = Teachers.objects.filter(schoolid=sch)
    
    teacher_class_subs = Teacher_Class_sub.objects.filter(teacher__in=teachers).order_by('teacher__id')
    grouped_data = []

    # Group by teacher
    for teacher, entries in groupby(teacher_class_subs, key=attrgetter('teacher')):
        # Group entries by subject name
        entries_by_subject = {}
        for entry in entries:
            subject_name = entry.subject.name
            if subject_name not in entries_by_subject:
                entries_by_subject[subject_name] = []
            entries_by_subject[subject_name].append(entry)

        grouped_data.append({
            'teacher': teacher,
            'entries_by_subject': entries_by_subject,
        })

    return render(request, 'admin-template/view_teacher_sub_class.html',{'grouped_data': grouped_data,'k':k})

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models.functions import Cast, Length
from django.db.models import IntegerField
from .models import Schools, cls_name, Subject, Teachers, Teacher_Class_sub, MenuItem

def assign_subjects_classes(request):
    k = MenuItem.objects.filter(parent_category=None)
    sch = Schools.objects.filter(usernumber=request.user.id).first()
    school_count = Schools.objects.filter(usernumber=request.user.id).count()

    teachers = Teachers.objects.filter(schoolid=sch)
    classes = cls_name.objects.filter(school_id=sch).order_by(Cast('classes', output_field=IntegerField()))  
    message = ''

    if request.method == 'POST':
        teacher_id = request.POST['teacher']
        subject_id = request.POST['subject']
        class_ids = request.POST.getlist('classes')

        teacher = Teachers.objects.get(id=teacher_id)
        subject = Subject.objects.get(id=subject_id)

        for class_id in class_ids:
            class_name = get_object_or_404(cls_name, id=class_id)
            Teacher_Class_sub.objects.create(
                teacher=teacher,
                class_name=class_name,
                subject=subject,
                school_id=sch
            )
        message = 'Successfully Submitted.'

    return render(request, 'admin-template/assign_subjects_classes.html', {
        'teachers': teachers,
        'classes': classes,
        'message': message,
        'k': k,
        'school_count': school_count
    })

def get_subjects_for_class(request, class_id):
    subjects = Subject.objects.filter(class_name__id=class_id).order_by('name')  
    data = [{'id': subject.id, 'name': subject.name} for subject in subjects]
    return JsonResponse(data, safe=False)


from django.shortcuts import render, redirect
from django.db.models import IntegerField
from django.db.models.functions import Cast
from.models import Schools, cls_name, Subject, MenuItem

from django.shortcuts import render
from django.db.models import IntegerField
from django.db.models.functions import Cast
from django.shortcuts import render, redirect
from django.db.models import IntegerField
from django.db.models.functions import Cast
from.models import Schools, cls_name, Subject, MenuItem

def addsubject(request):
    k = MenuItem.objects.filter(parent_category=None)  
    schools = Schools.objects.filter(usernumber=request.user.id).first()
    classes = cls_name.objects.filter(school_id=schools).order_by(Cast('classes', output_field=IntegerField())) 
    existing_subjects = Subject.objects.filter(school_id=schools.id).select_related('school_id')
    message = ''

    if request.method == "POST":
        name = request.POST.get('name')
        existing_subject_id = request.POST.get('existing_subject')
        selected_class_ids = request.POST.getlist('classes')

        if not existing_subject_id and (not name or not selected_class_ids):
            message = 'Name and at least one class must be provided.'
        else:
            if name and Subject.objects.filter(name=name, school_id=schools.id).exists():
                message = f'Subject "{name}" already exists.'
            else:
                if existing_subject_id:
                    subject = Subject.objects.get(id=existing_subject_id)
                else:
                    subject = Subject.objects.create(name=name, school_id=schools)
                
                for class_id in selected_class_ids:
                    selected_class = cls_name.objects.get(id=class_id)
                    subject.class_name.add(selected_class)
                
                message = 'Added Subject Successfully.'

    return render(request, 'admin-template/addSubject.html', {'message': message, 'classes': classes, 'k': k, 'existing_subjects': existing_subjects})



from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models.functions import Cast, Length
from django.db.models import IntegerField
from .models import Schools, cls_name, Subject, Teachers, Teacher_Class_sub, MenuItem

def assign_subjects_classes(request):
    k = MenuItem.objects.filter(parent_category=None)
    sch = Schools.objects.filter(usernumber=request.user.id).first()
    school_count = Schools.objects.filter(usernumber=request.user.id).count()

    teachers = Teachers.objects.filter(schoolid=sch)
    classes = cls_name.objects.filter(school_id=sch).order_by(Cast('classes', output_field=IntegerField()))  
    message = ''

    if request.method == 'POST':
        teacher_id = request.POST['teacher']
        subject_id = request.POST['subject']
        class_ids = request.POST.getlist('classes')

        teacher = Teachers.objects.get(id=teacher_id)
        subject = Subject.objects.get(id=subject_id)

        for class_id in class_ids:
            class_name = get_object_or_404(cls_name, id=class_id)
            Teacher_Class_sub.objects.create(
                teacher=teacher,
                class_name=class_name,
                subject=subject,
                school_id=sch
            )
        message = 'Successfully Submitted.'

    return render(request, 'admin-template/assign_subjects_classes.html', {
        'teachers': teachers,
        'classes': classes,
        'message': message,
        'k': k,
        'school_count': school_count
    })

def get_subjects_for_class(request, class_id):
    subjects = Subject.objects.filter(class_name__id=class_id).order_by('name')  
    data = [{'id': subject.id, 'name': subject.name} for subject in subjects]
    return JsonResponse(data, safe=False)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def addclass(request):
    k = MenuItem.objects.filter(parent_category=None)  
    school = Schools.objects.filter(usernumber=request.user.id).first()
    message = ''
    if request.method == "POST":
        classes = request.POST.get('classes')
        if cls_name.objects.filter(classes=classes, school_id=school).exists():
            message = 'Error: This class already exists.'
        else:
            k1 = cls_name(classes=classes)
            k1.school_id = school
            k1.save()
            message = 'Added Class Successfully.'

    return render(request, 'admin-template/addClass.html', {'message': message, 'k': k})
def class_wise(request):
    k=MenuItem.objects.filter(parent_category=None)

    second_table_data = Schools.objects.filter(usernumber=request.user.id)
    third_table_data = Student.objects.filter(schoolid__in=second_table_data)
    
    class_1_to_4_students = third_table_data.filter(className__in=['1', '2', '3', '4'])
    class_5_to_8_students = third_table_data.filter(className__in=['5', '6', '7', '8'])
    class_9_to_12_students = third_table_data.filter(className__in=['9', '10', '11', '12'])
    
    count_class_1_to_4 = class_1_to_4_students.count()
    count_class_5_to_8 = class_5_to_8_students.count()
    count_class_9_to_12 = class_9_to_12_students.count()
    
    return render(request, 'admin-template/classes_wise.html', {'k':k,'class_1_to_4_students': class_1_to_4_students,'class_5_to_8_students': class_5_to_8_students,'class_9_to_12_students': class_9_to_12_students,'count_class_1_to_4': count_class_1_to_4,'count_class_5_to_8': count_class_5_to_8,'count_class_9_to_12': count_class_9_to_12})

def classes1to4(request):
    k=MenuItem.objects.filter(parent_category=None)
    second_table_data = Schools.objects.filter(usernumber=request.user.id)
    third_table_data = Student.objects.filter(schoolid__in=second_table_data)
       
    class1students = third_table_data.filter(className__in=['1'])
    class2students = third_table_data.filter(className__in=['2'])
    class3students = third_table_data.filter(className__in=['3'])
    class4students = third_table_data.filter(className__in=['4'])
    count_class1students=class1students.count()
    count_class2students=class2students.count()
    count_class3students=class3students.count()
    count_class4students=class4students.count()
    return render(request, 'admin-template/class1to4.html', {'k':k,'count_class1students':count_class1students,'count_class2students':count_class2students,'count_class3students':count_class3students,'count_class4students':count_class4students})

def class1(request):
    k=MenuItem.objects.filter(parent_category=None)

    second_table_data = Schools.objects.filter(usernumber=request.user.id)
    third_table_data = Student.objects.filter(schoolid__in=second_table_data)
    class1students = third_table_data.filter(className__in=['1'])
    return render(request,'admin-template/class.html',{'class1students':class1students,'k':k})

def class2(request):
    k=MenuItem.objects.filter(parent_category=None)

    second_table_data = Schools.objects.filter(usernumber=request.user.id)
    third_table_data = Student.objects.filter(schoolid__in=second_table_data)
    class2students = third_table_data.filter(className__in=['2'])
    return render(request,'admin-template/class.html',{'class2students':class2students,'k':k})

def class3(request):
    k=MenuItem.objects.filter(parent_category=None)

    second_table_data = Schools.objects.filter(usernumber=request.user.id)
    third_table_data = Student.objects.filter(schoolid__in=second_table_data)
    class3students = third_table_data.filter(className__in=['3'])
    return render(request,'admin-template/class.html',{'class3students':class3students,'k':k})

def class4(request):
    k=MenuItem.objects.filter(parent_category=None)

    second_table_data = Schools.objects.filter(usernumber=request.user.id)
    third_table_data = Student.objects.filter(schoolid__in=second_table_data)
    class4students = third_table_data.filter(className__in=['4'])
    return render(request,'admin-template/class.html',{'class4students':class4students,'k':k})

def classes5to8(request):
    k=MenuItem.objects.filter(parent_category=None)
   
    second_table_data = Schools.objects.filter(usernumber=request.user.id)
    third_table_data = Student.objects.filter(schoolid__in=second_table_data)
   
    class5students = third_table_data.filter(className__in=['5'])
    class6students = third_table_data.filter(className__in=['6'])
    class7students = third_table_data.filter(className__in=['7'])
    class8students = third_table_data.filter(className__in=['8'])
    count_class5students=class5students.count()
    count_class6students=class6students.count()
    count_class7students=class7students.count()
    count_class8students=class8students.count()
    return render(request, 'admin-template/class5to8.html', {'k':k,'count_class5students':count_class5students,'count_class6students':count_class6students,'count_class7students':count_class7students,'count_class8students':count_class8students})

def class5(request):
    k=MenuItem.objects.filter(parent_category=None)
    second_table_data = Schools.objects.filter(usernumber=request.user.id)
    third_table_data = Student.objects.filter(schoolid__in=second_table_data)
    class5students = third_table_data.filter(className__in=['5'])
    return render(request,'admin-template/class.html',{'class5students':class5students,'k':k})

def class6(request):
    k=MenuItem.objects.filter(parent_category=None)

    second_table_data = Schools.objects.filter(usernumber=request.user.id)
    third_table_data = Student.objects.filter(schoolid__in=second_table_data)
    class6students = third_table_data.filter(className__in=['6'])
    return render(request,'admin-template/class.html',{'class6students':class6students,'k':k})

def class7(request):
    k=MenuItem.objects.filter(parent_category=None)

    second_table_data = Schools.objects.filter(usernumber=request.user.id)
    third_table_data = Student.objects.filter(schoolid__in=second_table_data)
    class7students = third_table_data.filter(className__in=['7'])
    return render(request,'admin-template/class.html',{'class7students':class7students,'k':k})

def class8(request):
    k=MenuItem.objects.filter(parent_category=None)

    second_table_data = Schools.objects.filter(usernumber=request.user.id)
    third_table_data = Student.objects.filter(schoolid__in=second_table_data)
    class8students = third_table_data.filter(className__in=['8'])
    return render(request,'admin-template/class.html',{'class8students':class8students,'k':k})
   
        
def classes9to12(request):
    k=MenuItem.objects.filter(parent_category=None)

    
    second_table_data = Schools.objects.filter(usernumber=request.user.id)
    third_table_data = Student.objects.filter(schoolid__in=second_table_data)

    class9students = third_table_data.filter(className__in=['9'])
    class10students = third_table_data.filter(className__in=['10'])
    class11students = third_table_data.filter(className__in=['11'])
    class12students = third_table_data.filter(className__in=['12'])
    count_class9students=class9students.count()
    count_class10students=class10students.count()
    count_class11students=class11students.count()
    count_class12students=class12students.count()
    return render(request, 'admin-template/class9to12.html', {'k':k,'count_class9students':count_class9students,'count_class10students':count_class10students,'count_class11students':count_class11students,'count_class12students':count_class12students})

def class9(request):
    k=MenuItem.objects.filter(parent_category=None)

    second_table_data = Schools.objects.filter(usernumber=request.user.id)
    third_table_data = Student.objects.filter(schoolid__in=second_table_data)
    class9students = third_table_data.filter(className__in=['9'])
    return render(request,'admin-template/class.html',{'class9students':class9students,'k':k})

def class10(request):
    k=MenuItem.objects.filter(parent_category=None)

    second_table_data = Schools.objects.filter(usernumber=request.user.id)
    third_table_data = Student.objects.filter(schoolid__in=second_table_data)
    class10students = third_table_data.filter(className__in=['10'])
    return render(request,'admin-template/class.html',{'class10students':class10students,'k':k})

def class11(request):
    k=MenuItem.objects.filter(parent_category=None)

    second_table_data = Schools.objects.filter(usernumber=request.user.id)
    third_table_data = Student.objects.filter(schoolid__in=second_table_data)
    class11students = third_table_data.filter(className__in=['11'])
    return render(request,'admin-template/class.html',{'class11students':class11students,'k':k})

def class12(request):
    k=MenuItem.objects.filter(parent_category=None)

    second_table_data = Schools.objects.filter(usernumber=request.user.id)
    third_table_data = Student.objects.filter(schoolid__in=second_table_data)
    class12students = third_table_data.filter(className__in=['12'])
    return render(request,'admin-template/class.html',{'class12students':class12students,'k':k})


from django.shortcuts import render
from .models import Teachers
from django.http import HttpResponseRedirect

def staff_management(request):
    k=MenuItem.objects.filter(parent_category=None)
    return render(request,'admin-template/staff_management.html',{'k':k})

def teaching_staff(request):
    k=MenuItem.objects.filter(parent_category=None)
    sch = Schools.objects.filter(usernumber=request.user.id).first()
    plans = Teachers.objects.filter(schoolid=sch,staff_type='Teaching')
    teca=Teacher_Class_sub.objects.all()
    return render(request,'admin-template/Teaching_staff.html',{'plans':plans,'teca':teca,'k':k})

def non_teaching_staff(request):
    k=MenuItem.objects.filter(parent_category=None)
    sch = Schools.objects.filter(usernumber=request.user.id).first()
    t1 = Teachers.objects.filter(schoolid=sch,staff_type='Non-Teaching')
    return render(request,'admin-template/Non_Teaching_Staff.html',{'t1':t1,'k':k})



def get_teachers_count(request):
    sch = Schools.objects.filter(usernumber=request.user.id).first()
    teachers_count = Teachers.objects.filter(schoolid=sch).count()
    teaching_staff_count = Teachers.objects.filter(schoolid=sch, staff_type='Teaching').count()
    non_teaching_staff_count = Teachers.objects.filter(schoolid=sch, staff_type='Non-Teaching').count()
    return teachers_count, teaching_staff_count, non_teaching_staff_count

def get_student_class_count(request):
    sch = Schools.objects.filter(usernumber=request.user.id).first()
    student_count = Student.objects.filter(schoolid=sch).count()
    classes_count = cls_name.objects.filter(school_id=sch).count()
    return student_count,classes_count


from django.shortcuts import render 
from .models import fee_payment 

def class_form1(request):
    k = MenuItem.objects.filter(parent_category=None)    


    payments = fee_payment.objects.select_related('student_class', 'schoolid').all() 

    return render(request, "admin-template/fee_payment_table.html", {'k': k, 'payments': payments}) 



from django.shortcuts import render, get_object_or_404, redirect 
from .models import fee_payment, Student 

def update_fee_payment(request, payment_id):
    payment = get_object_or_404(fee_payment, id=payment_id) 

    if request.method == 'POST': 
        payment.amount = request.POST.get('amount') 
        payment.terms = request.POST.get('terms')
        payment.save()   

        return redirect('class_form1')  

    return render(request, 'admin-template/update_fee_payment.html', {'payment': payment})





def delete_fee_payment(request, payment_id):                
    payment = get_object_or_404(fee_payment, id=payment_id) 

    if request.method == 'POST':                           
        payment.delete()              

        return redirect('class_form1') 
    
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Teacher_Class_sub, Teachers, Schools, ZoomMeeting, cls_name, Subject
from django.db.models.fields import IntegerField
from django.db.models.functions import Cast

def create_meeting(request):
    school = Schools.objects.filter(usernumber=request.user.id).first()

    class_levels = cls_name.objects.filter(school_id=school).order_by(Cast('classes', output_field=IntegerField()))
    subjects = Subject.objects.filter(school_id=school)  # Filter subjects by school

    error_message = None  # Initialize error message variable

    if request.method == 'POST':
        class_level_id = request.POST.get('class_level')
        subject_id = request.POST.get('subject')
        selected_teacher_id = request.POST.get('teacher')
        event_details = request.POST.get('event_details')

        if class_level_id and subject_id and selected_teacher_id and event_details:
            try:
                meeting = ZoomMeeting.objects.create(
                    school=school,
                    class_name_id=class_level_id,
                    subject_name_id=subject_id,
                    Teacher_name_id=selected_teacher_id,
                    event_details=event_details,
                )
                return redirect('meeting_list1')
            except Exception as e:
                error_message = "Error creating meeting: {}".format(e)
        else:
            error_message = "Please select class, subject, and teacher, and provide event details."

    if request.GET.get('class_level'):
        class_level_id = request.GET.get('class_level')

        if request.GET.get('subject'):
            subject_id = request.GET.get('subject')
            teacher_class_subs = Teacher_Class_sub.objects.filter(
                class_name_id=class_level_id,
                subject_id=subject_id
            ).values('teacher_id')
            teacher_ids = teacher_class_subs.values_list('teacher_id', flat=True)
            teachers = Teachers.objects.filter(id__in=teacher_ids).values('id', 'first_name', 'last_name')
            return JsonResponse({'teachers': list(teachers)})
        else:
            subjects = Subject.objects.filter(
                school_id=school,
                teacher_class_sub__class_name_id=class_level_id
            ).distinct()
            return JsonResponse({'subjects': list(subjects.values('id', 'name'))})

    context = {
        'school': school,
        'class_levels': class_levels,
        'subjects': [],
        'teachers': [],
        'error_message': error_message,
    }

    return render(request, 'admin-template/meetings.html', context)

from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from .models import Schools, ZoomMeeting
import re

def meeting_list1(request):
    school = Schools.objects.filter(usernumber=request.user.id).first()
    
    if school:
        meetings = ZoomMeeting.objects.filter(school=school).order_by('-meeting_date')
        
        # Group meetings by class level
        meetings_by_class = {}
        for meeting in meetings:
            try:
                class_name = meeting.class_name.classes
            except ObjectDoesNotExist:
                class_name = "Unknown"  # Handle if class_name does not exist
                
            if class_name not in meetings_by_class:
                meetings_by_class[class_name] = []
            meetings_by_class[class_name].append(meeting)
    else:
        # If school is not found, return an empty dictionary
        meetings_by_class = {}

    def extract_meeting_link(event_details):
        if event_details is None:
            return ''
        pattern = r'https?://[^\s]+'
        match = re.search(pattern, event_details)
        if match:
            return match.group()
        return ''

    # Add the meeting link to each meeting object
    for class_name, meetings in meetings_by_class.items():
        for meeting in meetings:
            meeting.meeting_link = extract_meeting_link(meeting.event_details)

    context = {
        'meetings_by_class': meetings_by_class,
    }

    return render(request, 'admin-template/meeting_list1.html', context)
# .................................fees management................






# .........................class from.........

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Schools, cls_name, fee_payment, Student, MenuItem
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def class_form(request):
    try:
        k = MenuItem.objects.filter(parent_category=None)
        sch = Schools.objects.filter(usernumber=request.user.id).first()
        if not sch:
            messages.error(request, "School not found.")
            return redirect('some_default_route_if_no_school')

        student_classes = cls_name.objects.filter(school_id=sch).extra(select={'class_number': 'CAST(classes AS INTEGER)'}).order_by('class_number')

        if request.method == 'POST':
            amount = float(request.POST.get('amount'))
            class_id = request.POST.get('student_class')
            terms = int(request.POST.get('terms'))
            discount = float(request.POST.get('discount', 0))
            discounted_student_ids = request.POST.getlist('discounted_student_ids[]')

            class_instance = cls_name.objects.get(id=class_id)
            fee_payment.objects.filter(student_class=class_instance).delete()
            students_in_class = Student.objects.filter(className=class_instance)

            term_amount = amount / terms
            discount_term_amount = (amount - (amount * (discount / 100))) / terms

            for student in students_in_class:
                is_discounted = str(student.id) in discounted_student_ids
                final_term_amounts = [discount_term_amount if is_discounted else term_amount] * terms

                new_payment = fee_payment(
                    student_class=class_instance,
                    schoolid=sch,
                    amount=amount,
                    first_name=student.first_name,
                    s_class=student.className.classes,
                    terms=terms,
                    term1=final_term_amounts[0] if terms > 0 else None,
                    term2=final_term_amounts[1] if terms > 1 else None,
                    term3=final_term_amounts[2] if terms > 2 else None,
                    term4=final_term_amounts[3] if terms > 3 else None,
                    term5=final_term_amounts[4] if terms > 4 else None,
                    term6=final_term_amounts[5] if terms > 5 else None,
                    term7=final_term_amounts[6] if terms > 6 else None,
                    term8=final_term_amounts[7] if terms > 7 else None,
                    discount_percentage=discount if is_discounted else 0,
                )
                new_payment.save()

            messages.success(request, 'Payment details successfully updated.')
            return redirect('class_form')

        students = Student.objects.filter(schoolid=sch)
        return render(request, "admin-template/class_form.html", {'student_classes': student_classes, 'students': students, 'k': k})

    except cls_name.DoesNotExist:
        messages.error(request, "The specified class does not exist.")
        return redirect('class_form')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('class_form')

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import cls_name, Student

@login_required
def fetch_students(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        class_id = request.GET.get('class_id')
        if class_id:
            try:
                class_instance = cls_name.objects.get(id=class_id)
                students = Student.objects.filter(className=class_instance)
                students_data = [{'id': student.id, 'name': f'{student.first_name} {student.last_name}'} for student in students]
                return JsonResponse(students_data, safe=False)
            except cls_name.DoesNotExist:
                return JsonResponse([], safe=False)
    return JsonResponse([], safe=False)

def Fee_pay(request):
    k=MenuItem.objects.filter(parent_category=None)
    sch = Schools.objects.filter(usernumber=request.user.id).first()

    if request.method=="GET":
        # ob=Student.objects.values("student_class").distinct()
        # ob = Student.objects.filter(schoolid=sch).values("student_class").distinct()
        ob = Student.objects.filter(schoolid=sch).values("student_class").distinct().order_by('student_class')
        ob1=fee_payment.objects.all()
        return render(request,"admin-template/Feepayment.html",{'ob':ob,'k':k,'ob1':ob1})   

from django.shortcuts import render
from .models import Student, fee_payment 
from decimal import Decimal
from django.shortcuts import render
from django.http import HttpResponse
from .models import Schools, Student, fee_payment, cls_name, RazorpayPayment
from decimal import Decimal
import csv

def Fees_std_details(request, student_class):
    k = MenuItem.objects.filter(parent_category=None)
    sch = Schools.objects.filter(usernumber=request.user.id).first()
    if not sch:
        return HttpResponse("School not found", status=404)

    ob = Student.objects.filter(schoolid=sch).values("student_class").distinct().order_by('student_class')

    class_instance = cls_name.objects.filter(classes=student_class, school_id=sch).first()
    if not class_instance:
        return HttpResponse("Class not found", status=404)

    mn = fee_payment.objects.filter(student_class=class_instance)
    mns = mn.first()
    tem = mns.terms if mns else None

    ob1 = fee_payment.objects.all()
    st = mn.first()
    ter = st.terms if st else None
    payments = fee_payment.objects.filter(student_class=class_instance)

    if request.method == "GET":
        md = Student.objects.filter(student_class=student_class, schoolid=sch)

        for payment in mn:
            total_fee = Decimal(payment.amount).quantize(Decimal('0.00'))
            amount_paid = Decimal(payment.amountpaid).quantize(Decimal('0.00'))
            discount_percentage = Decimal(payment.discount_percentage).quantize(Decimal('0.00')) if payment.discount_percentage else Decimal('0.00')
            discount_amount = (total_fee * (discount_percentage / 100)).quantize(Decimal('0.00'))
            balance = (total_fee - amount_paid - discount_amount).quantize(Decimal('0.00'))
            payment.balance = balance
            payment.save()

        razorpay_transactions = RazorpayPayment.objects.filter(fee_payment__in=payments)

        return render(request, "admin-template/details.html", {
            'payments': payments,
            'ter': ter,
            'tem': tem,
            'md': md,
            'mn': mn,
            'st': st,
            'ob': ob,
            'k': k,
            'ob1': ob1,
            'razorpay_transactions': razorpay_transactions
        })


    elif request.method == "POST":
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="fee_payments.csv"'

        writer = csv.writer(response)
        writer.writerow(['First Name', 'Last Name', 'Amount', 'Amount Paid', 'Balance'])

        for payment in payments:
            writer.writerow([
                payment.first_name,
                '',
                Decimal(payment.amount).quantize(Decimal('0.00')),
                Decimal(payment.amountpaid).quantize(Decimal('0.00')),
                Decimal(payment.balance).quantize(Decimal('0.00'))
            ])

        return response


from django.shortcuts import render, get_object_or_404
from .models import RazorpayPayment, fee_payment
from decimal import Decimal, ROUND_HALF_UP

def download_receipt(request, payment_id):
    k = MenuItem.objects.filter(parent_category=None)
    sch = Schools.objects.filter(usernumber=request.user.id).first()


    # Retrieve the RazorpayPayment instance for the given payment ID
    transaction = get_object_or_404(RazorpayPayment, id=payment_id)

    # Retrieve the corresponding fee payment for the transaction
    fee_payment_obj = transaction.fee_payment

    # Retrieve the school information
    school = fee_payment_obj.schoolid
    organizationname = school.organizationname if school else "N/A"

    # Retrieve the fee payment details
    firstname = fee_payment_obj.first_name
    student_class = fee_payment_obj.student_class
    address = fee_payment_obj.address  # Ensure address is a field in FeePayment
    phone_number = fee_payment_obj.phone_number  # Ensure phone_number is a field in FeePayment
    total_amount = fee_payment_obj.amount
    amt = fee_payment_obj.amountpaid
    amount_paid = transaction.amount  # Amount paid in this transaction

    # Calculate the discount amount and the discounted total amount
    discount_percentage = Decimal(fee_payment_obj.discount_percentage)
    discount_amount = (total_amount * discount_percentage / 100).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    discounted_total_amount = (total_amount - discount_amount).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    # Calculate the remaining balance based on the discounted total amount
    remaining_balance = (discounted_total_amount - fee_payment_obj.amountpaid).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    # Create context to pass to the template
    context = {
        'organizationname': organizationname,
        'fee_payment_id': fee_payment_obj.id,
        'payment_id': transaction.payment_id,
        'total_amount': total_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
        'discount_percentage': discount_percentage.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
        'discount_amount': discount_amount,
        'discounted_total_amount': discounted_total_amount,
        'amount_paid_transaction': amount_paid.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
        'remaining_balance': remaining_balance,
        'transaction_date': transaction.created_at,
        'amt': amt.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
        'firstname': firstname,
        'student_class': student_class,  # Include student class in the context
        'address': address,              # Include address in the context
        'phone_number': phone_number,  
        'k':k  
    }

    # Render the invoice template with the transaction details
    return render(request, "admin-template/invoice.html", context)


from django.shortcuts import render, get_object_or_404
from .models import RazorpayPayment, fee_payment
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from decimal import Decimal

def download_receipt1(request, payment_id):
    # Get the transaction object
    transaction = get_object_or_404(RazorpayPayment, payment_id=payment_id)  # Use payment_id instead of id
    fee_payment_obj = transaction.fee_payment

    # Check payment status
    if transaction.status == 'captured':
        payment_status = "success"
    else:
        payment_status = "failed"

    # Get school and organization details
    school = fee_payment_obj.schoolid
    organizationname = school.organizationname if school else "N/A"

    # Get fee payment details
    firstname = fee_payment_obj.first_name  
    total_amount = fee_payment_obj.amount
    amount_paid_transaction = transaction.amount
    amt = fee_payment_obj.amountpaid

    # Calculate the discount
    discount_percentage = Decimal(fee_payment_obj.discount_percentage)
    discount_amount = (total_amount * discount_percentage) / 100
    discounted_total_amount = total_amount - discount_amount

    discount_percentage = discount_percentage.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    discount_amount = discount_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    discounted_total_amount = discounted_total_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    # Calculate the remaining balance based on the discounted total amount
    remaining_balance = discounted_total_amount - fee_payment_obj.amountpaid
    remaining_balance = remaining_balance.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    # Round amount paid in the transaction to 2 decimal places
    amount_paid_transaction = Decimal(amount_paid_transaction).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    context = {
        'organizationname': organizationname,
        'transaction': transaction,
        'fee_payment_obj': fee_payment_obj,
        'total_amount': total_amount,
        'discount_percentage': discount_percentage,
        'discount_amount': discount_amount,
        'discounted_total_amount': discounted_total_amount,
        'amount_paid_transaction': amount_paid_transaction,
        'remaining_balance': remaining_balance,
        'transaction_date': transaction.created_at,
        'fee_payment_id': fee_payment_obj.id,
        'amt': amt,
        'payment_id': transaction.payment_id,
        'firstname': firstname,
        'payment_status': payment_status  # Add payment status to context
    }

    # Render HTML to PDF
    template = get_template('admin-template/download.html')
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{payment_id}.pdf"'
        return response
    return HttpResponse('We had some errors while generating the PDF')

def term_payment_details(request, id):
    payment = fee_payment.objects.get(id=id)
    return render(request, "action.html", {'payment': payment})

from django.shortcuts import render 
from .models import fee_payment 
def class_form1(request):
    k = MenuItem.objects.filter(parent_category=None)    


    payments = fee_payment.objects.select_related('student_class', 'schoolid').all() 

    return render(request, "admin-template/fee_payment_table.html", {'k': k, 'payments': payments}) 


from django.shortcuts import render, get_object_or_404, redirect 
from .models import fee_payment, Student 

def update_fee_payment(request, payment_id):
    payment = get_object_or_404(fee_payment, id=payment_id) 

    if request.method == 'POST': 
        payment.amount = request.POST.get('amount') 
        payment.terms = request.POST.get('terms')
        payment.save()   

        return redirect('class_form1')  

    return render(request, 'admin-template/update_fee_payment.html', {'payment': payment})


def delete_fee_payment(request, payment_id):                
    payment = get_object_or_404(fee_payment, id=payment_id) 

    if request.method == 'POST':                           
        payment.delete()              

        return redirect('class_form1') 

# ..........................attedences..........

from .models import MenuItem, Student, Event, AttendanceRecord, MonthlyAttendanceSummary, Schools
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
import calendar

def alldata1(request):
    # Fetch the school data for the logged-in user
    data = Schools.objects.filter(usernumber=request.user.id).first()
    plans = Student.objects.filter(schoolid=data).order_by('className')
    k = MenuItem.objects.filter(parent_category=None)

    today = timezone.now().date()
    current_year = today.year
    current_month = today.month
    month_name = calendar.month_name[current_month]

    # Get the selected month from the request, default to current month
    selected_month = request.GET.get('month', current_month)
    selected_month = int(selected_month)
    selected_month_name = calendar.month_name[selected_month]

    # Get the first and last day of the selected month
    start_of_month = today.replace(day=1, month=selected_month)
    end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    student_data = []

    for student in plans:
        total_working_days = 0
        total_present_days = 0
        total_absent_days = 0
        total_half_days = 0

        # Get all attendance records for the selected month
        attendance_records = AttendanceRecord.objects.filter(student=student, date__gte=start_of_month, date__lte=end_of_month)
        
        # Create a set of all the dates in the selected month
        all_dates_in_month = set(start_of_month + timedelta(n) for n in range((end_of_month - start_of_month).days + 1))

        if start_of_month <= today <= end_of_month:
            # Handle current month
            for single_date in all_dates_in_month:
                is_working_day = False

                if single_date.weekday() == 6:  # Sunday
                    # Check if there's an event on this Sunday
                    event_on_sunday = Event.objects.filter(start=single_date).exists()
                    if event_on_sunday:
                        is_working_day = True
                else:
                    # Consider it a working day if it's not a Sunday or a holiday
                    if not Event.objects.filter(start=single_date).exists():
                        is_working_day = True

                if is_working_day:
                    total_working_days += 1
                    # Only check attendance for days up to today
                    if single_date <= today:
                        attendance_record = attendance_records.filter(date=single_date).first()
                        if attendance_record:
                            if attendance_record.status == "Full Day":
                                total_present_days += 1
                            elif attendance_record.status == "Half Day":
                                total_half_days += 1
                            elif attendance_record.status == "Absent":
                                total_absent_days += 1
                        else:
                            # No attendance record means it should be counted as absent
                            total_absent_days += 1
        elif start_of_month < today:
            # Handle past months
            for single_date in all_dates_in_month:
                if single_date > today:
                    continue

                is_working_day = False

                if single_date.weekday() == 6:  # Sunday
                    event_on_sunday = Event.objects.filter(start=single_date).exists()
                    if event_on_sunday:
                        is_working_day = True
                else:
                    if not Event.objects.filter(start=single_date).exists():
                        is_working_day = True

                if is_working_day:
                    total_working_days += 1
                    attendance_record = attendance_records.filter(date=single_date).first()
                    if attendance_record:
                        if attendance_record.status == "Full Day":
                            total_present_days += 1
                        elif attendance_record.status == "Half Day":
                            total_half_days += 1
                        elif attendance_record.status == "Absent":
                            total_absent_days += 1
                    else:
                        total_absent_days += 1
        else:
            # Handle future months
            for single_date in all_dates_in_month:
                if single_date <= today:
                    continue

                is_working_day = False

                if single_date.weekday() == 6:  # Sunday
                    event_on_sunday = Event.objects.filter(start=single_date).exists()
                    if event_on_sunday:
                        is_working_day = True
                else:
                    if not Event.objects.filter(start=single_date).exists():
                        is_working_day = True

                if is_working_day:
                    total_working_days += 1

        # Calculate the percentage
        percentage = ((total_present_days +(total_half_days/2))/ total_working_days) * 100 if total_working_days > 0 else 0

        # Create or update the monthly attendance summary record
        monthly_summary, created = MonthlyAttendanceSummary.objects.get_or_create(
            student=student,
            month=selected_month_name,
            year=current_year,
            defaults={
                'total_working_days': total_working_days,
                'total_present_days': total_present_days,
                'total_absent_days': total_absent_days,
                'total_half_days': total_half_days,
                'percentage': percentage
            }
        )

        if not created:
            monthly_summary.total_working_days = total_working_days
            monthly_summary.total_present_days = total_present_days
            monthly_summary.total_absent_days = total_absent_days
            monthly_summary.total_half_days = total_half_days
            monthly_summary.percentage = round(percentage,2)
            monthly_summary.save()

        student_data.append({
            'student': student,
            'monthly_summary': monthly_summary,
        })

    months = [(i, calendar.month_name[i]) for i in range(1, 13)]

    return render(request, 'admin-template/alldata.html', {
        'plans': plans,
        'k': k,
        'student_data': student_data,
        'selected_month': selected_month,
        'months': months,
    })


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
from .models import LateLoginRequest

def is_admin(user):
    return user.is_staff

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from .models import LateLoginRequest, Notification

def approve_late_login_request(request, request_id):
    late_request = get_object_or_404(LateLoginRequest, id=request_id)
    
    if not late_request.approved:
        late_request.approved = True
        late_request.rejected = False
        late_request.approved_at = timezone.now()
        late_request.save()
        
        # Send notification to the student
        Notification.objects.create(
            student=late_request.student,
            message="Your late login request has been approved."
        )

        messages.success(request, f"Late login request for {late_request.student.username} has been approved.")
    
    return redirect('late_login_requests_list')


def reject_late_login_request(request, request_id):
    late_request = get_object_or_404(LateLoginRequest, id=request_id)
    
    if not late_request.rejected:
        late_request.approved = False
        late_request.rejected = True
        late_request.save()

        # Send notification to the student
        Notification.objects.create(
            student=late_request.student,
            message="Your late login request has been rejected."
        )

        messages.success(request, f"Late login request for {late_request.student.username} has been rejected.")
    
    return redirect('late_login_requests_list')



def late_login_requests_list(request):
    late_login_requests = LateLoginRequest.objects.select_related('student').all().order_by('-date')
    k = MenuItem.objects.filter(parent_category=None)
    return render(request, 'admin-template/latelogin.html', {'late_login_requests': late_login_requests, 'k': k})



