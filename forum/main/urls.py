from django.urls import path
from .forms import UserLoginForm
from .views import index, create, profile_status
from .views import LoginView
from .views import profile
from .views import LogoutView
from .views import RegisterViews

from .views import delete

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('login/', LoginView.as_view(template_name='main/login.html', authentication_form=UserLoginForm), name='login'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/<str:status>', profile_status, name='profile_status'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterViews.as_view(), name='register'),
    path('accounts/create/', create, name='create'),
    path('accounts/profile/<pk>', delete, name='delete'),

]
