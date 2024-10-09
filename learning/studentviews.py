from django.shortcuts import render ,get_object_or_404 ,redirect 
from . models import *

from datetime import datetime, timedelta
from django.http import HttpResponse,HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import render

def student_sidebar(request):

    login=Student.objects.get(mystudent=request.user.id)  

    k5=compose_message.objects.filter(studentname=login)  

    k4=leave.objects.filter(admin=request.user.id,read1=0)   

    leave_count = leave.objects.filter(admin=request.user.id,read1=0).count() 
    k = studentnav.objects.filter(parent_category=None)                                    
    
    k1=compose_message.objects.filter(studentname=login,read1=0)  


    k7=compose_message.objects.filter(studentname=login,read1=0)    

    message_count = compose_message.objects.filter(studentname=login,read1=0).count() 

    total_count=  leave_count+ message_count; 

    current_time = timezone.now()  # Get the current time in UTC


    
    return render(request,'student-template/student_sidebar.html',{'k':k,'k4':k4,'leave_count':leave_count,'k5':k5,'k1':k1,'k7':k7,'message_count':message_count,'total_count':total_count,'current_time':current_time})

    
def student_applyforleave(request):
    k2=leave.objects.filter(admin=request.user.id)
    # k2=leave.objects.all()
    k = studentnav.objects.filter(parent_category=None)

    k1=leavestype.objects.all()
    adminid=CustomUser.objects.get(id=request.user.id)
    pending_leave_count = leave.objects.filter(is_status=0,admin=request.user.id).count()
    approved_leave_count = leave.objects.filter(is_status=1,admin=request.user.id).count()
    disapproved_leave_count = leave.objects.filter(is_status=2,admin=request.user.id).count()

    if request.method == "POST":
        Leave_Type=request.POST.getlist('Leave_Type')
        Reason=request.POST.get('Reason')
        from_date_str = request.POST.get('from_date')
        to_date_str = request.POST.get('to_date')

        from_date = datetime.strptime(from_date_str, '%Y-%m-%dT%H:%M')
        to_date = datetime.strptime(to_date_str, '%Y-%m-%dT%H:%M')

        days_difference = (to_date - from_date).days

        for Leave_Type, from_date_str, to_date_str in zip(Leave_Type, from_date_str,to_date_str):
            if Leave_Type and from_date_str and to_date_str:
                Leave_instance = leavestype.objects.get(id=Leave_Type)
                k3=leave(Leave_Type=Leave_instance,Reason=Reason,from_date=from_date,to_date=to_date,admin=adminid,user_type=3,days_difference=days_difference)
                k3.save()

    return render(request,'student-template/student_apply_leave.html',{'k':k,'k1':k1,'k2':k2,'pending_leave_count':pending_leave_count,'approved_leave_count':approved_leave_count,'disapproved_leave_count':disapproved_leave_count})

def mark_all_as_read2(request):
    leave.objects.filter(admin=request.user.id).update(read1=True)
    return HttpResponseRedirect('/student_sidebar') 
    
def student_mark_as_read(request, leave_id):
    leave_obj = get_object_or_404(leave, id=leave_id)
    leave_obj.read1 = True
    leave_obj.save()
    return HttpResponseRedirect('/student_sidebar')




from .models import teachermenu
def student_showmessage(request):
    # login=Teachers.objects.get(admin=request.user.id)
    # k2=compose_message.objects.filter(teachername=login)
    # leave_count = compose_message.objects.count()

    k=studentnav.objects.filter(parent_category=None)
    k2=compose_message.objects.filter(studentname__mystudent=request.user.id)
    for message in k2:
        if message.MessageType == "0":
            message.ShortMessage = message.Message
        if message.MessageType == "1":
            message.ShortMessage = message.Message
        if message.MessageType == "2":
            message.ShortMessage = message.Message
        if message.MessageType == "3":
            message.ShortMessage = message.Message 
    




    return render(request,'student-template/student_showmessage.html',{'k2':k2,'k':k})

def student_all_messages_as_read(request):   
    login=Student.objects.get(mystudent=request.user.id)
                                
    compose_message.objects.filter(studentname=login).update(read1=True)
    return HttpResponseRedirect('/student_sidebar')
def student_messages_mark_as_read(request, compose_message_id):
    compose_message_obj = get_object_or_404(compose_message, id=compose_message_id)
    compose_message_obj.read1 = True
    compose_message_obj.save()
    return HttpResponseRedirect('/student_showmessage')   

def general_instructions(request):
    k=studentnav.objects.filter(parent_category=None)
    p=instruction_headings.objects.all()
    q=instructions11.objects.all()
    return render(request,"student-template/general_instructions.html",{'k':k,'p':p,'q':q})

def quiz_subjects(request):
    current_student = Student.objects.get(mystudent=request.user)
    qu = Teacher_Class_sub.objects.filter(class_name=current_student.class_name,is_correct=1,school_id=current_student.schoolid)
    return render(request, 'student-template/quiz_subjects.html', {'qu': qu})


def std_quiz(request):
    k = studentnav.objects.filter(parent_category=None)
    current_student = Student.objects.get(mystudent=request.user)
    # ob = Teacher_Class_sub.objects.filter(class_name=current_student.className)
    ob= Teacher_Class_sub.objects.filter(class_name=current_student.className,is_control=1,school_id=current_student.schoolid)

    return render(request, "student-template/ssu.html", {'ob': ob,'k':k})


def std_quiz1(request,subject):
    k = studentnav.objects.filter(parent_category=None)
    current_student = Student.objects.get(mystudent=request.user)
    obb = quiz_questions.objects.filter(class_name=current_student.className,subject_id=subject)
    mn=set_timer.objects.filter(class_name=current_student.className,subject_id=subject)
   
    if request.method == "POST":
        try:
            for question in obb:
                answer = request.POST.get('answer{}'.format(question.id))
                result = std_result(questionstd=question.question, answer=answer,student=current_student,classes=current_student.className,subject_id_id=subject)
                result.save()
            return HttpResponse('Submited Successfully..!!')
        except Exception as e:
            return HttpResponse(f'Error: {str(e)}')
    return render(request, "student-template/ssu1.html", {'obb': obb,'k':k,'mn':mn}) 
    



# ..................................fees management....................

from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import fee_payment, studentnav, Student,RazorpayPayment
from decimal import Decimal

def studentfeepay_form(request):
    student = get_object_or_404(Student, mystudent=request.user.id)
    k = studentnav.objects.filter(parent_category=None)
    fee_payments = fee_payment.objects.filter(first_name=student.first_name, student_class=student.className)
    razorpay_transactions = RazorpayPayment.objects.filter(fee_payment__in=fee_payments)

    for payment in fee_payments:
        term1 = float(payment.term1) if payment.term1 else 0
        term2 = float(payment.term2) if payment.term2 else 0
        term3 = float(payment.term3) if payment.term3 else 0
        term4 = float(payment.term4) if payment.term4 else 0
        term5 = float(payment.term5) if payment.term5 else 0
        term6 = float(payment.term6) if payment.term6 else 0
        term7 = float(payment.term7) if payment.term7 else 0
        term8 = float(payment.term8) if payment.term8 else 0

        total_paid = round(term1 + term2 + term3 + term4 + term5 + term6 + term7 + term8, 2)
        remaining_balance = round(total_paid, 2)

        if remaining_balance < 1:
            remaining_balance = 0.00

        payment.balance = remaining_balance

    return render(request, "student-template/studentfeepay_form.html", {'k': k, 'fee_payments': fee_payments,'razorpay_transactions': razorpay_transactions})

from django.shortcuts import render, get_object_or_404
from .models import fee_payment, RazorpayPayment

def payment_details_view(request, fee_payment_id):
    # Retrieve the fee_payment object
    fee_payment_instance = get_object_or_404(fee_payment, id=fee_payment_id)

    # Retrieve all RazorpayPayment objects related to this fee_payment
    razorpay_transactions = RazorpayPayment.objects.filter(fee_payment=fee_payment_instance)

    context = {
        'razorpay_transactions': razorpay_transactions,
        'fee_payment_instance': fee_payment_instance,
    }

    return render(request, 'studentfeepay_form.html', context)


def studentpayfee_edit(request, id):
    k = studentnav.objects.filter(parent_category=None) 
    if request.method == "GET":
        u = fee_payment.objects.get(id=id)
        return render(request, "student-template/studentfee_update.html", {'u': u, 'k': k})

def studentpayfee_update(request, id):
    k = studentnav.objects.filter(parent_category=None)
    sch = Student.objects.filter(mystudent=request.user.id).first()

    if request.method == "POST":
        form_data = request.POST

        def safe_float(value):
            try:
                return float(value)
            except ValueError:
                return 0.0  # Return a default value if conversion fails

        term1 = safe_float(form_data.get('term1', 0))
        term2 = safe_float(form_data.get('term2', 0))
        term3 = safe_float(form_data.get('term3', 0))
        term4 = safe_float(form_data.get('term4', 0))
        term5 = safe_float(form_data.get('term5', 0))
        term6 = safe_float(form_data.get('term6', 0))
        term7 = safe_float(form_data.get('term7', 0))
        term8 = safe_float(form_data.get('term8', 0))
        amountpaid = safe_float(form_data.get('amountpaid', 0))
        
        u = get_object_or_404(fee_payment, id=id)

        remaining_amount = amountpaid

        if remaining_amount >= term1:
            remaining_amount -= term1
            term1 = 0
        else:
            term1 -= remaining_amount
            remaining_amount = 0

        if remaining_amount >= term2:
            remaining_amount -= term2
            term2 = 0
        else:
            term2 -= remaining_amount
            remaining_amount = 0

        if remaining_amount >= term3:
            remaining_amount -= term3
            term3 = 0
        else:
            term3 -= remaining_amount
            remaining_amount = 0

        if remaining_amount >= term4:
            remaining_amount -= term4
            term4 = 0
        else:
            term4 -= remaining_amount
            remaining_amount = 0

        if remaining_amount >= term5:
            remaining_amount -= term5
            term5 = 0
        else:
            term5 -= remaining_amount
            remaining_amount = 0

        if remaining_amount >= term6:
            remaining_amount -= term6
            term6 = 0
        else:
            term6 -= remaining_amount
            remaining_amount = 0

        if remaining_amount >= term7:
            remaining_amount -= term7
            term7 = 0
        else:
            term7 -= remaining_amount
            remaining_amount = 0

        term8 -= remaining_amount

        u.term1 = term1
        u.term2 = term2
        u.term3 = term3
        u.term4 = term4
        u.term5 = term5
        u.term6 = term6
        u.term7 = term7
        u.term8 = term8

        if isinstance(u.amountpaid, str):
            u.amountpaid = float(u.amountpaid)

        u.amountpaid += Decimal(str(amountpaid))
        u.transaction_datetime = timezone.now()

        u.save(update_fields=['term1', 'term2', 'term3', 'term4', 'term5', 'term6', 'term7', 'term8', 'amountpaid', 'transaction_datetime'])

        payment_id = form_data.get('payment_id')
        order_id = form_data.get('order_id')
        status = form_data.get('status')
        method = form_data.get('method')  # Ensure this field is retrieved
        description = form_data.get('description')
        created_at = timezone.now()
        captured_at = created_at if status == 'captured' else None

        # Ensure method is not null or empty
        if not method:
            method = "unknown"  # or handle this scenario as needed

        RazorpayPayment.objects.create(
            payment_id=payment_id,
            order_id=order_id,
            amount=amountpaid,
            currency='INR',
            status=status,
            method=method,
            description=description,
            created_at=created_at,
            captured_at=captured_at,
            fee_payment=u
        )

        return redirect("studentfeepay_form")

    return render(request, 'student-template/studentfee_update.html', {'k': k})


from .models import MonthlyAttendanceSummary, Student
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import calendar
from django.utils import timezone

@login_required
def alldata3(request):
    user_email = request.user.email
    student = Student.objects.filter(email=user_email).first()
    k = studentnav.objects.filter(parent_category=None)

    # Get the current month and year
    today = timezone.now().date()
    current_year = today.year
    current_month = today.month

    # Get the selected month from the request, default to current month
    selected_month = request.GET.get('month', current_month)
    selected_month = int(selected_month)

    # Fetch the relevant MonthlyAttendanceSummary for the selected month
    if student:
        monthly_attendance_summaries = MonthlyAttendanceSummary.objects.filter(
            student=student,
            month=calendar.month_name[selected_month],
            year=current_year
        )
    else:
        monthly_attendance_summaries = []

    # Optionally: Get the list of months for the dropdown
    months = [(i, calendar.month_name[i]) for i in range(1, 13)]

    return render(request, 'student-template/alldata.html', {
        'monthly_attendance_summaries': monthly_attendance_summaries,
        'selected_month': selected_month,
        'months': months,
        'student': student,  # Pass the student object to the template
        'k': k
    })



from django.shortcuts import render, get_object_or_404
from .models import RazorpayPayment, fee_payment, Schools
from decimal import Decimal, ROUND_HALF_UP

def download_receipt2(request, payment_id):
    k = studentnav.objects.filter(parent_category=None)
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
    return render(request, "student-template/invoice_student.html", context)


from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .forms import LateLoginRequestForm
from .models import LateLoginRequest, Student
from .models import studentnav

def student_apply_for_late_login_permission(request):
    k = studentnav.objects.filter(parent_category=None)

    if request.method == 'POST':
        form = LateLoginRequestForm(request.POST)
        if form.is_valid():
            late_login_request = form.save(commit=False)
            student = Student.objects.get(mystudent=request.user)
            late_login_request.student = student
            late_login_request.date = timezone.now().date()
            late_login_request.save()

            messages.success(request, 'Your late login request has been sent successfully.')

            return redirect('student_apply_for_late_login_permission')  # Redirect to clear the form
    else:
        form = LateLoginRequestForm()

    return render(request, 'student-template/permissionlogin.html', {'form': form, 'k': k})


def notification1(request):
    student = Student.objects.get(mystudent=request.user)
    k = studentnav.objects.filter(parent_category=None)

    notifications = Notification.objects.filter(student=student, is_read=False)

    return render(request, 'student-template/notification.html', {'notifications': notifications,'k':k})


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Notification  # Add any other required imports

def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'success'})

