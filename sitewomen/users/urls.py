from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # path('login/', views.login_user, name='login'),
    path('login/', views.LoginUser.as_view(), name='login'),

    # path('logout/', LogoutView.as_view(), name='logout'), # не работает
    path('logout/', views.logout_user, name='logout'),
]
