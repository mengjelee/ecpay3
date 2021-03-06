from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
        path('', views.index, name='index'),
        path('register/', views.register, name='register'),
        path('login/', views.login, name='login'),
        path('logout/', views.logout_user, name='logout_user'),
        path('homepage/', views.calendar, name='homepage'),
        path('calendar/', views.calendar, name='calendar'),
        path('new_course/', views.new_course, name='new_course'),
        path('new_single_course/', views.new_single_course, name='new_single_course'),
        path('delete_course/', views.delete_course, name='delete_course'),
        path('mydata/', views.mydata, name='mydata'),
        path('editdata/', views.editdata, name='editdata'),
        path('changepw/', views.changepw, name='changepw'),
        path('ecpay/', views.ecpay_view, name='ecpay'),
        path('ecpay/success_pay', views.success_pay, name='success_pay'),
        path('ecpay/fail_pay', views.fail_pay, name='fail_pay'),
        path('ecpay/end_page', views.end_page, name='end_page'),
        path('ecpay/end_return', views.end_return, name='end_return'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)