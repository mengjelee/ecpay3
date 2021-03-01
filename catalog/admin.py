from django.contrib import admin

# Register your models here.
from .models import User, Class, Class_DayTime, Class_details, Payment#Author, Genre, Book, BookInstance, 

# Register the user
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name','email','status','bank_account','bank_no','account','password')

# Register the class
@admin.register(Class) 
class ClassAdmin(admin.ModelAdmin):
    list_display = ('class_id','class_serial', 'subject','tutor','student',
                    'pay_per_class','start_date','end_date','pay_or_not', 'trade_no')
    
# Register the class_daytime
@admin.register(Class_DayTime) 
class Class_DayTimeAdmin(admin.ModelAdmin):
    list_display = ('class_serial', 'class_day', 'start_time','end_time')

# Register the class_details
@admin.register(Class_details) 
class Class_detailsAdmin(admin.ModelAdmin):
    list_display = ('class_detail_id','class_serial', 'class_date', 'fee',
                    'start_time','end_time', 'finish_or_not', 'description')
    
@admin.register(Payment) 
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('trade_no','trade_amt', 'trade_status', 'trade_time',
                    'CheckMacValue')
