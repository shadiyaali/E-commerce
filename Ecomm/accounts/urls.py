
from django.urls import path
from . import views

urlpatterns = [
    
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('user_dashboard/',views.user_dashboard, name= 'user_dashboard'),
    path('dashboard',views.user_dashboard, name= 'dashboard'),
    
    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    path('forgotpassword/',views.forgotpassword, name='forgotpassword'),
    path('resetpassword_validate/<uidb64>/<token>/',views.resetpassword_validate, name='resetpassword_validate'),
    path('resetpassword/',views.resetpassword, name='resetpassword'),
    path('edit_profile/',views.edit_profile, name='edit_profile'), 
    path('change_password/',views.change_password, name='change_password'), 
    
]
