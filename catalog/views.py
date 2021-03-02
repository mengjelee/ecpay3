from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .ecpay_testing import main
# Create your views here.
from .models import User, Class, Class_DayTime, Class_details, Payment #Book, Author, BookInstance, Genre,
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from datetime import datetime, timedelta
from django.db.models import Sum

def ecpay_view(request):
    context = {
        'user_name': request.COOKIES['user_name'],
        'user_account': request.COOKIES['user_account'],
    }
   user_id = request.COOKIES['user_id']
    class_ = Class.objects.filter(tutor = user_id).first()
    class_serial = class_.class_serial#從前端接收
    context['class_serial'] = class_serial
    #價格計算
    c = Class.objects.get(class_serial = class_serial)
    result = Class_details.objects.filter(class_serial = c).aggregate(total = Sum('fee'))
    context.update(result)
    #if request.COOKIES != None:
    return HttpResponse(main(context))

def index(request):
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'frontpage.html')

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        # 如果登入成功，繫結引數到cookie中，set_cookie
        account = request.POST.get('account')
        password = request.POST.get('password')
        
        # 查詢使用者是否在資料庫中
        if User.objects.filter(account=account).exists():
            user = User.objects.get(account=account)
            if password == user.password:#check_password(password, user.password):
                response = HttpResponseRedirect('../homepage/')
                response.set_cookie("user_id", user.user_id)
                response.set_cookie("user_account", user.account)
                response.set_cookie("user_name", user.name)
                response.set_cookie("user_email", user.email)
                if user.status == 1:
                    response.set_cookie("user_status", "Teacher")
                else:
                    response.set_cookie("user_status", "Student")
                response.set_cookie("user_bank_no", user.bank_no)
                response.set_cookie("user_bank_account", user.bank_account)
                return response
        messages.error(request, '使用者帳號或密碼錯誤')
        return HttpResponseRedirect(reverse('index'))       
        #return render(request, 'frontpage.html')

def register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        status = request.POST.get('status')
        email = request.POST.get('email')
        bank_no = request.POST.get('bank_no')
        bank_account = request.POST.get('bank_account')        
        password = request.POST.get('password')
        user_id = User.objects.count()
        user = User.objects.create(user_id = user_id, name = name, password = password, email = email, status = status, bank_account = bank_account, bank_no = bank_no)
        account = str(user_id)
        while(len(account)!=5):
            account = '0' + account
        if user.status == '1':
            account = 'T' + account
        else:
            account = 'S' + account
        user.account = account
        user.save()
        messages.success(request, '註冊成功！你的帳號是 %s' %account) # 
        return HttpResponseRedirect('../')
    return render(request, 'register.html')

def homepage(request):
    if request.COOKIES != None: 
        try:
            user_name = request.COOKIES['user_name']
        except:
            return HttpResponse('No user name.') 
    context = {
        'user_name': user_name
    }
    return render(request, 'calendarpage/calendar.html', context)

def calendar(request):
    teacher_id = request.COOKIES['user_id']
    courses = Class.objects.filter(tutor=teacher_id)
    course_value = Class.objects.filter(tutor=teacher_id).values()
    course = [entry for entry in course_value]
    course_detail = []
    for c in courses:
        detail_value = Class_details.objects.filter(class_serial=c).values()
        course_detail.extend([entry for entry in detail_value])
    return render(request, 'calendarpage/calendar.html', {'course':course, 'course_detail':course_detail})

def new_course(request):
    if request.method == 'GET':
        return render(request, 'calendarpage/input.html')
    elif request.method == 'POST':
        student_id = request.POST.get('student_id')
        if User.objects.filter(account = student_id).exists():
            student_id = User.objects.get(account = student_id)
            teacher_id = request.COOKIES['user_account']
            teacher_id = User.objects.get(account = teacher_id)
            subject = request.POST.get('subject')
            fee = request.POST.get('fee')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            class_id = Class.objects.count()
            course = Class.objects.create(class_id = class_id, tutor = teacher_id, student = student_id, subject = subject, 
                                        pay_per_class = fee, start_date = start_date, end_date = end_date)
            # 新增課程日
            i=0
            days=[]
            more_daytime = True
            while(more_daytime):
                day = request.POST.get(('day'+str(i)))
                if day is None:
                    more_daytime = False
                    break
                start_time = request.POST.get(('start_time'+str(i)))
                end_time = request.POST.get(('end_time'+str(i)))
                days.append(day)
                i+=1
                Class_DayTime.objects.create(class_serial = course, class_day = day, start_time = start_time, end_time = end_time)
            # 課程序號
            serial = "C"
            days.sort()
            for day in days:
                serial += str(day)
            serial += str(subject)
            serial_no = str(class_id)
            while(len(serial_no)!=4):
                serial_no = '0' + serial_no
            course.class_serial = serial + serial_no
            course.save()
            # 新增課程細項
            class_daytime = Class_DayTime.objects.filter(class_serial = course)            
            date_end = datetime.strptime(end_date, "%Y-%m-%d")
            for i in range(7):
                date2add = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)
                dayinweek = date2add.isoweekday()
                for c_daytime in class_daytime:
                    if c_daytime.class_day == dayinweek:
                        start_time = c_daytime.start_time
                        end_time = c_daytime.end_time
                        while(date2add<=date_end):
                            Class_details.objects.create(class_serial = course, class_date = date2add, fee = fee,
                                                         start_time = start_time, end_time = end_time)
                            date2add += timedelta(days=7)
                        break                                
            messages.error(request, '成功新增課程')
            return HttpResponseRedirect(reverse('calendar'))
        else:
            messages.error(request, '學生不存在')
            return HttpResponseRedirect(reverse('new_course'))

def editdata(request):
    if request.method == 'GET':
        if request.COOKIES != None: 
            try:
                context = {
                    'user_name': request.COOKIES['user_name'],
                    'user_email': request.COOKIES['user_email'],
                    'user_status': request.COOKIES['user_status'],
                    'user_card_number': request.COOKIES['user_card_number'],
                } 
            except:
                return HttpResponse('User undifined.') 
        return render(request, 'editdata.html', context)
    elif request.method == 'POST':
        user_id = request.COOKIES['user_id']
        if User.objects.filter(user_id = user_id).exists():
            user = User.objects.get(user_id = user_id)
            user.name = request.POST.get('name')
            user.email = request.POST.get('email')
            user.card_number = request.POST.get('card_number')
            user.save()
            messages.success(request, '資料修改成功')
            response = HttpResponseRedirect('../homepage/')
            response.set_cookie("user_name", user.name)
            response.set_cookie("user_email", user.email)
            response.set_cookie("user_card_number", user.card_number)
            return response
        else:
            messages.error(request, '資料修改失敗')
            return HttpResponseRedirect(reverse('editdata'))

def changepw(request):
    if request.method == 'GET':
        return render(request, 'changepw.html')
    elif request.method == 'POST':
        password = request.POST.get('pw')
        newpw = request.POST.get('newpw')
        confirmpw = request.POST.get('confirmpw')
        if password == newpw or newpw != confirmpw:
            messages.error(request, '請重新輸入密碼')
            return HttpResponseRedirect(reverse('changepw'))
        user_id = request.COOKIES['user_id']
        if User.objects.filter(user_id = user_id).exists():
            user = User.objects.get(user_id = user_id)
            if password == user.password:
                user.password = newpw
                user.save() #儲存
                messages.success(request, '密碼修改成功，請重新登錄！')
                response = HttpResponseRedirect('../login/')
                return response
            else:
                messages.error(request, '請重新輸入密碼')
                return HttpResponseRedirect(reverse('changepw'))

def success_pay(request):
    return render(request, 'success.html')

def fail_pay(request):
    return render(request, 'fail.html')
#@csrf_protect
def end_page(request):
    if request.method == 'GET':
        paymenet = Payment.objects.create(trade_no =request.POST.get('TradeNo'), trade_amt =0,CheckMacValue='fail')
        return HttpResponseRedirect(reverse('fail_pay'))

    if request.method == 'POST':
        result = request.POST.get('RtnMsg')
        if result == 'Succeeded':
            paymenet = Payment.objects.create(trade_no =request.POST.get('TradeNo'), trade_amt =request.POST.get('TradeAmt'),trade_status='Succeeded',trade_time=request.POST.get('TradeDate'),CheckMacValue=request.POST.get('CheckMacValue'))
            # class_serial = request.POST.get('ItemName')
            # c = Class.objects.get(class_serial = class_serial)
            # c.update(trade_no=paymenet, pay_or_not = True)
            return HttpResponseRedirect(reverse('success_pay'))
        # 判斷失敗
        else:
            paymenet = Payment.objects.create(trade_no =request.POST.get('TradeNo'), trade_amt =request.POST.get('TradeAmt'),trade_status='Failed',trade_time=request.POST.get('TradeDate'),CheckMacValue=request.POST.get('CheckMacValue'))
            return HttpResponseRedirect(reverse('fail_pay'))

def end_return(request):
    if request.method == 'POST':
        return '1|OK'